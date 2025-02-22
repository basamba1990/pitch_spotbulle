import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models.transcriber import transcribe_video
from models.classifier import classify_pitch
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "uploads")

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

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

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        text = transcribe_video(filepath)
        category = classify_pitch(text)
        return jsonify({"transcription": text, "category": category})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
    app.run(host="0.0.0.0", port=5000, debug=True)
