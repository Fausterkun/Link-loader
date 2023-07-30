import logging
from logging.handlers import RotatingFileHandler

import yaml

from linker_app import log_buffer, socketio
from linker_app.utils.logger import WebsocketHandler, LogBufferHandler


def load_config(file_path):
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def configure_logging(app):
    """Set logger level and add necessary handlers"""

    # config log buffer:
    logging_conf = app.config["LOGGING"]

    # setup global logging level
    level = logging_conf["LEVEL"]
    app.logger.setLevel(level)

    # add rotating file handler with app config
    file_conf = logging_conf["FILE"]
    _add_file_handler(app, file_conf)

    # add buffer handler for store all new log in memory
    buffer_conf = logging_conf.get("BUFFER", None)
    if buffer_conf:
        # add log buffer obj to handler and configure it
        _add_buffer_handler(app, log_buffer, buffer_conf)

    # add websocket handler for realtime logs monitoring
    ws_conf = logging_conf["WS"]
    _add_ws_handler(app, socketio, ws_conf)


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


def _add_buffer_handler(app, buffer_obj, conf):
    """Setup buffer obj and set handler that store all new logs"""
    formatter_conf = conf["FORMATTER"]
    level = conf["LEVEL"]

    # setup max buffer size from args or config
    max_size = 50  # default value
    # re-assign if value in args or conf
    if "LOG_BUFFER_SIZE" in conf:
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
