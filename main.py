from flask import Flask
from routes.voice_routes import voice_routes  # El router maestro

app = Flask(__name__)
app.register_blueprint(voice_routes)

from routes.login import login_bp
app.register_blueprint(login_bp)









if __name__ == "__main__":
    app.run(debug=True, port=3000)

