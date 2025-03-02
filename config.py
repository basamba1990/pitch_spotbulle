import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")  # Récupère la clé secrète
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")  # Dossier pour les fichiers téléchargés
    # Ajouter d'autres variables nécessaires
    API_KEY_TRANSCRIPTION = os.getenv("API_KEY_TRANSCRIPTION")


# Charger la configuration
config = Config()
