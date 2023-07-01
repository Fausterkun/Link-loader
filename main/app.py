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


#
# def _add_file_handler(app, conf: dict):
#     formatter_data = conf["FORMATTER"]
#     handler_args = conf["HANDLER"]
#     level = conf["LEVEL"]
#
#     handler = RotatingFileHandler(**handler_args)
#     # TODO: may be refactor for all args in one call pass
#     handler.setLevel(level)
#
#     log_formatter = logging.Formatter(**formatter_data)
#     handler.setFormatter(log_formatter)
#
#     app.logger.addHandler(handler)
#
#
# def _add_ws_handler(app, socket_obj, conf):
#     # handler_conf: dict = conf["HANDLER"]
#     formatter_conf = conf["FORMATTER"]
#     event_name = conf["EVENT_NAME"]
#     namespace = conf["NAMESPACE"]
#     level = conf["LEVEL"]
#
#     handler = WebsocketHandler(socket_obj, event_name, level=level, namespace=namespace)
#     formatter = logging.Formatter(**formatter_conf)
#     handler.setFormatter(formatter)
#
#     app.logger.addHandler(handler)
#
#
# def configure_logging(app):
#     # setup global logging level
#     level = logging_conf["LEVEL"]
#     app.logger.setLevel(level)
#
#     # add rotating file handler with app config
#     file_conf = logging_conf["FILE"]
#     _add_file_handler(app, file_conf)
#
#     # add websocket handler for realtime logs monitoring
#     ws_conf = logging_conf["WS"]
#     _add_ws_handler(app, socketio, ws_conf)
