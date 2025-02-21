import os
import whisper
import ffmpeg

def extract_audio(video_path: str) -> str:
    """Extrait l'audio d'une vidéo avec ffmpeg et retourne le chemin du fichier audio."""
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    ffmpeg.input(video_path).output(audio_path, format='wav', acodec='pcm_s16le', ar='16000').run(overwrite_output=True)
    return audio_path

def transcribe_audio_whisper(audio_path: str) -> str:
    """Utilise Whisper d'OpenAI pour transcrire l'audio."""
    model = whisper.load_model("base")  # Vous pouvez choisir "small", "medium", "large" selon la puissance de votre PC
    result = model.transcribe(audio_path)
    return result["text"]

def transcribe_video(video_path: str) -> str:
    """Extrait l'audio et utilise Whisper pour la transcription."""
    audio_path = extract_audio(video_path)
    if not os.path.exists(audio_path):
        return "Erreur lors de l'extraction audio"

    try:
        transcript = transcribe_audio_whisper(audio_path)
        return transcript.strip() if transcript else "Aucune transcription obtenue"
    except Exception as e:
        print(f"Erreur de transcription audio : {e}")
        return "Erreur de transcription"
