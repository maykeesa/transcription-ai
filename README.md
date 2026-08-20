<p align="center">
  <img src="assets/logo.png" width="160" alt="Logo do TranscriptionIA"/>
</p>

<h1 align="center">TranscriptionIA</h1>

<p align="center">
É uma ferramenta de linha de comando que transcreve vídeos do YouTube automaticamente: você passa apenas a URL do vídeo e ela baixa o áudio em mp3 (yt-dlp), transcreve com IA rodando 100% local (Whisper, com aceleração por GPU e fallback para CPU) e organiza tudo em pastas: cada vídeo vira uma subpasta com o <code>.mp3</code> e o <code>.txt</code> da transcrição, com barras de progresso e tempo de cada etapa direto no terminal.
</p>

<br>

## ✨ Funcionalidades

* Transcrição 100% local, nada é enviado para servidores externos
* Aceleração por GPU (NVIDIA/CUDA) com fallback automático para CPU
* Barras de progresso por etapa (download e transcrição) e tempo total ao final
* Detecção automática de idioma (ou forçado com `-l pt`)
* 6 modelos Whisper à escolha, do mais rápido ao mais preciso
* Retry automático em falhas temporárias de download
* Logs detalhados de cada execução salvos em `logs/`

<br>

## 📦 Dependências

| Dependência | Para quê | Instalação |
|---|---|---|
| [Python 3.12+](https://www.python.org/downloads/) | Rodar o projeto | `sudo apt install python3` |
| [ffmpeg](https://ffmpeg.org/) | Converter o áudio para mp3 | `sudo apt install ffmpeg` |
| [Node.js](https://nodejs.org/) | Runtime JS exigido pelo yt-dlp para o YouTube | `sudo apt install nodejs` |

Bibliotecas Python (instaladas via `requirements.txt`):

* **yt-dlp**: download do áudio dos vídeos
* **faster-whisper**: transcrição com o modelo Whisper otimizado
* **rich**: barras de progresso e interface do terminal
* **nvidia-cublas-cu12 / nvidia-cudnn-cu12 / nvidia-cuda-runtime-cu12**: bibliotecas CUDA para usar a GPU (opcional; sem GPU o script usa a CPU)

<br>

## 🚀 Como instalar

**Linux**

```bash
# 1. Dependências do sistema
sudo apt install ffmpeg nodejs

# 2. Clone o repositório
git clone https://github.com/MaykeESA/transcription-ia.git
cd transcription-ia

# 3. Crie o ambiente virtual e instale as bibliotecas
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

**Windows**

```powershell
# 1. Dependências do sistema
winget install ffmpeg
winget install OpenJS.NodeJS.LTS

# 2. Clone o repositório
git clone https://github.com/MaykeESA/transcription-ia.git
cd transcription-ia

# 3. Crie o ambiente virtual e instale as bibliotecas
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

> Chamar o interpretador do venv pelo caminho dispensa ativar o ambiente. Se preferir ativar para encurtar os comandos, use `source .venv/bin/activate` no Linux ou `.venv\Scripts\Activate.ps1` no PowerShell, este último exige liberar scripts uma vez com `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

<br>

## 💻 Como usar

**Linux**

```bash
# Básico: só passar a URL (idioma detectado automaticamente)
.venv/bin/python transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Forçando português
.venv/bin/python transcribe.py "URL" -l pt

# Modelo mais preciso
.venv/bin/python transcribe.py "URL" -m medium -l pt

# Vídeos longos: prioridade baixa, PC continua responsivo
nice -n 19 .venv/bin/python transcribe.py "URL" -l pt
```

**Windows**

```powershell
# Básico: só passar a URL (idioma detectado automaticamente)
.venv\Scripts\python.exe transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Forçando português
.venv\Scripts\python.exe transcribe.py "URL" -l pt

# Modelo mais preciso
.venv\Scripts\python.exe transcribe.py "URL" -m medium -l pt

# Redes onde o IPv6 está quebrado
.venv\Scripts\python.exe transcribe.py "URL" -l pt --force-ipv4
```

O resultado fica em `transcriptions/<título do vídeo>/` com o `.mp3` e o `.txt` juntos.

Todas as opções: `transcribe.py --help`

| Modelo (`-m`) | Velocidade | Precisão |
|---|---|---|
| `tiny` / `base` | muito rápido | básica |
| `small` *(padrão)* | rápido | boa |
| `medium` | mais lento | ótima |
| `large-v3` / `turbo` | lento / rápido | excelente (pede GPU forte) |

<br>

## 📄 Licença

Distribuído sob a licença [MIT](LICENSE): uso livre, inclusive comercial, desde que o aviso de copyright seja mantido. O software é fornecido sem garantias.