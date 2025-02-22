import os
import ffmpeg
import torch
import whisper
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Vérifier si un GPU est disponible
device = "cuda" if torch.cuda.is_available() else "cpu"

def load_model(model_name="tiny"):
    """Charge le modèle Whisper en fonction du matériel disponible."""
    try:
        model = whisper.load_model(model_name, device=device)
        return model
    except Exception as e:
        print(f"Erreur lors du chargement du modèle Whisper : {e}")
        return None

# Charger le modèle au démarrage
whisper_model = load_model("tiny")

def extract_audio(video_path: str) -> str:
    """Extrait l'audio d'une vidéo avec ffmpeg et retourne le chemin du fichier audio."""
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, format="wav", acodec="pcm_s16le", ac=1, ar=16000)
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        )
        if os.path.exists(audio_path):
            return audio_path
        else:
            print("Erreur : Le fichier audio n'a pas été généré.")
            return None
    except ffmpeg.Error as e:
        print(f"Erreur ffmpeg : {e.stderr.decode()}")
        return None

def transcribe_audio_whisper(audio_path: str) -> str:
    """Utilise Whisper pour transcrire un fichier audio."""
    if whisper_model is None:
        return "Modèle Whisper non chargé"

    try:
        result = whisper_model.transcribe(audio_path)
        return result.get("text", "Aucune transcription obtenue").strip()
    except Exception as e:
        print(f"Erreur de transcription Whisper : {e}")
        return "Erreur de transcription"

def transcribe_video(video_path: str) -> str:
    """Extrait l'audio d'une vidéo et transcrit son contenu avec Whisper."""
    audio_path = extract_audio(video_path)
    if not audio_path:
        return "Erreur lors de l'extraction audio"

    return transcribe_audio_whisper(audio_path)

# Test avec une vidéo (à remplacer par ton fichier)
if __name__ == "__main__":
    video_file = "example.mp4"  # Remplace par le chemin de ta vidéo
    transcription = transcribe_video(video_file)
    print("\n📜 Transcription :\n", transcription)
