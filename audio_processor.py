# audio_processor.py
from pydub import AudioSegment
import whisper
import json
from datetime import datetime
from pathlib import Path
import torch
from typing import Union, Dict, List
from config import Config

class AudioProcessor:
    """Classe para processar arquivos de áudio e realizar transcrição"""
    
    def __init__(self, config: Config):
        self.config = config
        self.model = whisper.load_model(config.WHISPER_MODEL)
        
    def load_audio(self, audio_path: Union[str, Path]) -> AudioSegment:
        """Carrega e normaliza o arquivo de áudio"""
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {audio_path}")
            
        if audio_path.suffix not in self.config.SUPPORTED_FORMATS:
            raise ValueError(f"Formato não suportado: {audio_path.suffix}")
        
        # Carrega o áudio
        audio = AudioSegment.from_file(str(audio_path))
        
        # Normaliza o volume
        normalized_audio = audio.normalize()
        
        return normalized_audio
    
    def transcribe(self, audio_path: Union[str, Path]) -> Dict:
        """Realiza a transcrição do áudio"""
        try:
            # Carrega o áudio
            audio = self.load_audio(audio_path)
            
            # Realiza a transcrição
            result = self.model.transcribe(
                str(audio_path),
                language=self.config.LANGUAGE,
                fp16=torch.cuda.is_available()  # Usa GPU se disponível
            )
            
            # Adiciona metadados
            result['metadata'] = {
                'filename': Path(audio_path).name,
                'duration': len(audio) / 1000,  # Duração em segundos
                'timestamp': datetime.now().isoformat(),
                'model': self.config.WHISPER_MODEL,
                'language': self.config.LANGUAGE
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Erro na transcrição: {str(e)}")
    
    def export_transcription(self, transcription: Dict, output_path: Union[str, Path], 
                           format: str = 'txt') -> Path:
        """Exporta a transcrição no formato especificado"""
        output_path = Path(output_path)
        
        if format not in self.config.EXPORT_FORMATS:
            raise ValueError(f"Formato de exportação não suportado: {format}")
        
        if format == 'txt':
            # Exporta texto simples
            content = transcription['text']
            output_path = output_path.with_suffix('.txt')
            
        elif format == 'json':
            # Exporta JSON completo com metadados
            content = json.dumps(transcription, ensure_ascii=False, indent=2)
            output_path = output_path.with_suffix('.json')
            
        elif format == 'srt':
            # Exporta legendas no formato SRT
            content = self._generate_srt(transcription['segments'])
            output_path = output_path.with_suffix('.srt')
        
        # Salva o arquivo
        output_path.write_text(content, encoding='utf-8')
        
        return output_path
    
    def _generate_srt(self, segments: List[Dict]) -> str:
        """Gera legendas no formato SRT"""
        srt_content = []
        
        for i, segment in enumerate(segments, 1):
            # Converte timestamps para formato SRT
            start = self._format_timestamp(segment['start'])
            end = self._format_timestamp(segment['end'])
            
            # Formata o segmento
            srt_segment = f"{i}\n{start} --> {end}\n{segment['text'].strip()}\n"
            srt_content.append(srt_segment)
        
        return "\n".join(srt_content)
    
    def _format_timestamp(self, seconds: float) -> str:
        """Converte segundos para formato de timestamp SRT (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace('.', ',')

