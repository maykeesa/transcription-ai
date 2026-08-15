# TODO — transcription-ia

## Prioridade
- [ ] **Escolha de IPv4/IPv6**: opção `--ipv6` (ou detecção automática testando a conexão) em vez do IPv4 forçado no código — hoje o script assume que IPv6 está quebrado nesta rede
- [ ] **UI simples** (web local, ex.: Gradio ou Flask):
  - [ ] Campo para colar o link do YouTube
  - [ ] Barra de progresso em tempo real até 100% (download + transcrição)
  - [ ] Seletor do local de output (hoje fixo em `transcriptions/`)
  - [ ] Seletor do modelo Whisper (tiny/base/small/medium/large-v3/turbo)
- [ ] **Tempo na UI**: mostrar duração total também na futura UI web (no terminal já feito)
- [ ] Pular transcrição se o `.txt` já existir (hoje só pula o download do mp3)
- [ ] Rodar com prioridade baixa (`nice`) automaticamente de dentro do script, vê solução para o windows
- [ ] Detectar CPU, GPU/VRAM e RAM disponível e sugerir/escolher o modelo compatível sozinho
- [ ] Suporte a arquivo de áudio/vídeo local (sem YouTube)
