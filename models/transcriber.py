import os
import ffmpeg
import numpy as np
from whispercpp import Whisper

# Charger le modèle WhisperCpp
whisper_model = Whisper.from_pretrained("tiny.en")

def extract_audio(video_path: str) -> str:
    """Extrait l'audio d'une vidéo avec ffmpeg et retourne le chemin du fichier audio."""
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    ffmpeg.input(video_path).output(audio_path, format="wav", acodec="pcm_s16le", ac=1, ar=16000).run()
    return audio_path

def transcribe_audio_whisper(audio_path: str) -> str:
    """Utilise WhisperCpp pour transcrire l'audio."""
    try:
        # Charger l'audio
        y, _ = (
            ffmpeg.input(audio_path, threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=16000)
            .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
        )
        
        # Convertir en tableau NumPy normalisé
        audio_array = np.frombuffer(y, np.int16).astype(np.float32) / 32768.0

        # Transcription avec WhisperCpp
        transcription = whisper_model.transcribe(audio_array)
        return transcription.strip()
    
    except Exception as e:
        print(f"Erreur de transcription WhisperCpp : {e}")
        return "Erreur de transcription"

def transcribe_video(video_path: str) -> str:
    """Extrait l'audio et transcrit la vidéo avec WhisperCpp."""
    audio_path = extract_audio(video_path)
    if not os.path.exists(audio_path):
        return "Erreur lors de l'extraction audio"

    return transcribe_audio_whisper(audio_path)
