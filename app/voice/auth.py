# from flask import Blueprint, request, jsonify
# from app.voice.voice_processor import VoiceProcessor
# import os
# import json

# auth_bp = Blueprint("auth", __name__)
# processor = VoiceProcessor()

# # Ruta del "mock DB"
# DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/voiceprints.json"))

# @auth_bp.route("/api/auth", methods=["POST"])
# def authenticate():
#     user_id = request.form.get("userId")
#     audio_file = request.files.get("audio")

#     if not user_id or not audio_file:
#         return jsonify({"error": "Faltan campos requeridos: userId y audio"}), 400

#     # Guardar archivo temporal
#     temp_path = f"/tmp/{user_id}_auth.wav"
#     audio_file.save(temp_path)

#     try:
#         # Leer voiceprint registrado
#         with open(DB_PATH, "r") as f:
#             data = json.load(f)

#         if user_id not in data:
#             return jsonify({"error": "Usuario no registrado"}), 404

#         stored_voiceprint = data[user_id]

#         # Comparar voiceprints
#         match = processor.verify_voiceprint(temp_path, stored_voiceprint)

#         if match:
#             return jsonify({"message": "Autenticación exitosa", "userId": user_id}), 200
#         # else:
#             return jsonify({"error": "La voz no coincide"}), 401

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

#     finally:
#         if os.path.exists(temp_path):
#             os.remove(temp_path)
import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.voice.voice_processor import VoiceProcessor

# Carga del "mock DB"
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/voiceprints.json"))
processor = VoiceProcessor()

def get_saved_voiceprint(user_id):
    if not os.path.exists(DB_PATH):
        return None

    with open(DB_PATH, "r") as f:
        data = json.load(f)

    if user_id not in data:
        return None

    return np.array(data[user_id], dtype=float)  # ⚠️ Esta línea es la clave

def compare_voiceprints(embedding1, embedding2):
    embedding1 = np.array(embedding1, dtype=float)
    embedding2 = np.array(embedding2, dtype=float)
    return cosine_similarity(embedding1.reshape(1, -1), embedding2.reshape(1, -1))[0][0]

def verify_user(user_id, audio_path):
    # Generar vector del audio entrante
    input_vector = processor.generate_voiceprint(audio_path)

    # Obtener vector guardado
    saved_vector = get_saved_voiceprint(user_id)
    if saved_vector is None:
        raise ValueError("El usuario no está enrolado")

    # Comparar
    similarity = compare_voiceprints(input_vector, saved_vector)
    is_match = similarity > 0.75  # puedes ajustar este umbral

    return is_match, similarity
