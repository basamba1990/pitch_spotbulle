import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configuration de l'API Gemini (remplacée par l'API de Gemini pour la transcription)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def transcribe_video(video_path: str) -> str:
    """Utilise Gemini AI pour transcrire le texte"""
    try:
        # Implémentation de la transcription avec Gemini
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Transcrivez le contenu vidéo de ce fichier: {video_path}"
        response = model.generate_content(prompt)
        transcription = response.text.strip()

        if transcription.strip():
            return transcription
    
    except Exception as e:
        print(f"Erreur lors de la transcription : {e}")

    return "Erreur de transcription"
