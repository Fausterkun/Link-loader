
import yaml
import logging

from pathlib import Path

# from dotenv import load_dotenv

from linker_app import socketio, log_buffer

from linker_app import app

BASE_PATH = Path(__file__).resolve().parent.parent.parent


# def init_socketio(socketio, app, **kwargs):
#     configs = app.config["SOCKETIO"]
#     # update config vars from cmd kwargs
#     configs.update(kwargs)
#     socketio.init_app(app, **configs)


# def configure_app(app, conf_file: str = "config.yaml", args=None):
#     """load config from file and configure it"""
#     if not os.path.isabs(conf_file):
#         conf_file = os.path.join(BASE_PATH, conf_file)
#
#     if not conf_file.endswith(".yaml"):
#         raise FileNotFoundError(
#             f"Yaml config file not found in project directory, check that {conf_file} exist."
#         )
#
#     app.config.from_file(conf_file, load=yaml.safe_load)
#     if hasattr(app.config, "LOGGING"):
#         configure_logging(app, args)
#
#     # create db engine and set it in g context
#     from linker_app.db import init_engine
#     init_engine()
#

# def init_db():
#     db = create_engine(
#         app.config['SQLALCHEMY_DATABASE_URI'],
#         pool_size=app.config['SQLALCHEMY_POOL_SIZE'],
#         max_overflow=app.config['SQLALCHEMY_MAX_OVERFLOW'],
#         pool_timeout=app.config['SQLALCHEMY_TIMEOUT'],
#         echo=True,
#         echo_pool=True
#     )
#     return db
#



