import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from models.transcriber import transcribe_media
from models.classifier import classify_pitch
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "defaultsecret")
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "uploads")
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'wav', 'mp3'}

# Création du dossier uploads s'il n'existe pas
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def allowed_file(filename):
    """ Vérifie si le fichier a une extension autorisée """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload_video():
    if request.method == "GET":
        return render_template("upload.html")  # Afficher un formulaire d'upload

    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier reçu"}), 400
        
    file = request.files["file"]
    if file.filename == '':
        return jsonify({"error": "Aucun fichier sélectionné"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Format de fichier non supporté"}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        
        # Transcription
        text = transcribe_media(filepath)
        
        # Classification
        category = classify_pitch(text)
        
        # Nettoyage des fichiers temporaires
        os.remove(filepath)

        return jsonify({
            "transcription": text,
            "category": category
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085, debug=True)
