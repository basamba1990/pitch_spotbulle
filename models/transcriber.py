from dotenv import load_dotenv
import os
from google.cloud import speech_v1p1beta1 as speech

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Utiliser la variable GOOGLE_APPLICATION_CREDENTIALS pour définir la clé de service
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_PRIVATE_KEY")

def transcribe_video(video_path: str) -> str:
    """
    Transcrit l'audio d'une vidéo en texte en utilisant Google Speech-to-Text.

    Parameters
    ----------
    video_path : str
        Chemin vers le fichier vidéo.

    Returns
    -------
    str
        Transcription textuelle de l'audio.
    """
    # Configuration du client Google Speech-to-Text
    client = speech.SpeechClient()

    # Charger l'audio
    with open(video_path, "rb") as audio_file:
        content = audio_file.read()

    # Configuration de la requête
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="fr-FR",  # Langue française
    )

    # Envoyer la requête
    response = client.recognize(config=config, audio=audio)

    # Récupérer la transcription
    transcription = ""
    for result in response.results:
        transcription += result.alternatives[0].transcript + " "

    return transcription.strip()
