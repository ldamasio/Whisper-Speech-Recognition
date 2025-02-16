# main.py
from config import Config
from audio_processor import AudioProcessor
import argparse
from pathlib import Path
import sys

def main():
    # Configura os argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Transcrição de áudio usando Whisper')
    parser.add_argument('audio_path', help='Caminho para o arquivo de áudio')
    parser.add_argument('--output', '-o', help='Diretório de saída para a transcrição')
    parser.add_argument('--format', '-f', choices=['txt', 'json', 'srt'], 
                        default='txt', help='Formato de saída')
    args = parser.parse_args()
    
    try:
        # Inicializa configurações
        config = Config()
        
        # Inicializa o processador de áudio
        processor = AudioProcessor(config)
        
        # Define o caminho de saída
        audio_path = Path(args.audio_path)
        output_dir = Path(args.output) if args.output else config.OUTPUT_DIR
        output_path = output_dir / audio_path.stem
        
        print(f"Iniciando transcrição de: {audio_path.name}")
        
        # Realiza a transcrição
        transcription = processor.transcribe(audio_path)
        
        # Exporta o resultado
        output_file = processor.export_transcription(
            transcription, 
            output_path, 
            args.format
        )
        
        print("\nTranscrição concluída com sucesso!")
        print(f"Arquivo salvo em: {output_file}")
        
    except Exception as e:
        print(f"Erro: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()