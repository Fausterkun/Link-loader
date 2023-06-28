from flask import Flask
import yaml
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

# Project root path
BASE_PATH = Path(__file__).resolve().parent.parent


def create_app():
    # create app
    app = Flask(__name__)
    app.config.from_file(str(BASE_PATH) + '/config.yaml', load=yaml.safe_load)

    return app


app = create_app()
from routes import *

if __name__ == '__main__':
    app.run()
