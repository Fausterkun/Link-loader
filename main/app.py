import yaml
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask

# Project root path
BASE_PATH = Path(__file__).resolve().parent.parent


def create_app():
    app = Flask(__name__)
    # load config from yaml file
    app.config.from_file(str(BASE_PATH) + "/config.yaml", load=yaml.safe_load)
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
