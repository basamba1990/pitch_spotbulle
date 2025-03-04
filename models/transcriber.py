from dotenv import load_dotenv
import os
import subprocess
from google.cloud import storage
from google.cloud import speech_v1p1beta1 as speech

# Charger les variables d'environnement
load_dotenv()

# Clé API extraite directement
service_account_info = {
    "type": "service_account",
    "project_id": "speech-to-text-452320",
    "private_key_id": "99b02bd396ce1984fdf7d86c8889c9821e8b9e43",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDG1nnHAauUWLbg
mXQR52JZ36OdJXdPO0RSrVbMfyBbC0tbF34Bq02DV2VzLsikHdXPSHdGe5JuTs+2
sFobEfaQz+W7aNOLKU7rC7AChCmv1JlIQ342xyQ78ru2G/qFp/PcMCW1/O245MDe
Nljxq+P8HhsHvi0oj5BnasTOGxWh0mieTSksh6oebnbgqQAxr/mwZ6IKkiWL0+vm
80K4UE/4W2aqs3Yie/Zkb9QAA4DIMmwpT26n+4ysL5Q3gChljDfnNaWpWQzNDzRj
ZWmtif8DzMEE4xJ4hIx7XaObaXByYD9o9QtbbTtBlXGsJD7XlqxFAraD2j/jpXDd
nHzJkwDvAgMBAAECggEAHwT2moU4Lzxny0IlSWW/giXRcIKXylSEpCFGmUB727g3
WU6g6cG/pe3MddumkXPWFzBG60f74BmLbgS1CeQTgyPrwwDnf55CIYkBPGNB3Zxd
DVj6J7GJhZComBBlVNSOxpr8RxfePinxrLjtx0X5mytXLC4O/XToIjoV2dF/3m6d
5wJHqxF+Z1tXUeEd6bWPjYOtnH7fl13yCexYQ0H2Pl/YzW8u/6STjkkBhC0zy/dm
fYY2iMbaIsP+qd9GU1G5qrHqYQHc5x48foTMv1+8jfv/OzOxYVAwknmg/KKEFmdC
Mh5yQn715H1c8wkNjnKitJYFoEntsurw6//roypVAQKBgQD9I3Zf1W/gwkLBaBTD
TklBwm/GDeW9UChf44wP/AQED2ZSl2x6EDr0x8X0ea1CuuKdpM/jV/3yqxSRCis5
+o8KOvQb2EA7MlXys0/xEYqLpzdZPyaVL2tcPoTpWiYViDPU72SsFfQBNWWUecKt
zrGQynEmn1Ress9LL3Y+M1ZriQKBgQDJFeBvRAi56iYiHDlNCvnqu2iOqW5oejq8
SsFIx6kA/AjuFXsnxNf2UqJEJwUdxbhO/sWNV0Rwf8AI1tkiCKJP0NLWqe4BDdM0
8vS9Awv408GLP3QPyg+GtMdp+RAOko2NfsGKHWFhOPm+VrATDOV6pZ4gXFI/0UVs
0WIlq7iStwKBgQDEJZxt+dbtE9niP6IHDDxbhixSDSa9oMUIOCupnyAFfWFOEiNu
GfF1Bu9u1nHYyTMb8D9d7CrMxJ/1GyoPjQUVakUI5nIu7HwIycTiCTOPrwyGTRa6
drn8Cj23C7GC8b0n/C/H4GLoJNYHTKn7P7P7e8JdqQwZLPjPS4GWBPWr8QKBgD8k
WnQ11dOjPdQqLqgNkUpvDLb3Zw7xiq4Df0v+PghsG9W+8wwa2IGlkwR5iDbAFk7f
22K1i20UAFYGOOph8a3EceAsPesgzzhqLgWIBmNdAwJZq3UlythOvet95Nfelwpe
SiG3dhOUU3+8Ms/Yldp8VPnuY3lcmkNAQGR51pxjAoGBAK2f8+5ZyvpFEmyHgidL
qEYmNbFZfbDg3ksGzOl8EmpIdZAAD/GB5MZ1sZGdR/yy5KjYB0Q+qH4YcPQZhQNt
ZIDYI6mADlcfVd4/7A2JzDECPCVEHU2iKAze730kn0Dg6Uky681SywoERR7W5zNh
uJ5ogNfpKQHcUxCitje3nAae
-----END PRIVATE KEY-----""",
    "client_email": "speech-to-text-service@speech-to-text-452320.iam.gserviceaccount.com",
    "client_id": "118279315305838707937",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/speech-to-text-service%40speech-to-text-452320.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# Créer un client Google Speech-to-Text
client = speech.SpeechClient.from_service_account_info(service_account_info)

def extract_audio_from_video(video_path: str, audio_path: str) -> None:
    """
    Utilise ffmpeg pour extraire l'audio d'une vidéo et sauvegarder le fichier audio extrait.
    """
    command = ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', audio_path]
    subprocess.run(command, check=True)
    print(f"✅ Audio extrait de {video_path} et sauvegardé sous {audio_path}")

def upload_to_gcs(filepath: str, bucket_name: str) -> str:
    """
    Téléverse le fichier audio sur Google Cloud Storage et retourne l'URI GCS.
    """
    storage_client = storage.Client.from_service_account_info(service_account_info)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(os.path.basename(filepath))
    blob.upload_from_filename(filepath)
    gcs_uri = f"gs://{bucket_name}/{os.path.basename(filepath)}"
    print(f"📤 Fichier téléchargé vers {gcs_uri}")
    return gcs_uri

def transcribe_audio_from_gcs(gcs_uri: str) -> str:
    """
    Transcrit l'audio stocké sur Google Cloud Storage avec Google Speech-to-Text.
    """
    print(f"🔗 URI GCS reçu : {gcs_uri}")
    
    # Configurer la requête pour Google Speech-to-Text
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="fr-FR",
    )
    
    print("🔄 Transcription en cours... Cela peut prendre quelques minutes.")
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=600)  # Timeout après 10 minutes
    
    # Récupérer et retourner la transcription
    transcription = " ".join([result.alternatives[0].transcript for result in response.results])
    return transcription.strip()

def transcribe_video(video_path: str, bucket_name: str) -> str:
    """
    Transcrit l'audio d'une vidéo. Extrait d'abord l'audio, puis le téléverse sur GCS et le transcrit.
    """
    # Extraire l'audio de la vidéo
    audio_path = video_path.replace(".mp4", ".wav")
    extract_audio_from_video(video_path, audio_path)
    
    # Téléverser l'audio vers Google Cloud Storage
    gcs_uri = upload_to_gcs(audio_path, bucket_name)
    
    # Transcrire l'audio depuis GCS
    transcription = transcribe_audio_from_gcs(gcs_uri)
    return transcription

# Exemple d'utilisation
video_path = "chemin/vers/votre/video.mp4"
bucket_name = "mon-bucket-gcs-spotbulle-2050"
transcription = transcribe_video(video_path, bucket_name)
print(f"📝 Transcription : {transcription}")
