import os
import ffmpeg
import numpy as np
from whispercpp import Whisper
import torch
from tqdm import tqdm
import urllib
import hashlib
import io
import warnings

# Charger le modèle Whisper
def load_model(name="tiny.en"):
    _MODELS = {
        "tiny.en": "https://openaipublic.azureedge.net/main/whisper/models/d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03/tiny.en.pt",
    }

    device = "cuda" if torch.cuda.is_available() else "cpu"
    cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "whisper")

    os.makedirs(cache_dir, exist_ok=True)
    model_url = _MODELS[name]
    model_path = os.path.join(cache_dir, os.path.basename(model_url))

    if not os.path.exists(model_path):
        with urllib.request.urlopen(model_url) as source, open(model_path, "wb") as output:
            output.write(source.read())

    return Whisper(model_path)

whisper_model = load_model("tiny.en")

def extract_audio(video_path: str) -> str:
    """Extrait l'audio d'une vidéo avec ffmpeg et retourne le chemin du fichier audio."""
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    ffmpeg.input(video_path).output(audio_path, format="wav", acodec="pcm_s16le", ac=1, ar=16000).run(overwrite_output=True)
    return audio_path

def transcribe_audio_whisper(audio_path: str) -> str:
    """Utilise Whisper pour transcrire l'audio."""
    try:
        transcription = whisper_model.transcribe(audio_path)
        return transcription.strip()
    except Exception as e:
        print(f"Erreur de transcription Whisper : {e}")
        return "Erreur de transcription"

def transcribe_video(video_path: str) -> str:
    """Extrait l'audio et transcrit la vidéo avec Whisper."""
    audio_path = extract_audio(video_path)
    if not os.path.exists(audio_path):
        return "Erreur lors de l'extraction audio"

    return transcribe_audio_whisper(audio_path)
