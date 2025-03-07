import os
import shutil
import tempfile
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from models.transcriber import transcribe_video
from models.classifier import classify_pitch

# Chargement des variables d'environnement
load_dotenv()

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY"),
    UPLOAD_FOLDER=os.getenv("UPLOAD_FOLDER", "uploads"),
    MAX_CONTENT_LENGTH=500 * 1024 * 1024,  # 500MB
    ALLOWED_EXTENSIONS={'mp4', 'avi', 'mov', 'mp3', 'wav'}
)

# Création du dossier d'upload sécurisé
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def cleanup_temp_files(path):
    """Nettoie les fichiers temporaires de manière sécurisée"""
    try:
        if path and os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
    except Exception as e:
        app.logger.error(f"Error cleaning temp files: {str(e)}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier reçu"}), 400
        
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Fichier non valide"}), 400

    try:
        # Création d'un répertoire temporaire sécurisé
        with tempfile.TemporaryDirectory() as tmp_dir:
            filename = secure_filename(file.filename)
            file_path = os.path.join(tmp_dir, filename)
            file.save(file_path)

            # Transcription et classification
            transcription = transcribe_video(file_path)
            category = classify_pitch(file_path)
            
            return jsonify({
                "transcription": transcription,
                "category": category
            })

    except subprocess.CalledProcessError as e:
        app.logger.error(f"FFmpeg error: {str(e)}")
        return jsonify({"error": "Erreur de traitement vidéo"}), 500
        
    except Exception as e:
        app.logger.error(f"General error: {str(e)}")
        return jsonify({"error": "Erreur de traitement"}), 500

@app.route("/feedback", methods=["POST"])
def handle_feedback():
    try:
        feedback_data = request.get_json()
        if not feedback_data or 'feedback' not in feedback_data or 'category' not in feedback_data:
            return jsonify({"error": "Données manquantes"}), 400

        # Traitement du feedback
        app.logger.info(f"Feedback reçu ({feedback_data['category']}): {feedback_data['feedback']}")
        return jsonify({"message": "Feedback enregistré avec succès"})

    except Exception as e:
        app.logger.error(f"Feedback error: {str(e)}")
        return jsonify({"error": "Erreur de traitement"}), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8085)),
        debug=os.getenv("DEBUG_MODE", "false").lower() == "true"
    )
