import os.path

import sqlalchemy.exc
from flask import Flask
from sqlalchemy import text
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from dotenv import load_dotenv

from linker_app.database.base import metadata, IdModel
from linker_app.utils.argparse import clear_environ, get_env_vars_by_prefix
from linker_app.utils.config import load_config  # noqa: E402
from linker_app.utils.handlers import WebsocketHandler, LogBufferHandler, LogBuffer  # noqa: E402
from linker_app.rabbit_extension.rabbit import RQExtension

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ENV_VAR_PREFIX = "LINKER_APP_"
load_dotenv(".env")

socketio = SocketIO()
db = SQLAlchemy(model_class=IdModel, metadata=metadata)

# init migrations in db directory
migrate = Migrate(directory=os.path.join(BASE_DIR, "database", "migrations"))
csrf = CSRFProtect()
rabbit = RQExtension()

log_buffer = LogBuffer()


def create_app(conf_file: str = "config.yaml", **kwargs):
    app = Flask(__name__)

    # configure app
    # load map object from config file and env
    config = load_config(conf_file)
    env_vars = get_env_vars_by_prefix(ENV_VAR_PREFIX)

    # set or re-wright values from config file -> env vars -> kwargs
    app.config.from_mapping(config)
    app.config.from_mapping(env_vars)
    app.config.from_mapping(kwargs)

    # clear env vars for security reasons
    clear_environ(lambda i: i.startswith(ENV_VAR_PREFIX))
    # configure logging

    # TODO add configuration for all modules to use app logging

    # init all modules
    socketio.init_app(
        app,
        message_queue=app.config["MESSAGE_QUEUE"],
        channel=app.config["MESSAGE_QUEUE_CHANNEL"],
        cors_allowed_origins=app.config["CORS_ALLOWED_ORIGINS"],
        engineio_logger=True,
        logger=True,
        # engineio_logger= app.logger,
        # logger = app.logger,
    )
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    rabbit.init_app(app)

    from linker_app.utils.config import configure_logging
    configure_logging(app, socketio, log_buffer)

    from linker_app.main import bp

    app.register_blueprint(bp)

    return app
