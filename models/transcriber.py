
from dotenv import load_dotenv
import os
import subprocess
import dropbox
from google.cloud import speech_v1p1beta1 as speech

# Charger les variables d'environnement
load_dotenv()

# Configuration Dropbox
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# Configuration Google Speech-to-Text
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

client = speech.SpeechClient.from_service_account_info(service_account_info)

def upload_to_dropbox(local_path: str, dropbox_path: str) -> str:
    """Téléverse un fichier sur Dropbox et retourne le lien direct"""
    try:
        with open(local_path, "rb") as f:
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
        
        shared_link = dbx.sharing_create_shared_link_with_settings(dropbox_path).url
        return shared_link.replace("?dl=0", "?dl=1")
    except Exception as e:
        raise RuntimeError(f"Échec de l'upload Dropbox: {str(e)}")

def extract_audio(source_path: str, output_path: str) -> None:
    """Extrait l'audio d'un fichier vidéo avec ffmpeg"""
    try:
        subprocess.run([
            'ffmpeg', '-i', source_path,
            '-vn', '-acodec', 'pcm_s16le',
            '-ar', '16000', '-ac', '1', output_path
        ], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erreur ffmpeg: {e.stderr.decode()}")

def transcribe_media(file_path: str) -> str:
    """Pipeline complet de transcription"""
    try:
        # Extraction audio
        if file_path.lower().endswith(('.mp4', '.avi', '.mov')):
            audio_path = os.path.splitext(file_path)[0] + '.wav'
            extract_audio(file_path, audio_path)
            file_to_transcribe = audio_path
        else:
            file_to_transcribe = file_path

        # Upload vers Dropbox
        dropbox_path = f"/{os.path.basename(file_to_transcribe)}"
        direct_link = upload_to_dropbox(file_to_transcribe, dropbox_path)
        
        # Configuration transcription
        audio = speech.RecognitionAudio(uri=direct_link)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="fr-FR",
        )

        # Transcription
        operation = client.long_running_recognize(config=config, audio=audio)
        result = operation.result(timeout=600)
        
        # Nettoyage fichier audio temporaire
        if file_to_transcribe != file_path:
            os.remove(file_to_transcribe)
            
        return "\n".join([res.alternatives[0].transcript for res in result.results])
    
    except Exception as e:
        raise RuntimeError(f"Échec de la transcription: {str(e)}")

if __name__ == "__main__":
    # Exemple d'utilisation avec fichier local
    fichier = "samples_jfk.mp3"  # Utiliser un vrai fichier local
    transcription = transcribe_media(fichier)
    print("Résultat:\n", transcription)
