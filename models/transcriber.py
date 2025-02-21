import os
import google.generativeai as genai
import ffmpeg
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_audio(video_path):
    """Extrait l'audio d'une vidéo et le sauvegarde en format WAV."""
    audio_path = video_path.rsplit(".", 1)[0] + ".wav"
    
    try:
        ffmpeg.input(video_path).output(audio_path, format="wav", acodec="pcm_s16le").run(overwrite_output=True)
        return audio_path
    except Exception as e:
        print(f"Erreur d'extraction audio : {e}")
        return None

def transcribe_video(video_path: str) -> str:
    """Extrait l'audio et utilise Gemini AI pour la transcription"""
    audio_path = extract_audio(video_path)
    if not audio_path:
        return "Erreur lors de l'extraction audio"

    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Transcrivez le contenu audio du fichier : {audio_path}"
        response = model.generate_content(prompt)
        return response.text.strip() if response.text.strip() else "Transcription vide"
    except Exception as e:
        print(f"Erreur lors de la transcription : {e}")
        return "Erreur de transcription"
