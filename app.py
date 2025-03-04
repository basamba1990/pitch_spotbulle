import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models.transcriber import transcribe_file  # Assurez-vous d'importer correctement la fonction
from models.classifier import classify_pitch
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "uploads")

# Formats de fichiers autorisés
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Fonction pour vérifier les extensions de fichiers autorisées
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route principale - Page d'accueil
@app.route("/")
def index():
    return render_template("index.html")

# Route pour l'upload de vidéos
@app.route("/upload", methods=["GET", "POST"])
def upload_video():
    if request.method == "GET":
        return render_template("upload.html")
    
    if "file" not in request.files:
        flash("Aucun fichier reçu", "error")
        return redirect(url_for("upload_video"))

    file = request.files["file"]
    if file.filename == "":
        flash("Aucun fichier sélectionné", "error")
        return redirect(url_for("upload_video"))

    # Vérifier si le fichier a une extension autorisée
    if not allowed_file(file.filename):
        flash("Format de fichier non autorisé", "error")
        return redirect(url_for("upload_video"))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        # Transcription de la vidéo avec la fonction mise à jour
        text = transcriber_file(filepath, bucket_name="my_bucket")  # Assurez-vous que le nom du bucket est correct
        # Classification du pitch
        category = classify_pitch(filepath)
        return jsonify({"transcription": text, "category": category})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour le retour d'information (feedback)
@app.route("/feedback", methods=["POST"])
def feedback_page():
    user_feedback = request.form.get("feedback")
    category = request.form.get("category")

    if not user_feedback or not category:
        flash("Merci de remplir tous les champs.", "error")
        return redirect(url_for("index"))

    print(f"Feedback reçu : {user_feedback} pour la catégorie {category}")
    flash("Votre feedback a été envoyé avec succès !", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085, debug=True)
