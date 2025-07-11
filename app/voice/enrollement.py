from flask import Blueprint, request, jsonify
from app.voice.voice_processor import VoiceProcessor
import os
import json

enroll_bp = Blueprint("enroll", __name__)
processor = VoiceProcessor()

# Ruta del "mock DB" para almacenar voiceprints
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/voiceprints.json"))

# Asegura que exista el archivo
if not os.path.exists(os.path.dirname(DB_PATH)):
    os.makedirs(os.path.dirname(DB_PATH))

if not os.path.exists(DB_PATH):
    with open(DB_PATH, "w") as f:
        json.dump({}, f)

@enroll_bp.route("/api/enroll", methods=["POST"])
def enroll():
    user_id = request.form.get("userId")
    audio_file = request.files.get("audio")

    if not user_id or not audio_file:
        return jsonify({"error": "Faltan campos requeridos: userId y audio"}), 400

    # Guardar archivo temporal
    temp_path = f"/tmp/{user_id}.wav"
    audio_file.save(temp_path)

    try:
        # Generar voiceprint
        voiceprint = processor.generate_voiceprint(temp_path)
        voiceprint = voiceprint.tolist()  # ← convierte array NumPy a lista de floats JSON-safe


        # Guardar en "DB"
        with open(DB_PATH, "r") as f:
            data = json.load(f)

        data[user_id] = voiceprint

        with open(DB_PATH, "w") as f:
            json.dump(data, f, indent=4)

        return jsonify({"message": "Voiceprint registrado correctamente", "userId": user_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
