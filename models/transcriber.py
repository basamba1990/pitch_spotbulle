from dotenv import load_dotenv
import os
import json
from google.cloud import speech_v1p1beta1 as speech

# Charger les variables d'environnement
load_dotenv()

# Charger la clé API depuis Render ou l'environnement
service_account_info = json.loads(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"))
client = speech.SpeechClient.from_service_account_info(service_account_info)

def transcribe_video(video_path: str) -> str:
    """
    Transcrit l'audio d'une vidéo en texte en utilisant Google Speech-to-Text.
    Compatible avec les fichiers de plus de 1 minute via long_running_recognize.

    Parameters
    ----------
    video_path : str
        Chemin vers le fichier audio.

    Returns
    -------
    str
        Transcription textuelle de l'audio.
    """
    # Charger l'audio
    with open(video_path, "rb") as audio_file:
        content = audio_file.read()

    # Configuration de la requête
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="fr-FR",
    )

    # Utiliser long_running_recognize() pour les fichiers longs
    operation = client.long_running_recognize(config=config, audio=audio)

    print("🔄 Traitement en cours... Cela peut prendre quelques minutes.")
    response = operation.result(timeout=600)  # Timeout après 10 min

    # Récupérer la transcription
    transcription = " ".join([result.alternatives[0].transcript for result in response.results])

    return transcription.strip()

# Exemple d'utilisation
if __name__ == "__main__":
    video_path = "/sdcard/Download/samples_jfk.wav"  # Ton fichier audio
    transcription = transcribe_video(video_path)
    print(f"📝 Transcription : {transcription}")
