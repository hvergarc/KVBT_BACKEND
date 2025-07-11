# from flask import Blueprint, request, jsonify
# import os
# import json
# from app.voice.voice_processor import VoiceProcessor

# login_bp = Blueprint("login", __name__)
# processor = VoiceProcessor()

# # Ruta al archivo de voiceprints
# DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/voiceprints.json"))

# @login_bp.route("/api/login", methods=["POST"])
# def login():
#     user_id = request.form.get("userId")
#     audio_file = request.files.get("audio")

#     if not user_id or not audio_file:
#         return jsonify({"error": "Faltan campos requeridos: userId y audio"}), 400

#     temp_path = f"/tmp/{user_id}_login.wav"
#     audio_file.save(temp_path)

#     try:
#         # Cargar base de datos
#         if not os.path.exists(DB_PATH):
#             return jsonify({"error": "No hay voiceprints registrados"}), 404

#         with open(DB_PATH, "r") as f:
#             data = json.load(f)

#         if user_id not in data:
#             return jsonify({"error": "Usuario no registrado"}), 404

#         stored_voiceprint = data[user_id]
#         is_match, similarity = processor.compare_voiceprints(temp_path, stored_voiceprint)

#         if is_match:
#             return jsonify({"success": True, "userId": user_id, "similarity": similarity}), 200
#         else:
#             return jsonify({"success": False, "message": "La voz no coincide", "similarity": similarity}), 401

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

#     finally:
#         if os.path.exists(temp_path):
#             os.remove(temp_path)
from flask import Blueprint, request, jsonify
import os
from app.voice.auth import verify_user  # ✅ Importamos la función nueva

login_bp = Blueprint("login", __name__)

@login_bp.route("/api/login", methods=["POST"])
def login():
    user_id = request.form.get("userId")
    audio_file = request.files.get("audio")

    if not user_id or not audio_file:
        return jsonify({"error": "Faltan campos requeridos: userId y audio"}), 400

    temp_path = f"/tmp/{user_id}_login.wav"
    audio_file.save(temp_path)

    try:
        is_match, similarity = verify_user(user_id, temp_path)

        if is_match:
            return jsonify({"success": True, "userId": user_id, "similarity": similarity}), 200
        else:
            return jsonify({"success": False, "message": "La voz no coincide", "similarity": similarity}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
