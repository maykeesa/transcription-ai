# TODO — transcription-ia

## Prioridade
- [ ] **Escolha de IPv4/IPv6**: opção `--ipv6` (ou detecção automática testando a conexão) em vez do IPv4 forçado no código — hoje o script assume que IPv6 está quebrado nesta rede
- [ ] **UI simples** (web local, ex.: Gradio ou Flask):
  - [ ] Campo para colar o link do YouTube
  - [ ] Barra de progresso em tempo real até 100% (download + transcrição)
  - [ ] Seletor do local de output (hoje fixo em `transcriptions/`)
  - [ ] Seletor do modelo Whisper (tiny/base/small/medium/large-v3/turbo)
- [x] **`cpu_threads` automático**: calcular a partir de `os.cpu_count()` (ex.: metade dos núcleos) em vez do valor fixo 6
- [ ] **Tempo na UI**: mostrar duração total também na futura UI web (no terminal já feito)
- [x] **Tempo**: duração de todo o processo no final do terminal (por etapa e total)
- [x] **Melhoria de UI do terminal**: etapas separadas (yt-dlp e whisper) com barras de progresso via `rich`; logs detalhados ficam "recolhidos" num arquivo em `logs/` (mostrado no final) e `--verbose` expande tudo ao vivo
- [x] **Código e mensagens em inglês** (script renomeado para `transcribe.py`; apenas o TODO fica em português)

## Outras ideias
- [ ] Gerar `.srt`/`.vtt` com timestamps além do `.txt`
- [ ] Fila de vídeos: aceitar várias URLs ou playlist inteira de uma vez
- [ ] Pular transcrição se o `.txt` já existir (hoje só pula o download do mp3)
- [ ] Rodar com prioridade baixa (`nice`) automaticamente de dentro do script
- [ ] Detectar VRAM disponível e sugerir/escolher o modelo compatível sozinho
- [ ] Suporte a arquivo de áudio/vídeo local (sem YouTube)
- [ ] `HF_TOKEN` opcional para downloads de modelo mais rápidos
