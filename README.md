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
* **nvidia-cublas-cu12 / nvidia-cudnn-cu12**: bibliotecas CUDA para usar a GPU (opcional; sem GPU o script usa a CPU)

<br>

## 🚀 Como instalar

```bash
# 1. Clone o repositório
git clone https://github.com/MaykeESA/transcription-ia.git
cd transcription-ia

# 2. Crie um ambiente virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate

# 3. Instale as dependências Python
pip install -r requirements.txt
```

> No Windows, instale o ffmpeg e o Node com `winget install ffmpeg` e `winget install OpenJS.NodeJS.LTS`, e ative o venv com `.venv\Scripts\activate`.

<br>

## 💻 Como usar

```bash
# Básico: só passar a URL (idioma detectado automaticamente)
python3 transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Forçando português
python3 transcribe.py "URL" -l pt

# Modelo mais preciso
python3 transcribe.py "URL" -m medium -l pt

# Vídeos longos: prioridade baixa, PC continua responsivo
nice -n 19 python3 transcribe.py "URL" -l pt
```

O resultado fica em `transcriptions/<título do vídeo>/` com o `.mp3` e o `.txt` juntos.

Todas as opções: `python3 transcribe.py --help`

| Modelo (`-m`) | Velocidade | Precisão |
|---|---|---|
| `tiny` / `base` | muito rápido | básica |
| `small` *(padrão)* | rápido | boa |
| `medium` | mais lento | ótima |
| `large-v3` / `turbo` | lento / rápido | excelente (pede GPU forte) |

<br>

## 🤝 Colaboradores

Agradecemos às seguintes pessoas que contribuíram para este projeto:

<table>
  <tr>
    <td align="center">
      <a href="#">
        <a href="https://github.com/MaykeESA">
          <img src="https://avatars.githubusercontent.com/u/81484737?v=4" width="100px;" alt="Foto do Mayke Erick no GitHub"/><br>
        </a>
        <sub>
          <b>Mayke Erick</b>
        </sub>
      </a>
    </td>
  </tr>
</table>
