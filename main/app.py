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
    # load config from yaml file
    app.config.from_file(str(BASE_PATH) + '/config.yaml', load=yaml.safe_load)
    return app

app = create_app()
from routes import *

def configure_logging():
    handler_args = app.config['LOGGING']['HANDLER']
    level = app.config["LOGGING"]['LEVEL']
    format = app.config['LOGGING']['FORMATTER']['format']

    log_handler = RotatingFileHandler(**handler_args)
    log_handler.setLevel(level)
    log_formatter = logging.Formatter(format)
    log_handler.setFormatter(log_formatter)

    app.logger.addHandler(log_handler)

configure_logging()
if __name__ == '__main__':
    app.run()
