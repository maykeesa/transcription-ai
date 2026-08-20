import argparse
import sys
import time
from pathlib import Path

from rich.console import Console
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn, TimeRemainingColumn

from core.downloader import DownloadError, YtdlpLogBuffer, download_mp3_with_retry
from core.network import force_ipv4
from core.transcriber import MODEL_CHOICES, transcribe_audio

PROJECT_DIR = Path(__file__).parent
OUTPUT_DIR = PROJECT_DIR / "transcriptions"
LOGS_DIR = PROJECT_DIR / "logs"

console = Console()


def _new_progress() -> Progress:
    return Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,
    )


def _run_download(url: str, log_buffer: YtdlpLogBuffer) -> Path:
    progress = _new_progress()
    task_id = None

    def hook(event: dict) -> None:
        nonlocal task_id
        if event["status"] == "downloading":
            total = event.get("total_bytes") or event.get("total_bytes_estimate")
            if total:
                if task_id is None:
                    task_id = progress.add_task("Downloading audio", total=total)
                progress.update(task_id, completed=event.get("downloaded_bytes", 0), total=total)
        elif event["status"] == "finished" and task_id is not None:
            progress.update(task_id, completed=progress.tasks[task_id].total or 0)
            progress.console.print("Converting to mp3...")

    def on_retry(attempt: int, attempts: int) -> None:
        progress.console.print(f"[yellow]Download failed (attempt {attempt}/{attempts}), retrying...[/]")

    with progress:
        return download_mp3_with_retry(url, OUTPUT_DIR, log_buffer, hook, on_retry)


def _run_transcription(mp3_path: Path, model_name: str, language: str | None) -> Path:
    console.print(f"Loading Whisper model '{model_name}'...")
    progress = _new_progress()
    task_id = None

    def on_progress(done: float, total: float) -> None:
        nonlocal task_id
        if task_id is None:
            task_id = progress.add_task("Transcribing", total=total)
        progress.update(task_id, completed=done)

    def on_status(message: str) -> None:
        progress.console.print(f"[yellow]{message}[/]")

    with progress:
        return transcribe_audio(mp3_path, model_name, language, on_status, on_progress)


def format_elapsed(seconds: float) -> str:
    minutes, secs = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m {secs}s"
    if minutes:
        return f"{minutes}m {secs}s"
    return f"{secs}s"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Transcribe YouTube videos with yt-dlp + Whisper.\n"
        "Downloads the audio as mp3 and writes the transcript next to it,\n"
        "both inside transcriptions/<video title>/.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "models (--model):\n"
            "  tiny, base   fastest, lower accuracy\n"
            "  small        good balance (default)\n"
            "  medium       more accurate, slower, bigger download\n"
            "  large-v3     best accuracy, needs a strong GPU\n"
            "  turbo        near large-v3 accuracy, much faster\n"
            "\n"
        ),
    )
    parser.add_argument("url", help="YouTube video URL (wrap it in quotes)")
    parser.add_argument(
        "-m",
        "--model",
        default="small",
        choices=MODEL_CHOICES,
        metavar="MODEL",
        help=f"Whisper model: {', '.join(MODEL_CHOICES)} (default: small)",
    )
    parser.add_argument(
        "-l",
        "--language",
        default=None,
        metavar="LANG",
        help="language code, e.g. pt, en (default: auto-detect)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="stream yt-dlp logs live instead of only writing them to the log file",
    )
    parser.add_argument(
        "--force-ipv4",
        action="store_true",
        help="force IPv4 connections, useful when IPv6 is broken on your network (e.g. some Wi-Fi networks)",
    )
    args = parser.parse_args()
    url = args.url.replace("\\", "")

    if args.force_ipv4:
        force_ipv4()
    echo = (lambda line: console.print(f"[dim]{line}[/]", highlight=False)) if args.verbose else None
    log_buffer = YtdlpLogBuffer(echo=echo)
    started = time.monotonic()

    console.rule("[bold]Step 1/2 · Download (yt-dlp)")
    try:
        mp3_path = _run_download(url, log_buffer)
    except DownloadError as error:
        console.print(f"[red]Video download failed: {error}[/]")
        console.print(f"[dim]Full yt-dlp log: {log_buffer.dump(LOGS_DIR)}[/]")
        sys.exit(1)

    download_elapsed = time.monotonic() - started
    console.print(f"[green]✓[/] Audio saved: {mp3_path} [dim]({format_elapsed(download_elapsed)})[/]")

    console.rule("[bold]Step 2/2 · Transcription (faster-whisper)")
    transcription_started = time.monotonic()
    txt_path = _run_transcription(mp3_path, args.model, args.language)
    transcription_elapsed = time.monotonic() - transcription_started
    console.print(f"[green]✓[/] Transcript saved: {txt_path} [dim]({format_elapsed(transcription_elapsed)})[/]")

    console.rule()
    total_elapsed = time.monotonic() - started
    console.print(
        f"[bold green]Done in {format_elapsed(total_elapsed)}[/] — "
        f"download {format_elapsed(download_elapsed)}, transcription {format_elapsed(transcription_elapsed)}"
    )
    console.print(f"[dim]Detailed yt-dlp log: {log_buffer.dump(LOGS_DIR)}[/]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled by user[/]")
        sys.exit(130)
