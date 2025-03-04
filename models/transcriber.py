from dotenv import load_dotenv  
import os  
import json  
import dropbox  
from google.cloud import speech_v1p1beta1 as speech  

# Charger les variables d'environnement  
load_dotenv()  

# Configurer Dropbox API  
DROPBOX_ACCESS_TOKEN = os.getenv("sl.u.AFkKGNXTdif2ypO22MC0aJKJt7f7VVmXv9iDVBQOHtn1bbDrcP4Uy30A9ovpSNmYwjqjOTbPn60zVviLcaobddB0OQ2xpCIxT4")  
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)  

# Google Speech-to-Text API  
service_account_info = json.loads(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"))  
client = speech.SpeechClient.from_service_account_info(service_account_info)  

def upload_to_dropbox(local_file_path, dropbox_path):  
    """Uploader un fichier vers Dropbox"""  
    with open(local_file_path, "rb") as f:  
        dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))  
    print(f"✅ Fichier uploadé sur Dropbox : {dropbox_path}")  

def get_dropbox_direct_link(dropbox_path):  
    """Obtenir un lien direct pour Google Speech-to-Text"""  
    shared_link = dbx.sharing_create_shared_link_with_settings(dropbox_path).url  
    direct_link = shared_link.replace("?dl=0", "?dl=1")  # Convertir en lien direct  
    return direct_link  

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
    print(f"🔗 Lien Dropbox : {gcs_uri}")  

    # 3️⃣ Envoyer à Google Speech-to-Text  
    audio = speech.RecognitionAudio(uri=gcs_uri)  
    config = speech.RecognitionConfig(  
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  
        sample_rate_hertz=16000,  
        language_code="fr-FR",  
    )  

    operation = client.long_running_recognize(config=config, audio=audio)  
    print("🔄 Transcription en cours...")  

    response = operation.result(timeout=600)  

    # Récupérer la transcription  
    transcription = " ".join([result.alternatives[0].transcript for result in response.results])  

    return transcription.strip()  

# Exemple d'utilisation  
if __name__ == "__main__":  
    video_path = "/sdcard/Download/samples_jfk.wav"  # Fichier audio local  
    transcription = transcribe_video(video_path)  
    print(f"📝 Transcription : {transcription}")
