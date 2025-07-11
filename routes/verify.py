from flask import Blueprint, request, jsonify
from app.voice.voice_processor import VoiceProcessor
import os
import json

verify_bp = Blueprint("verify", __name__)
processor = VoiceProcessor()

# DB_PATH = os.path.join(os.path.dirname(__file__), "../data/voiceprints.json")
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/voiceprints.json"))

@verify_bp.route("/api/verify", methods=["POST"])
def verify():
    user_id = request.form.get("userId")
    audio_file = request.files.get("audio")

    if not user_id or not audio_file:
        return jsonify({"error": "Faltan campos requeridos: userId y audio"}), 400

    temp_path = f"/tmp/{user_id}_verify.wav"
    audio_file.save(temp_path)

    try:
        # Cargar voiceprints
        with open(DB_PATH, "r") as f:
            data = json.load(f)

        if user_id not in data:
            return jsonify({"error": "Usuario no registrado"}), 404

        stored_voiceprint = data[user_id]
        new_voiceprint = processor.generate_voiceprint(temp_path)

        # Comparar (aquí puedes ajustar el umbral)
        similarity = processor.compare_voiceprints(new_voiceprint, stored_voiceprint)
        is_match = similarity > 0.75  # umbral de confianza

        return jsonify({
            "match": is_match,
            "similarity": similarity
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
