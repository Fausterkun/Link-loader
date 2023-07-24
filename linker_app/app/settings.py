import os

import yaml
import logging

from pathlib import Path

# from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

from . import socketio, log_buffer
from .logger import WebsocketHandler, LogBufferHandler

BASE_PATH = Path(__file__).resolve().parent.parent.parent


def init_socketio(socketio, app, **kwargs):
    configs = app.config["SOCKETIO"]
    # update config vars from cmd kwargs
    configs.update(kwargs)
    socketio.init_app(app, **configs)


def configure_app(app, conf_file: str = "config.yaml", args=None):
    """load config from file and configure it"""
    if not os.path.isabs(conf_file):
        conf_file = os.path.join(BASE_PATH, conf_file)

    if not conf_file.endswith(".yaml"):
        raise FileNotFoundError(
            f"Yaml config file not found in project directory, check that {conf_file} exist."
        )

    app.config.from_file(conf_file, load=yaml.safe_load)
    if hasattr(app.config, "LOGGING"):
        configure_logging(app, args)


def configure_logging(app, args=None):
    """Set logger level and add necessary handlers"""

    logging_conf = app.config["LOGGING"]

    # setup global logging level
    level = logging_conf["LEVEL"]
    app.logger.setLevel(level)

    # add rotating file handler with app config
    file_conf = logging_conf["FILE"]
    _add_file_handler(app, file_conf)

    # add buffer handler for store all new log in memory
    buffer_conf = logging_conf["BUFFER"]
    # add log buffer obj to handler and configure it
    _add_buffer_handler(app, log_buffer, buffer_conf, args)

    # add websocket handler for realtime logs monitoring
    ws_conf = logging_conf["WS"]
    _add_ws_handler(app, socketio, ws_conf)

    # config log buffer:


def _add_file_handler(app, conf: dict):
    """Add rotation file log handler"""
    formatter_data = conf["FORMATTER"]
    handler_args = conf["HANDLER"]
    level = conf["LEVEL"]

    handler = RotatingFileHandler(**handler_args)
    # TODO: may be refactor for all args in one call pass
    handler.setLevel(level)

    log_formatter = logging.Formatter(**formatter_data)
    handler.setFormatter(log_formatter)

    app.logger.addHandler(handler)


def _add_buffer_handler(app, buffer_obj, conf, args):
    """Setup buffer obj and set handler that store all new logs"""
    formatter_conf = conf["FORMATTER"]
    level = conf["LEVEL"]

    # setup max buffer size from args or config
    max_size = 50  # default value
    # re-assign if value in args or conf
    if args.log_buffer_size:
        max_size = args.log_buffer_size
    elif "LOG_BUFFER_SIZE" in conf:
        max_size = conf["LOG_BUFFER_SIZE"]
    log_buffer.update_size(max_size)

    # create handler
    handler = LogBufferHandler(buffer_obj=buffer_obj)
    handler.setLevel(level)

    # setup formatter for handler
    formatter = logging.Formatter(**formatter_conf)
    handler.setFormatter(formatter)

    # add handler to loger
    app.logger.addHandler(handler)
    app.logger_buffer = log_buffer


def _add_ws_handler(app, socket_obj, conf):
    """
    Set handler for real-time notification through ws connection to all connected clients
    """
    # handler_conf: dict = conf["HANDLER"]
    formatter_conf = conf["FORMATTER"]
    event_name = conf["EVENT_NAME"]
    namespace = conf["NAMESPACE"]
    level = conf["LEVEL"]

    handler = WebsocketHandler(socket_obj, event_name, level=level, namespace=namespace)
    formatter = logging.Formatter(**formatter_conf)
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
