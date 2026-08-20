import time
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

import yt_dlp

DOWNLOAD_ATTEMPTS = 3
RETRY_WAIT_SECONDS = 10
MP3_QUALITY = "192"
TRANSIENT_ERROR_MARKERS = (
    "403",
    "timed out",
    "timeout",
    "connection",
    "temporary",
    "requested format is not available",
)

DownloadError = yt_dlp.utils.DownloadError


class YtdlpLogBuffer:
    def __init__(self, echo: Callable[[str], None] | None = None) -> None:
        self.lines: list[str] = []
        self.echo = echo

    def _log(self, level: str, message: str) -> None:
        self.lines.append(f"[{level}] {message}")
        if self.echo:
            self.echo(message)

    def debug(self, message: str) -> None:
        self._log("debug", message)

    def info(self, message: str) -> None:
        self._log("info", message)

    def warning(self, message: str) -> None:
        self._log("warning", message)

    def error(self, message: str) -> None:
        self._log("error", message)

    def dump(self, logs_dir: Path) -> Path:
        logs_dir.mkdir(exist_ok=True)
        log_path = logs_dir / f"run-{datetime.now():%Y%m%d-%H%M%S}.log"
        log_path.write_text("\n".join(self.lines) + "\n", encoding="utf-8")
        return log_path


def download_mp3(
    url: str,
    output_dir: Path,
    log_buffer: YtdlpLogBuffer | None = None,
    progress_hook: Callable[[dict], None] | None = None,
    force_ipv4: bool = False,
) -> Path:
    options = {
        "quiet": True,
        "noprogress": True,
        "js_runtimes": {"node": {}},
        "remote_components": ["ejs:github"],
        "extractor_args": {"youtube": {"player_client": ["default", "-android_vr"]}},
        "noplaylist": True,
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / "%(title)s" / "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": MP3_QUALITY,
            }
        ],
    }
    if force_ipv4:
        options["source_address"] = "0.0.0.0"
    if log_buffer is not None:
        options["logger"] = log_buffer
    if progress_hook is not None:
        options["progress_hooks"] = [progress_hook]

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
        mp3_path = Path(ydl.prepare_filename(info)).with_suffix(".mp3")

        if mp3_path.exists():
            return mp3_path

        ydl.process_ie_result(info, download=True)

    if not mp3_path.exists():
        raise DownloadError(f"No video was downloaded — check that the URL points to a valid video: {url}")

    return mp3_path


def download_mp3_with_retry(
    url: str,
    output_dir: Path,
    log_buffer: YtdlpLogBuffer | None = None,
    progress_hook: Callable[[dict], None] | None = None,
    on_retry: Callable[[int, int], None] | None = None,
    force_ipv4: bool = False,
) -> Path:
    for attempt in range(1, DOWNLOAD_ATTEMPTS + 1):
        try:
            return download_mp3(url, output_dir, log_buffer, progress_hook, force_ipv4)
        except DownloadError as error:
            transient = any(marker in str(error).lower() for marker in TRANSIENT_ERROR_MARKERS)
            if not transient or attempt == DOWNLOAD_ATTEMPTS:
                raise
            if on_retry:
                on_retry(attempt, DOWNLOAD_ATTEMPTS)
            time.sleep(RETRY_WAIT_SECONDS)
    raise AssertionError("unreachable")
