# Whisper-Speech-Recognition
This project utilizes OpenAI's Whisper, a cutting-edge automatic speech recognition (ASR) system, to transcribe speech from audio files. It provides a simple and efficient way to convert spoken language into text, opening up possibilities for various applications like voice assistants, transcription services, and more.


### Como usar

```
# 1. Instale as dependências
pip install -r requirements.txt

# 2. Execute a transcrição
python main.py caminho/do/audio.mp3 --format txt

# Exemplos de uso:
python main.py audio/entrevista.mp3  # Saída em texto
python main.py audio/palestra.wav --format srt  # Gera legendas
python main.py audio/podcast.mp3 --format json --output ./transcricoes/
```

### Recursos Avançados

- Normalização automática do volume do áudio
- Detecção de idioma (configurado para português)
- Geração de legendas sincronizadas
- Metadados completos da transcrição
- Suporte a processamento em GPU
