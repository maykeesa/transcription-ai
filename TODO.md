# TODO — transcription-ai

## Interface
- [ ] **UI web local** (Gradio ou Flask):
  - [ ] Campo para colar o link do YouTube
  - [ ] Barra de progresso em tempo real, até 100% (download + transcrição)
  - [ ] Seletor do modelo Whisper (tiny/base/small/medium/large-v3/turbo)
  - [ ] Seletor do local de saída (hoje fixo em `transcriptions/`)
  - [ ] Duração total ao final (já existe no terminal)

## Compatibilidade
- [ ] Suporte a GPUs não-NVIDIA (AMD, Intel Arc, Apple Silicon) — o CTranslate2
      aceita apenas `cpu` e `cuda`, então exige trocar a engine de transcrição
      por whisper.cpp, que suporta ROCm, Vulkan e Metal
- [ ] Rodar com prioridade baixa automaticamente, de dentro do script — `nice` no
      Linux e equivalente no Windows

## Funcionalidades
- [ ] Suporte a arquivo de áudio/vídeo local, sem YouTube
- [ ] Pular a transcrição se o `.txt` já existir (hoje só pula o download do mp3)
- [ ] Detectar CPU, GPU/VRAM e RAM disponíveis e sugerir ou escolher sozinho o
      modelo compatível
