from dotenv import load_dotenv
import os
import subprocess
import tempfile
from google.cloud import storage
from google.cloud import speech_v1p1beta1 as speech

# Charger les variables d'environnement
load_dotenv()

# Configuration sécurisée
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

# Clients init
storage_client = storage.Client.from_service_account_info(service_account_info)
speech_client = speech.SpeechClient.from_service_account_info(service_account_info)

def download_from_gcs(gcs_uri: str) -> str:
    """Télécharge un fichier depuis GCS vers un fichier temporaire"""
    try:
        bucket_name, blob_name = gcs_uri.replace("gs://", "").split("/", 1)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            blob.download_to_filename(temp_file.name)
            return temp_file.name
            
    except Exception as e:
        raise RuntimeError(f"Erreur de téléchargement GCS: {str(e)}")

def extract_audio_from_video(video_path: str) -> str:
    """Extrait l'audio en WAV 16kHz mono"""
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as audio_temp:
            command = [
                'ffmpeg',
                '-i', video_path,
                '-vn',
                '-acodec', 'pcm_s16le',
                '-ar', '16000',
                '-ac', '1',
                '-y',
                audio_temp.name
            ]
            subprocess.run(command, check=True, stderr=subprocess.PIPE)
            return audio_temp.name
            
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode('utf-8')
        raise RuntimeError(f"Erreur FFmpeg: {error_msg}")

def upload_to_gcs(file_path: str, bucket_name: str) -> str:
    """Upload un fichier vers GCS"""
    try:
        blob_name = os.path.basename(file_path)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return f"gs://{bucket_name}/{blob_name}"
        
    except Exception as e:
        raise RuntimeError(f"Erreur d'upload GCS: {str(e)}")

def transcribe_audio(gcs_uri: str) -> str:
    """Transcrit un fichier audio depuis GCS"""
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="fr-FR",
        enable_automatic_punctuation=True,
    )

    operation = speech_client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=600)
    
    return " ".join([result.alternatives[0].transcript for result in response.results])

def process_file(gcs_input_uri: str, bucket_name: str) -> str:
    """Pipeline complet de traitement"""
    try:
        # Téléchargement du fichier source
        local_video_path = download_from_gcs(gcs_input_uri)
        
        # Extraction audio
        local_audio_path = extract_audio_from_video(local_video_path)
        
        # Upload audio
        audio_gcs_uri = upload_to_gcs(local_audio_path, bucket_name)
        
        # Transcription
        transcription = transcribe_audio(audio_gcs_uri)
        
        return transcription
        
    finally:
        # Nettoyage des fichiers temporaires
        for path in [local_video_path, local_audio_path]:
            if path and os.path.exists(path):
                os.remove(path)

# Exemple d'utilisation
if __name__ == "__main__":
    input_uri = "gs://mon-bucket-gcs-spotbulle-2050/Emerging_Valley.mp4"
    output_bucket = "mon-bucket-gcs-spotbulle-2050"
    
    result = process_file(input_uri, output_bucket)
    print(f"Résultat de la transcription:\n{result}")
