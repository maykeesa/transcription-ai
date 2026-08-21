# TODO — transcription-ai

## Interface
- [ ] **Local web UI** (Gradio or Flask):
  - [ ] Field to paste the YouTube link
  - [ ] Real-time progress bar, up to 100% (download + transcription)
  - [ ] Whisper model selector (tiny/base/small/medium/large-v3/turbo)
  - [ ] Output location selector (currently fixed at `transcriptions/`)
  - [ ] Total elapsed time at the end (already available in the terminal)

## Compatibility
- [ ] Support non-NVIDIA GPUs (AMD, Intel Arc, Apple Silicon) — CTranslate2
      exposes only `cpu` and `cuda`, so this means replacing the transcription
      engine with whisper.cpp, which supports ROCm, Vulkan and Metal
- [ ] Lower the process priority automatically, from within the script — `nice`
      on Linux and the equivalent on Windows

## Features
- [ ] Accept local audio and video files, without going through YouTube
- [ ] Skip transcription when the `.txt` already exists (today only the mp3
      download is skipped)
- [ ] Detect the available CPU, GPU/VRAM and RAM and suggest, or pick
      automatically, a compatible model
