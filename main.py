from flask import Flask
from routes.voice_routes import voice_routes  # El router maestro

app = Flask(__name__)
app.register_blueprint(voice_routes)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
