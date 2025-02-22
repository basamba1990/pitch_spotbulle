import os
import ffmpeg
import torch
import whisper
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Vérifier si un GPU est disponible
device = "cuda" if torch.cuda.is_available() else "cpu"

# Charger le modèle Whisper
def load_model(model_name="tiny"):
    """Charge le modèle Whisper."""
    try:
        model = whisper.load_model(model_name, device=device)
        return model
    except Exception as e:
        print(f"Erreur lors du chargement du modèle Whisper : {e}")
        return None

whisper_model = load_model("tiny")

def extract_audio(video_path: str) -> str:
    """Extrait l'audio d'une vidéo avec ffmpeg et retourne le chemin du fichier audio."""
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    try:
        ffmpeg.input(video_path).output(audio_path, format="wav", acodec="pcm_s16le", ac=1, ar=16000).run(overwrite_output=True)
        return audio_path
    except Exception as e:
        print(f"Erreur lors de l'extraction audio : {e}")
        return None

def transcribe_audio_whisper(audio_path: str) -> str:
    """Utilise Whisper pour transcrire l'audio."""
    if whisper_model is None:
        return "Modèle Whisper non chargé"
    
    try:
        result = whisper_model.transcribe(audio_path)
        return result["text"].strip() if "text" in result else "Aucune transcription obtenue"
    except Exception as e:
        print(f"Erreur de transcription Whisper : {e}")
        return "Erreur de transcription"

def transcribe_video(video_path: str) -> str:
    """Extrait l'audio et transcrit la vidéo avec Whisper."""
    audio_path = extract_audio(video_path)
    if not audio_path or not os.path.exists(audio_path):
        return "Erreur lors de l'extraction audio"

    return transcribe_audio_whisper(audio_path)
