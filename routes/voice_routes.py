from flask import Blueprint
from app.voice.enrollement import enroll_bp
# from app.voice.auth import auth_bp
from routes.verify import verify_bp

voice_routes = Blueprint("voice_routes", __name__)

# Registrar subrutas
voice_routes.register_blueprint(enroll_bp)
# voice_routes.register_blueprint(auth_bp)


voice_routes = Blueprint("voice_routes", __name__)
voice_routes.register_blueprint(enroll_bp)
voice_routes.register_blueprint(verify_bp)
