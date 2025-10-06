# src/core/video_recorder.py
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import threading
import time
from pathlib import Path
from typing import Optional, Callable

# Optional deps for full-screen fallback
try:
    import mss  # screen capture
    from PIL import Image
except Exception:
    mss = None
    Image = None


class VideoRecorder:
    """
    Robust test video recorder.

    Primary mode (best):  Selenium screenshot provider (exact browser viewport)
      - Call set_screenshot_provider(lambda: driver.get_screenshot_as_png()).
      - Works in headed & headless.
    Fallback mode: MSS full-screen capture (if provider unavailable).

    Behavior:
      - Captures PNG frames at `fps` to a temp folder.
      - On stop(), encodes to MP4 via ffmpeg (H.264, yuv420p).
      - Ensures a playable MP4 even with very few frames (auto-duplicate).
      - .reason() explains why a video wasn't produced if that happens.
    """

    def __init__(self, outfile: Path, fps: int = 10, region: str = "window"):
        self.outfile = Path(outfile)
        self.fps = max(1, int(fps))
        self.region = region  # kept for compatibility; selenium provider ignores it
        self._frames_dir: Optional[Path] = None
        self._thr: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self._frame_count = 0
        self._reason: Optional[str] = None
        self._ffmpeg_exe: Optional[str] = None

        # Screenshot provider (callable -> PNG bytes). If not set, we try MSS.
        self._provider: Optional[Callable[[], bytes]] = None

        # Note: MSS/Pillow are optional now; only required for fallback mode.
        self._mss_ok = bool(mss and Image)

    # ---------------- Public API ----------------

    def set_screenshot_provider(self, provider: Callable[[], bytes]) -> None:
        """
        Register a function that returns PNG bytes (e.g., driver.get_screenshot_as_png).
        Must be set BEFORE start().
        """
        self._provider = provider

    def reason(self) -> Optional[str]:
        return self._reason

    def is_available(self) -> bool:
        """
        We consider recorder 'available' if either a selenium provider is set
        or we can fallback to MSS.
        """
        return bool(self._provider or self._mss_ok)

    # ---------------- Internals ----------------

    @staticmethod
    def _now() -> float:
        return time.perf_counter()

    @staticmethod
    def _sleep_until(target_ts: float) -> None:
        # accurate pacing loop (avoids drift)
        while True:
            now = time.perf_counter()
            diff = target_ts - now
            if diff <= 0:
                return
            # sleep in small chunks near the end for more stable pacing
            time.sleep(min(diff, 0.005))

    @staticmethod
    def _write_png(path: Path, data: bytes) -> None:
        path.write_bytes(data)

    def _resolve_ffmpeg(self) -> Optional[str]:
        cand = shutil.which("ffmpeg")
        if cand:
            return cand
        env_vars = ("FFMPEG", "FFMPEG_BIN", "FFMPEG_PATH", "FFMPEG_CONFIG_PATH")
        for var in env_vars:
            val = os.environ.get(var, "").strip()
            if not val:
                continue
            p = Path(val)
            if p.is_dir():
                exe = p / ("ffmpeg.exe" if os.name == "nt" else "ffmpeg")
                if exe.exists():
                    return str(exe)
            elif p.exists():
                return str(p)
        return None

    def _capture_loop_provider(self) -> None:
        """Capture using the registered selenium provider (preferred)."""
        assert self._frames_dir is not None
        period = 1.0 / float(self.fps)
        next_ts = self._now()
        idx = 0
        while not self._stop.is_set():
            try:
                png = self._provider()  # type: ignore[operator]
                assert isinstance(png, (bytes, bytearray))
                p = self._frames_dir / f"frame_{idx:06d}.png"
                self._write_png(p, png)
                idx += 1
                self._frame_count += 1
            except Exception as e:
                self._reason = f"Selenium screenshot provider failed: {e}"
                break
            next_ts += period
            self._sleep_until(next_ts)

    def _capture_loop_mss(self) -> None:
        """Fallback to full-screen capture via MSS."""
        assert self._frames_dir is not None
        if not self._mss_ok:
            self._reason = "MSS/Pillow not available for fallback capture."
            return

        period = 1.0 / float(self.fps)
        next_ts = self._now()
        idx = 0
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[0]  # desktop capture (reliable on Windows)
                while not self._stop.is_set():
                    try:
                        img = sct.grab(monitor)
                        p = self._frames_dir / f"frame_{idx:06d}.png"
                        Image.frombytes("RGB", img.size, img.rgb).save(p, "PNG")
                        idx += 1
                        self._frame_count += 1
                    except Exception as cap_err:
                        self._reason = f"Screen grab failed: {cap_err}"
                        break
                    next_ts += period
                    self._sleep_until(next_ts)
        except Exception as e:
            self._reason = f"MSS capture crashed: {e}"

    # ---------------- Lifecycle ----------------

    def start(self) -> None:
        """Begin capturing frames in background."""
        # Prepare temp frames dir
        try:
            self._frames_dir = Path(tempfile.mkdtemp(prefix="vidframes_"))
        except Exception as e:
            self._reason = f"Could not create temp frames dir: {e}"
            return

        self._stop.clear()
        self._frame_count = 0

        # Decide capture strategy
        if self._provider:
            target = self._capture_loop_provider
        elif self._mss_ok:
            target = self._capture_loop_mss
        else:
            self._reason = "No capture method available (no selenium provider and MSS/Pillow missing)."
            return

        self._thr = threading.Thread(target=target, name="VideoRecorder", daemon=True)
        self._thr.start()

    def stop(self) -> None:
        """Stop capture and encode frames to MP4."""
        # stop the capture thread
        if self._thr and self._thr.is_alive():
            self._stop.set()
            self._thr.join(timeout=3.0)

        # If no frames dir, nothing to encode
        if not self._frames_dir:
            if not self._reason:
                self._reason = "No frames directory (capture did not start)."
            return

        # Ensure at least a couple of frames so ffmpeg has something usable
        frames = sorted(self._frames_dir.glob("frame_*.png"))
        if len(frames) == 0:
            if not self._reason:
                self._reason = "No frames captured."
        elif len(frames) == 1:
            # Duplicate the single frame to produce a short video
            dup = self._frames_dir / "frame_000001.png"
            try:
                shutil.copy(frames[0], dup)
            except Exception:
                pass

        # Encode
        frames_exist = any(self._frames_dir.glob("frame_*.png"))
        if frames_exist:
            self._ffmpeg_exe = self._resolve_ffmpeg()
            if not self._ffmpeg_exe:
                self._reason = "FFmpeg not found on PATH or via configured path."
            else:
                try:
                    self.outfile.parent.mkdir(parents=True, exist_ok=True)
                    # Encode with H.264 for compatibility. Keep it quick but clear.
                    cmd = [
                        self._ffmpeg_exe,
                        "-loglevel", "error",
                        "-y",
                        "-framerate", str(self.fps),
                        "-i", str(self._frames_dir / "frame_%06d.png"),
                        "-c:v", "libx264",
                        "-preset", "veryfast",
                        "-crf", "23",
                        "-pix_fmt", "yuv420p",
                        "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
                        str(self.outfile),
                    ]
                    proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=False)
                    if proc.returncode != 0:
                        self._reason = f"FFmpeg exited with code {proc.returncode}: {proc.stderr.decode(errors='ignore')[:200]}"
                    elif not self.outfile.exists():
                        self._reason = "FFmpeg reported success but MP4 not found."
                except Exception as e:
                    self._reason = f"FFmpeg encoding error: {e}"

        # cleanup raw frames
        try:
            if self._frames_dir and self._frames_dir.exists():
                shutil.rmtree(self._frames_dir, ignore_errors=True)
        finally:
            self._frames_dir = None
