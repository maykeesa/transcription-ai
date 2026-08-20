import os
import platform
from collections.abc import Callable, Iterable
from pathlib import Path

from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment, TranscriptionInfo

CPU_THREADS = max(1, (os.cpu_count() or 8) // 2)

MODEL_CHOICES = ["tiny", "base", "small", "medium", "large-v3", "turbo"]


WINDOWS_CUDA_LIBS = (
    ("cuda_runtime", "cudart64_12.dll"),
    ("cublas", "cublasLt64_12.dll"),
    ("cublas", "cublas64_12.dll"),
    ("cudnn", "cudnn64_9.dll"),
)

LINUX_CUDA_LIBS = (
    ("cublas", "libcublas.so.12"),
    ("cudnn", "libcudnn.so.9"),
)


def _load_cuda_libs() -> None:
    import ctypes
    import importlib.util

    spec = importlib.util.find_spec("nvidia")
    if spec is None or not spec.submodule_search_locations:
        return
    base = Path(list(spec.submodule_search_locations)[0])

    if platform.system() == "Windows":
        for package, name in WINDOWS_CUDA_LIBS:
            lib = base / package / "bin" / name
            if lib.exists():
                try:
                    ctypes.WinDLL(str(lib))
                except OSError:
                    pass
        return

    for package, name in LINUX_CUDA_LIBS:
        lib = base / package / "lib" / name
        if lib.exists():
            try:
                ctypes.CDLL(str(lib), mode=ctypes.RTLD_GLOBAL)
            except OSError:
                pass


def _write_transcript(
    segments: Iterable[Segment],
    info: TranscriptionInfo,
    txt_path: Path,
    on_progress: Callable[[float, float], None] | None = None,
) -> None:
    tmp_path = txt_path.with_suffix(txt_path.suffix + ".tmp")
    duration = info.duration or 0.0

    try:
        with tmp_path.open("w", encoding="utf-8") as file:
            for segment in segments:
                file.write(segment.text.strip() + "\n")
                if duration > 0 and on_progress:
                    on_progress(min(segment.end, duration), duration)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise
    if duration > 0 and on_progress:
        on_progress(duration, duration)

    os.replace(tmp_path, txt_path)


def transcribe_audio(
    mp3_path: Path,
    model_name: str,
    language: str | None = None,
    on_status: Callable[[str], None] | None = None,
    on_progress: Callable[[float, float], None] | None = None,
) -> Path:
    txt_path = mp3_path.with_suffix(".txt")

    _load_cuda_libs()
    try:
        model = WhisperModel(model_name, device="cuda", compute_type="int8_float16")
        segments, info = model.transcribe(str(mp3_path), language=language)
    except (RuntimeError, OSError) as error:
        if on_status:
            on_status(f"GPU unavailable ({error}); falling back to CPU with {CPU_THREADS} threads")
        model = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=CPU_THREADS)
        segments, info = model.transcribe(str(mp3_path), language=language)

    _write_transcript(segments, info, txt_path, on_progress)
    return txt_path
