from dotenv import load_dotenv
import os
from google.cloud import speech_v1p1beta1 as speech
import wave
import pydub

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Utiliser la variable GOOGLE_APPLICATION_CREDENTIALS pour définir la clé de service
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def extract_audio_from_video(video_path: str, audio_path: str) -> None:
    """
    Extrait l'audio d'une vidéo et le sauvegarde en fichier WAV.
    
    Parameters
    ----------
    video_path : str
        Chemin vers le fichier vidéo.
    audio_path : str
        Chemin vers le fichier audio où l'extraction sera sauvegardée.
    """
    video = pydub.AudioSegment.from_file(video_path)
    video.export(audio_path, format="wav")

def transcribe_audio(audio_path: str) -> str:
    """
    Transcrit l'audio en texte en utilisant Google Speech-to-Text.
    
    Parameters
    ----------
    audio_path : str
        Chemin vers le fichier audio en format WAV.
    
    Returns
    -------
    str
        La transcription textuelle de l'audio.
    """
    # Lire le fichier audio
    with open(audio_path, "rb") as audio_file:
        audio_content = audio_file.read()

    # Configuration du client Google Speech-to-Text
    client = speech.SpeechClient()

    # Configuration de la demande de transcription
    response = client.recognize(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="fr-FR"
        ),
        audio=speech.RecognitionAudio(content=audio_content)
    )
    
    # Retourner la première transcription obtenue
    for result in response.results:
        return result.alternatives[0].transcript

# Exemple d'utilisation
video_path = "/home/userland/mon_video.mp4"  # Remplace par ton fichier vidéo
audio_path = "/home/userland/mon_audio.wav"  # Chemin de sauvegarde de l'audio extrait

# Extraire l'audio de la vidéo
extract_audio_from_video(video_path, audio_path)

# Transcrire l'audio
transcription = transcribe_audio(audio_path)
print(f"📝 Transcription : {transcription}")
