from dotenv import load_dotenv  
import os  
import json  
import dropbox  
from google.cloud import speech_v1p1beta1 as speech  

# Charger les variables d'environnement  
load_dotenv()  

# Récupérer les clés API  
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")

# Vérification des variables d'environnement  
if not DROPBOX_ACCESS_TOKEN:
    raise ValueError("⚠️ ERREUR : Le jeton Dropbox est introuvable. Vérifie ton fichier .env.")

if not GOOGLE_CREDENTIALS_JSON:
    raise ValueError("⚠️ ERREUR : Les identifiants Google Cloud sont introuvables. Vérifie ton fichier .env.")

# Configurer Dropbox API  
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# Configurer Google Speech-to-Text API  
service_account_info = json.loads(GOOGLE_CREDENTIALS_JSON)
client = speech.SpeechClient.from_service_account_info(service_account_info)

def upload_to_dropbox(local_file_path, dropbox_path):  
    """Uploader un fichier vers Dropbox."""  
    try:
        with open(local_file_path, "rb") as f:  
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))  
        print(f"✅ Fichier uploadé sur Dropbox : {dropbox_path}")  
    except Exception as e:
        print(f"❌ Erreur lors de l'upload : {e}")

def get_dropbox_direct_link(dropbox_path):  
    """Obtenir un lien direct pour Google Speech-to-Text."""  
    try:
        shared_link = dbx.sharing_create_shared_link_with_settings(dropbox_path).url  
        direct_link = shared_link.replace("?dl=0", "?dl=1")  # Convertir en lien direct  
        return direct_link  
    except Exception as e:
        print(f"❌ Erreur lors de la génération du lien : {e}")
        return None

def transcribe_video(video_path: str) -> str:  
    """  
    Transcrit un fichier audio en texte via Dropbox + Google Speech-to-Text.  

    Parameters  
    ----------  
    video_path : str  
        Chemin du fichier audio local.  

    Returns  
    -------  
    str  
        Transcription textuelle.  
    """  
    dropbox_path = f"/{os.path.basename(video_path)}"  # Chemin Dropbox  

    # 1️⃣ Upload sur Dropbox  
    upload_to_dropbox(video_path, dropbox_path)  

    # 2️⃣ Obtenir le lien direct Dropbox  
    gcs_uri = get_dropbox_direct_link(dropbox_path)  
    if not gcs_uri:
        return "❌ Impossible de récupérer le lien Dropbox."

    print(f"🔗 Lien Dropbox : {gcs_uri}")  

    # 3️⃣ Envoyer à Google Speech-to-Text  
    audio = speech.RecognitionAudio(uri=gcs_uri)  
    config = speech.RecognitionConfig(  
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  
        sample_rate_hertz=16000,  
        language_code="fr-FR",  
    )  

    try:
        operation = client.long_running_recognize(config=config, audio=audio)  
        print("🔄 Transcription en cours...")  

        response = operation.result(timeout=600)  

        # Récupérer la transcription  
        transcription = " ".join([result.alternatives[0].transcript for result in response.results])  

        return transcription.strip()  
    except Exception as e:
        print(f"❌ Erreur de transcription : {e}")
        return "❌ La transcription a échoué."

# Exemple d'utilisation  
if __name__ == "__main__":  
    video_path = "/sdcard/Download/samples_jfk.wav"  # Fichier audio local  
    transcription = transcribe_video(video_path)  
    print(f"📝 Transcription : {transcription}")
