import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")  # Récupère la clé secrète
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")  # Dossier pour les fichiers téléchargés
    # Ajouter d'autres variables nécessaires
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")  # Ajouté pour la clé Google Cloud


# Charger la configuration
config = Config()
