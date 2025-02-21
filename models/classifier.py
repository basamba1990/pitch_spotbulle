import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def classify_pitch(text):
    """Classifie le pitch en catégorie avec Gemini AI"""
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Classifie ce pitch en catégorie (Tech, Santé, Éducation, Finance) : {text}"
    response = model.generate_content(prompt)
    
    return response.text.strip()
