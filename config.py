# config.py
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do projeto
class Config:
    # Diretórios do projeto
    BASE_DIR = Path(__file__).parent
    AUDIO_DIR = BASE_DIR / "audio"
    OUTPUT_DIR = BASE_DIR / "transcricoes"
    
    # Configurações do Whisper
    WHISPER_MODEL = "medium"  # Opções: tiny, base, small, medium, large
    LANGUAGE = "pt"  # Código do idioma para português
    
    # Formatos de áudio suportados
    SUPPORTED_FORMATS = ['.mp3', '.wav', '.m4a', '.ogg']
    
    # Configurações de saída
    EXPORT_FORMATS = ['txt', 'json', 'srt']
    
    def __init__(self):
        # Cria diretórios necessários
        self.AUDIO_DIR.mkdir(exist_ok=True)
        self.OUTPUT_DIR.mkdir(exist_ok=True)
