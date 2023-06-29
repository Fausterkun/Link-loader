import os.path
import yaml
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask
from dotenv import load_dotenv

from main import socketio
from main.logger import WebsocketHandler

# Project root path

BASE_PATH = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_PATH, ".env"))


def create_app():
    app = Flask(__name__)

    app.config.from_file(str(BASE_PATH) + "/config.yaml", load=yaml.safe_load)
    configure_logging(app)

    return app


def _add_file_handler(app, conf: dict):
    formatter_data = conf["FORMATTER"]
    handler_args = conf["HANDLER"]
    level = conf["LEVEL"]

    log_handler = RotatingFileHandler(**handler_args)
    # TODO: may be refactor for all args in one call pass
    log_handler.setLevel(level)

    log_formatter = logging.Formatter(**formatter_data)
    log_handler.setFormatter(log_formatter)

    app.logger.addHandler(log_handler)


def _add_ws_handler(app, socket_obj, conf):
    # handler_conf: dict = conf["HANDLER"]
    formatter_conf = conf["FORMATTER"]
    event_name = conf["EVENT_NAME"]
    level = conf["LEVEL"]

    websocket_handler = WebsocketHandler(socket_obj, event_name, level=level)
    formatter = logging.Formatter(**formatter_conf)
    websocket_handler.setFormatter(formatter)

    app.logger.addHandler(websocket_handler)


def configure_logging(app):
    # setup global logging level
    level = app.config["LOGGING"]["LEVEL"]
    app.logger.setLevel(level)

    # add rotating file handler with app config
    file_conf = app.config["LOGGING"]["FILE"]
    _add_file_handler(app, file_conf)

    # add websocket handler for realtime logs monitoring
    ws_conf = app.config["LOGGING"]["WS"]
    _add_ws_handler(app, socketio, ws_conf)
