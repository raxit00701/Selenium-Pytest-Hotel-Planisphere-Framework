from __future__ import annotations
import csv
import io
from pathlib import Path
from typing import List, Dict, Iterable, Sequence, Tuple, Optional

# ---------------------------
# Project root / path resolve
# ---------------------------

def _project_root_candidates() -> list[Path]:
    here = Path(__file__).resolve()
    candidates = [
        here.parents[2],   # project root in our layout
        Path.cwd(),        # pytest working dir
    ]
    # Walk up to find dirs containing 'config' or 'data'
    p = here
    for _ in range(5):
        if (p / "config").exists() or (p / "data").exists():
            candidates.append(p)
        p = p.parent
    # Deduplicate, preserve order
    seen: set[Path] = set()
    uniq: list[Path] = []
    for c in candidates:
        if c not in seen:
            uniq.append(c)
            seen.add(c)
    return uniq


def _resolve_csv_path(path: str | Path) -> Path:
    p = Path(path)
    if p.is_absolute() and p.exists():
        return p
    if p.exists():
        return p
    for root in _project_root_candidates():
        cand = (root / p).resolve()
        if cand.exists():
            return cand
        if not p.parent or str(p.parent) in (".", ""):
            alt = (root / "data" / p.name).resolve()
            if alt.exists():
                return alt
    return (Path.cwd() / p).resolve()

# ---------------------------
# IO / CSV helpers
# ---------------------------

def _open_text(path: Path, encoding: str | None) -> io.TextIOWrapper:
    enc = encoding or "utf-8-sig"  # BOM-friendly
    return path.open("r", encoding=enc, newline="")

def _sniff_dialect(sample: str) -> csv.Dialect:
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;|\t")
    except Exception:
        class _Default(csv.Dialect):
            delimiter = ","
            quotechar = '"'
            escapechar = None
            doublequote = True
            lineterminator = "\n"
            quoting = csv.QUOTE_MINIMAL
            skipinitialspace = True
        return _Default()

def _norm_header(h: str, mode: str) -> str:
    if h is None:
        return ""
    s = str(h).strip()
    if mode == "lower":
        return s.lower()
    if mode == "lower_underscore":
        return (
            s.strip()
             .lower()
             .replace(" ", "_")
             .replace("-", "_")
        )
    return s  # identity

# ---------------------------
# Public API
# ---------------------------

def read_csv(
    path: str | Path,
    has_header: bool = True,
    encoding: str | None = None,
    delimiter: str | None = None,
    quotechar: str | None = None,
    escapechar: str | None = None,
    header_normalization: str = "lower_underscore",  # NEW: normalize headers by default
    required: Optional[Sequence[str]] = None,        # NEW: ensure columns exist
) -> List[Dict[str, str]] | List[List[str]]:
    """
    Read a CSV file with robust defaults.

    - Path can be absolute, relative to CWD, or just a filename (also tries <project>/data/<file>).
    - Auto-detects delimiter among ',', ';', '|', and tab, unless you pass one.
    - BOM-friendly via 'utf-8-sig'.
    - has_header=True -> List[Dict[str,str]] with:
        * header normalization (default: lower_underscore)
        * extra columns under DictReader key None are ignored
        * non-string values coerced to strings
      If 'required' is provided, raises KeyError when columns are missing.
    - has_header=False -> List[List[str]].
    """
    p = _resolve_csv_path(path)
    if not p.exists():
        raise FileNotFoundError(f"CSV not found: {p}")

    with _open_text(p, encoding) as f:
        head = f.read(2048)
        f.seek(0)

        if delimiter is None or quotechar is None:
            dialect = _sniff_dialect(head)
            if delimiter is None:
                delimiter = dialect.delimiter
            if quotechar is None:
                quotechar = dialect.quotechar
            if escapechar is None:
                escapechar = dialect.escapechar

        reader_kwargs = {
            "delimiter": delimiter or ",",
            "quotechar": quotechar or '"',
            "escapechar": escapechar,
            "doublequote": True,
            "skipinitialspace": True,
        }

        if has_header:
            rdr = csv.DictReader(f, **reader_kwargs)

            def _to_str(v):
                if isinstance(v, list):
                    return (delimiter or ",").join(str(x) for x in v)
                if v is None:
                    return ""
                return str(v)

            rows: List[Dict[str, str]] = []
            for row in rdr:
                clean: Dict[str, str] = {}
                for k, v in row.items():
                    if k is None:
                        continue  # DictReader’s bucket for extra cells
                    nk = _norm_header(k, header_normalization)
                    clean[nk] = _to_str(v).strip()
                rows.append(clean)

            if required:
                missing = [c for c in required if c not in rows[0].keys()] if rows else list(required)
                if missing:
                    raise KeyError(f"CSV missing required columns: {missing}")
            return rows

        else:
            rdr = csv.reader(f, **reader_kwargs)
            return [[(col or "").strip() for col in row] for row in rdr]


def rows_to_args(rows: List[Dict[str, str]], *cols: str, require_all: bool = True) -> Iterable[tuple]:
    """
    Convert dict rows to tuple args in fixed column order.
    """
    missing: set[str] = set()
    for r in rows:
        if require_all:
            for c in cols:
                if c not in r:
                    missing.add(c)
        yield tuple(r.get(c, "") for c in cols)
    if require_all and missing:
        raise KeyError(f"CSV missing required columns: {sorted(missing)}")


def params_from_csv(
    path: str | Path,
    columns: Sequence[str],
    **kwargs
) -> List[Tuple]:
    """
    Convenience: read CSV and return list of tuples in the same order as 'columns'.
    Example:
        params_from_csv("data/login.csv", ["email","password"])
    """
    rows = read_csv(path, has_header=True, required=columns, **kwargs)  # rows are dicts
    return list(rows_to_args(rows, *columns, require_all=True))


def count_rows(path: str | Path, **kwargs) -> int:
    data = read_csv(path, **kwargs)
    return len(data)
