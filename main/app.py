import os.path
from pathlib import Path

from flask import Flask
from dotenv import load_dotenv

from main.settings import configure_app

# Project root path

BASE_PATH = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_PATH, ".env"))


def create_app(conf_filename: str = "config.yaml"):
    """Create and configurate app"""
    app = Flask(__name__)
    configure_app(app, conf_filename)

    return app
