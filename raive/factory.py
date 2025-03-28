import os
import logging

from flask import Flask, render_template, request
from flask.json import jsonify
from flask_cors import CORS

from raive.engine import SoundEngine


def create_app():
    """
    Creates and configures the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(APP_DIR, "static")
    TEMPLATE_FOLDER = os.path.join(APP_DIR, "templates")
    logging.basicConfig(level=logging.DEBUG)

    sound_engine = SoundEngine()
    app = Flask(
        __name__,
        static_folder=STATIC_FOLDER,
        template_folder=TEMPLATE_FOLDER,
    )
    CORS(app)

    # Routes for HTML pages
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_index(path):
        return render_template("index.html")

    # Routes for API
    @app.route("/api/engine", methods=["POST"])
    def update_sound():
        prompt = request.json["prompt"]
        sound_engine.update(prompt)
        response = sound_engine.get_response()
        return jsonify({"response": response}), 200

    return app
