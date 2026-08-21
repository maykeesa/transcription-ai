<p align="center">
  <img src="assets/logo.png" width="160" alt="TranscriptionAI logo"/>
</p>

<h1 align="center">TranscriptionAI</h1>

<p align="center">
A command-line tool that transcribes YouTube videos automatically: you pass just the video URL and it downloads the audio as mp3 (yt-dlp), transcribes it with AI running fully on your machine (Whisper, GPU-accelerated with a CPU fallback) and keeps everything tidy: each video becomes a subfolder holding its <code>.mp3</code> and the <code>.txt</code> transcript, with per-step progress bars and timings right in the terminal.
</p>

<br>

## ✨ Features

* Fully local transcription, nothing is sent to external servers
* GPU acceleration (NVIDIA/CUDA) with an automatic CPU fallback
* Progress bars per step (download and transcription) and total time at the end
* Automatic language detection (or forced with `-l pt`)
* 6 Whisper models to choose from, from the fastest to the most accurate
* Automatic retry on temporary download failures
* Detailed logs of every run saved to `logs/`

<br>

## 📦 Dependencies

| Dependency | What for |
|---|---|
| [Python 3.12+](https://www.python.org/downloads/) | Running the project |
| [ffmpeg](https://ffmpeg.org/) | Converting the audio to mp3 |
| [Node.js](https://nodejs.org/) | JS runtime yt-dlp needs for YouTube |

Python libraries (installed from `requirements.txt`):

* **yt-dlp**: downloads the audio from the videos
* **faster-whisper**: transcription with the optimized Whisper model
* **rich**: progress bars and terminal interface
* **nvidia-cublas-cu12 / nvidia-cudnn-cu12 / nvidia-cuda-runtime-cu12**: CUDA libraries for GPU support (optional; without a GPU the script uses the CPU)

<br>

## 🚀 Installing

**Linux**

```bash
# 1. System dependencies
sudo apt install ffmpeg nodejs

# 2. Clone the repository
git clone https://github.com/MaykeESA/transcription-ai.git
cd transcription-ai

# 3. Create the virtual environment and install the libraries
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

**Windows**

```powershell
# 1. System dependencies
winget install ffmpeg
winget install OpenJS.NodeJS.LTS

# 2. Clone the repository
git clone https://github.com/MaykeESA/transcription-ai.git
cd transcription-ai

# 3. Create the virtual environment and install the libraries
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

> Calling the venv interpreter by its path means you never have to activate the environment. If you prefer activating it to shorten the commands, use `source .venv/bin/activate` on Linux or `.venv\Scripts\Activate.ps1` on PowerShell, the latter requiring you to allow scripts once with `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

<br>

## 💻 Usage

**Linux**

```bash
# Basic: just pass the URL (language is detected automatically)
.venv/bin/python transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Forcing Portuguese
.venv/bin/python transcribe.py "URL" -l pt

# More accurate model
.venv/bin/python transcribe.py "URL" -m medium -l pt

# Long videos: low priority, the machine stays responsive
nice -n 19 .venv/bin/python transcribe.py "URL" -l pt
```

**Windows**

```powershell
# Basic: just pass the URL (language is detected automatically)
.venv\Scripts\python.exe transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Forcing Portuguese
.venv\Scripts\python.exe transcribe.py "URL" -l pt

# More accurate model
.venv\Scripts\python.exe transcribe.py "URL" -m medium -l pt

# Networks where IPv6 is broken
.venv\Scripts\python.exe transcribe.py "URL" -l pt --force-ipv4
```

The result lands in `transcriptions/<video title>/`, with the `.mp3` and the `.txt` side by side.

Every option: `transcribe.py --help`

| Model (`-m`) | Speed | Accuracy |
|---|---|---|
| `tiny` / `base` | very fast | basic |
| `small` *(default)* | fast | good |
| `medium` | slower | great |
| `large-v3` / `turbo` | slow / fast | excellent (wants a strong GPU) |

<br>

## 📄 Copyright and license

Code and documentation copyright 2026 [Mayke Erick](https://github.com/MaykeESA). Code released under the [MIT License](LICENSE).
