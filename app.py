import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from models.transcriber import transcribe_video
from models.classifier import classify_pitch
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload_video():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"error": "Aucun fichier reçu"}), 400

        file = request.files["file"]
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Transcrire et classifier
        text = transcribe_video(filepath)
        category = classify_pitch(text)

        return jsonify({"transcription": text, "category": category})
      
    return render_template("upload.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedback_page():
    if request.method == "POST":
        user_feedback = request.form.get("feedback")
        category = request.form.get("category")
        print(f"Feedback reçu : {user_feedback} pour la catégorie {category}")
        return redirect(url_for("index"))

    return render_template("feedback.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Utilise le port fourni par Render
    app.run(host="0.0.0.0", port=port)

