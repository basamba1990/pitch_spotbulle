import librosa
import numpy as np
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Clé API Gemini pour l'usage de l'outil de génération de contenu
api_key = os.getenv("GEMINI_API_KEY")

# Configurer l'API Gemini avec la clé d'API
genai.configure(api_key=api_key)

def analyze_text(transcription: str) -> dict:
    """
    Analyse le texte avec Gemini et retourne des suggestions.

    Parameters
    ----------
    transcription : str
        Transcription textuelle de l'audio.
    
    Returns
    -------
    dict
        Résultats de l'analyse (ton, vocabulaire, structure, impact).
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Analyse du ton
    tone_prompt = f"Analysez le ton de ce texte :\n\n{transcription}"
    tone_response = model.generate_content(tone_prompt)
    tone = tone_response.text
    
    # Suggestions de vocabulaire
    vocab_prompt = f"Proposez des améliorations de vocabulaire pour ce texte :\n\n{transcription}"
    vocab_response = model.generate_content(vocab_prompt)
    vocab_suggestions = vocab_response.text
    
    # Analyse de la structure
    structure_prompt = f"Analysez la structure de ce texte et suggérez des améliorations :\n\n{transcription}"
    structure_response = model.generate_content(structure_prompt)
    structure_suggestions = structure_response.text
    
    # Évaluation de l'impact
    impact_prompt = f"Évaluez l'impact de ce texte et proposez des modifications pour maximiser l'engagement :\n\n{transcription}"
    impact_response = model.generate_content(impact_prompt)
    impact_suggestions = impact_response.text
    
    return {
        "tone": tone,
        "vocab_suggestions": vocab_suggestions,
        "structure_suggestions": structure_suggestions,
        "impact_suggestions": impact_suggestions,
    }

def classify_pitch(audio_file: str) -> str:
    """
    Analyse la hauteur du son (pitch) à partir d'un fichier audio.

    Parameters
    ----------
    audio_file : str
        Chemin du fichier audio à analyser.
    
    Returns
    -------
    str
        Résultat de l'analyse du pitch (fréquence moyenne en Hz).
    """
    try:
        # Charger l'audio avec librosa
        y, sr = librosa.load(audio_file)
        
        # Extraire le pitch (fréquence fondamentale)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        
        # Trouver la fréquence dominante
        pitch_values = pitches[magnitudes > np.median(magnitudes)]
        if len(pitch_values) > 0:
            avg_pitch = np.mean(pitch_values)
            return f"Analyse du pitch : fréquence moyenne = {avg_pitch:.2f} Hz"
        else:
            return "Impossible de détecter un pitch significatif."
    except Exception as e:
        return f"Erreur lors de l'analyse du pitch : {e}"
