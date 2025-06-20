# 🎵 LyricSync Designer

Um aplicativo web completo criado totalmente com diversas inteligencias artificiais em confluencia para sincronização automática de legendas com música usando IA. Extraia letras de músicas, sincronize automaticamente com o áudio e exporte vídeos com legendas personalizadas.

## IAs utilizadas para criação
- **Claude.ai**: Criação do front-end e back-end
- **ChatGPT.com**: Integração do front-end com o back-end, correção de erros, bugs e conflitos de dependências.

## ✨ Funcionalidades

- **🎤 Transcrição Automática**: Utiliza Whisper AI para extrair letras de qualquer arquivo de áudio
- **🎯 Separação de Vocals**: Usa Demucs para isolar a voz da música, melhorando a precisão da transcrição
- **⏰ Sincronização Precisa**: Timestamps automáticos para cada linha da letra
- **🎨 Editor Visual**: Interface intuitiva para editar letras e estilos
- **📊 Visualização de Waveform**: Navegação visual pelo áudio
- **🎬 Exportação de Vídeo**: Gera vídeos com legendas estilizadas
- **💾 Exportação SRT**: Salva legendas no formato padrão SRT
- **🎭 Estilos Customizáveis**: Múltiplos estilos visuais (Clean, Neon, Shadow, Bold, Minimal)

## 🛠️ Tecnologias Utilizadas

### Backend (Python/Flask)
- **Flask**: Framework web
- **Whisper**: Transcrição de áudio por IA
- **Demucs**: Separação de fontes de áudio
- **LibROSA**: Processamento de áudio
- **MoviePy**: Manipulação de vídeo
- **Pydub**: Processamento de áudio

### Frontend (HTML/CSS/JavaScript)
- **Vanilla JavaScript**: Interface interativa
- **Canvas API**: Visualização de waveform
- **Web Audio API**: Reprodução de áudio
- **CSS Grid/Flexbox**: Layout responsivo
- **Drag & Drop API**: Upload de arquivos

## 📋 Pré-requisitos

- Python 3.10+
- FFmpeg
- Dependências Python (ver requirements.txt)

## 🔧 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seuusuario/lyricsync-designer.git
cd lyricsync-designer
```

2. **Instale as dependências Python**
```bash
pip install -r requirements.txt
```

3. **Instale o FFmpeg**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Baixe do [site oficial do FFmpeg](https://ffmpeg.org/download.html)

4. **Instale o Demucs**
```bash
pip install demucs
```

## 🚀 Como Usar

1. **Inicie o servidor**
```bash
python app.py
```

2. **Abra o index.html no navegador**
```
lyricsync-designer/index.html
```

3. **Upload do arquivo**
   - Arraste e solte ou clique para selecionar
   - Suporta: MP3, WAV, MP4, M4A, OGG

4. **Transcrição**
   - Clique em "🎤 Transcrever"
   - Aguarde o processamento (isolamento de vocals + transcrição)

5. **Edição**
   - Edite as letras no painel direito
   - Ajuste estilos visuais
   - Visualize em tempo real

6. **Exportação**
   - **🎬 Exportar Vídeo**: Gera MP4 com legendas
   - **💾 Exportar SRT**: Salva arquivo de legendas

## 📁 Estrutura do Projeto

```
lyricsync-designer/
├── app.py                 # Backend Flask
├── index.html            # Frontend principal
├── uploads/              # Arquivos enviados
├── output/               # Arquivos gerados
├── requirements.txt      # Dependências Python
└── README.md            # Este arquivo
```

## 🎯 Endpoints da API

### Upload de Arquivo
```http
POST /upload
Content-Type: multipart/form-data
```

### Obter Waveform
```http
GET /waveform/<file_id>
```

### Transcrever Áudio
```http
POST /transcribe/<file_id>
```

### Exportar SRT
```http
POST /export/srt
Content-Type: application/json
```

### Servir Áudio
```http
GET /audio/<file_id>
```

## 🎨 Estilos Disponíveis

- **Clean**: Estilo minimalista e limpo
- **Neon**: Efeito de brilho neon
- **Shadow**: Sombra pronunciada
- **Bold**: Texto em negrito e maiúsculo
- **Minimal**: Estilo sutil e elegante

## ⚙️ Configurações

### Modelo Whisper
Por padrão usa o modelo "medium". Para alterar:
```python
whisper_model = whisper.load_model("large")  # Mais preciso, mais lento
whisper_model = whisper.load_model("small")  # Mais rápido, menos preciso
```

### Qualidade do Demucs
```python
# Para melhor qualidade (mais lento)
'demucs', '--two-stems', 'vocals', '--shifts', '1'
```

## OBSERVAÇÕES IMPORTANTES
1. Funcionalidade de exportação ainda em desenvolvimento
2. Caso Utilizar:
   ```python
   whisper_model = whisper.load_model("large")
   ```
   Poderá causar lentidão em seu dispositivo.
3. Aplicação ainda em desenvolvimento aberto a contribuições.

## 🤝 Contribuindo

1. Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 🐛 Problemas Conhecidos

- Transcrição pode ser menos precisa em músicas com muito instrumental
- Processamento pode ser lento em arquivos grandes
- Requer conexão com internet para download inicial dos modelos

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [OpenAI Whisper](https://github.com/openai/whisper) - Transcrição de áudio
- [Facebook Demucs](https://github.com/facebookresearch/demucs) - Separação de fontes
- [LibROSA](https://librosa.org/) - Processamento de áudio
- [MoviePy](https://zulko.github.io/moviepy/) - Manipulação de vídeo

## 📞 Contato

Estevão Amaro - stvviking@gmail.com

Link do Projeto: [https://github.com/Steve09012004/ia-LyricSync_Designer](https://github.com/Steve09012004/ia-LyricSync_Designer)

---

⭐ Se este projeto te ajudou, considere dar uma estrela!
