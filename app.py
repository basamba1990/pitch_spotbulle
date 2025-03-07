import os
import tempfile
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models.transcriber import transcribe_video
from models.classifier import classify_pitch
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret-key"),
    UPLOAD_FOLDER=os.getenv("UPLOAD_FOLDER", "uploads"),
    MAX_CONTENT_LENGTH=500 * 1024 * 1024,  # 500MB
    ALLOWED_EXTENSIONS={'mp4', 'avi', 'mov', 'mp3', 'wav'},
    GCS_BUCKET=os.getenv("GCS_BUCKET")
)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def handle_upload():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier reçu"}), 400
        
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Fichier non valide"}), 400

    try:
        # Sauvegarde temporaire
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            file.save(tmp_file.name)
            
            # Traitement
            transcription = transcribe_video(tmp_file.name, app.config["GCS_BUCKET"])
            category = classify_pitch(tmp_file.name)
            
            return jsonify({
                "transcription": transcription,
                "category": category
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if tmp_file:
            os.remove(tmp_file.name)

@app.route("/feedback", methods=["POST"])
def handle_feedback():
    try:
        data = request.get_json()
        if not data or 'feedback' not in data or 'category' not in data:
            return jsonify({"error": "Données manquantes"}), 400

        # Logique de traitement du feedback
        print(f"Feedback reçu ({data['category']}): {data['feedback']}")
        return jsonify({"message": "Feedback enregistré"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8085)),
        debug=os.getenv("DEBUG_MODE", "false").lower() == "true"
    )
