from flask import Blueprint, request, jsonify
from app.voice.voice_processor import VoiceProcessor
import os
import json

auth_bp = Blueprint("auth", __name__)
processor = VoiceProcessor()

# Ruta del "mock DB"
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/voiceprints.json"))

@auth_bp.route("/api/auth", methods=["POST"])
def authenticate():
    user_id = request.form.get("userId")
    audio_file = request.files.get("audio")

    if not user_id or not audio_file:
        return jsonify({"error": "Faltan campos requeridos: userId y audio"}), 400

    # Guardar archivo temporal
    temp_path = f"/tmp/{user_id}_auth.wav"
    audio_file.save(temp_path)

    try:
        # Leer voiceprint registrado
        with open(DB_PATH, "r") as f:
            data = json.load(f)

        if user_id not in data:
            return jsonify({"error": "Usuario no registrado"}), 404

        stored_voiceprint = data[user_id]

        # Comparar voiceprints
        match = processor.verify_voiceprint(temp_path, stored_voiceprint)

        if match:
            return jsonify({"message": "Autenticación exitosa", "userId": user_id}), 200
        else:
            return jsonify({"error": "La voz no coincide"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
