import whisper
import ffmpeg

def extract_audio(video_path):
    """Extrait l'audio d'une vidéo et le sauvegarde en format WAV."""
    audio_path = video_path.rsplit(".", 1)[0] + ".wav"
    
    try:
        ffmpeg.input(video_path).output(audio_path, format="wav", acodec="pcm_s16le", ar="16000").run(overwrite_output=True)
        return audio_path
    except Exception as e:
        print(f"Erreur d'extraction audio : {e}")
        return None

def transcribe_video(video_path):
    """Extrait l'audio et utilise Whisper pour la transcription"""
    audio_path = extract_audio(video_path)
    if not audio_path:
        return "Erreur lors de l'extraction audio"

    try:
        model = whisper.load_model("base")  # Choisir un modèle (tiny, base, small, medium, large)
        result = model.transcribe(audio_path, language="fr")
        return result["text"] if result["text"] else "Aucune transcription obtenue"
    except Exception as e:
        print(f"Erreur lors de la transcription : {e}")
        return "Erreur de transcription"
