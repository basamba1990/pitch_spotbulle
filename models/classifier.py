import google.generativeai as genai

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
    genai.configure(api_key="VOTRE_CLE_API_GEMINI")
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
