import os
import wave
import ffmpeg
from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH")  # Chemin du modèle Vosk

def extract_audio(video_path: str) -> str:
    """Extrait l'audio d'une vidéo avec ffmpeg."""
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    ffmpeg.input(video_path).output(audio_path, format='wav', acodec='pcm_s16le', ar='16000').run(overwrite_output=True)
    return audio_path

def transcribe_video(video_path: str) -> str:
    """Utilise Vosk pour la transcription audio."""
    audio_path = extract_audio(video_path)
    if not os.path.exists(audio_path):
        return "Erreur lors de l'extraction audio"

    try:
        wf = wave.open(audio_path, "rb")
        model = Model(VOSK_MODEL_PATH)
        rec = KaldiRecognizer(model, wf.getframerate())

        transcript = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                transcript += rec.Result()

        transcript += rec.FinalResult()
        return transcript.strip() if transcript else "Aucune transcription obtenue"

    except Exception as e:
        print(f"Erreur de transcription : {e}")
        return "Erreur de transcription"
