# src/core/logger.py
from __future__ import annotations
import logging
from logging import Logger
from logging.handlers import MemoryHandler
from pathlib import Path
from typing import Optional

try:
    from colorlog import ColoredFormatter
except Exception:
    ColoredFormatter = None  # graceful fallback if colorlog is missing

_DEFAULT_FMT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DEFAULT_DATEFMT = "%H:%M:%S"

def _make_console_handler(level: int) -> logging.Handler:
    ch = logging.StreamHandler()
    ch.setLevel(level)
    if ColoredFormatter:
        fmt = ColoredFormatter(
            "%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt=_DEFAULT_DATEFMT,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "white",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
        ch.setFormatter(fmt)
    else:
        fmt = logging.Formatter(_DEFAULT_FMT, datefmt=_DEFAULT_DATEFMT)
        ch.setFormatter(fmt)
    return ch

def _make_file_handler(log_path: Path, level: int) -> logging.Handler:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(level)
    fmt = logging.Formatter(_DEFAULT_FMT, datefmt=_DEFAULT_DATEFMT)
    fh.setFormatter(fmt)
    return fh

def get_buffered_logger(
    name: str = "tests",
    level: int = logging.INFO,
    capacity: int = 10000,  # number of records to buffer
) -> tuple[Logger, MemoryHandler]:
    """
    Returns (logger, memory_handler).
    - Exactly one console handler (colored if available).
    - Memory buffer is attached per-test; on fail we materialize to file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    # Ensure exactly one console handler across the run
    if not any(isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
               for h in logger.handlers):
        logger.addHandler(_make_console_handler(level))

    # Fresh memory handler per call
    mem = MemoryHandler(capacity=capacity, flushLevel=logging.CRITICAL + 1, target=None)
    mem.setLevel(level)
    logger.addHandler(mem)
    return logger, mem

def materialize_log_to_file(logger: Logger, mem: MemoryHandler, log_path: Path, level: int = logging.INFO) -> None:
    """
    Create a file handler, set as target for memory buffer, flush records to it,
    and keep the file handler attached for any further test teardown logs.
    """
    fh = _make_file_handler(log_path, level)
    mem.setTarget(fh)
    mem.flush()
    logger.addHandler(fh)

def drop_memory_handler(logger: Logger, mem: MemoryHandler) -> None:
    """
    Detach and close the memory handler (used on PASS).
    """
    try:
        mem.flush()
        logger.removeHandler(mem)
        mem.close()
    except Exception:
        pass
