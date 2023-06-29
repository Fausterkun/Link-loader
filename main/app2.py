import os.path

import yaml
import logging
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask
from dotenv import load_dotenv

# Project root path

BASE_PATH = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_PATH, ".env"))


def create_app():
    app = Flask(__name__)

    # config_path = os.path.join(BASE_PATH, 'config.yaml')
    # with open(config_path, 'r') as file:
    #     config = yaml.safe_load(file.read())
    #     app.config.from_mapping(config)

    # load config from yaml file
    app.config.from_file(str(BASE_PATH) + "/config.yaml", load=yaml.safe_load)
    configure_logging(app)

    from . import bp

    app.register_blueprint(bp)

    return app


def configure_logging(app):
    formatter_data = app.config["LOGGING"]["FORMATTER"]
    handler_args = app.config["LOGGING"]["HANDLER"]
    level = app.config["LOGGING"]["LEVEL"]

    # create formatter and setup
    log_handler = RotatingFileHandler(**handler_args)
    log_formatter = logging.Formatter(**formatter_data)
    log_handler.setFormatter(log_formatter)

    app.logger.setLevel(level)
    app.logger.addHandler(log_handler)
