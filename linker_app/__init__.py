import os.path

import sqlalchemy.exc
from flask import Flask
from sqlalchemy import text

# from redis import connection
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from dotenv import load_dotenv

from linker_app.db.schema import metadata
from linker_app.utils.logger import LogBuffer
from linker_app.utils.argparse import clear_environ, get_env_vars_by_prefix

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ENV_VAR_PREFIX = "LINKER_APP_"
load_dotenv(".env")

socketio = SocketIO()
db = SQLAlchemy(metadata=metadata)

# init migrations in db directory
migrate = Migrate(directory=os.path.join(BASE_DIR, "db", "migrations"))
csrf = CSRFProtect()

counter = 0
log_buffer = LogBuffer()

from linker_app.utils.config import load_config  # noqa: E402


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
    from linker_app.utils.config import configure_logging

    configure_logging(app)
    # TODO add configuration for all modules to use app logging

    # init all modules
    socketio.init_app(
        app,
        message_queue=app.config["MESSAGE_QUEUE"],
        channel=app.config["MESSAGE_QUEUE_CHANNEL"],
        cors_allowed_origins=app.config["CORS_ALLOWED_ORIGINS"],
        **app.config["SOCKETIO"]
    )
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Check connection to database and redis mq:
    with app.app_context():
        try:
            _ = db.session.query(text("1")).from_statement(text("SELECT 1")).first
            # register routes:
            app.logger.info("Database ready to accept connections.")
        except sqlalchemy.exc.SQLAlchemyError:
            app.logger.error(
                "Cannot connect to database, check url, connection and try again"
            )
            # print("Cannot connect to database, check url, connection and try again")
            exit(128)
        # TODO check also redis

    from linker_app.main import bp

    app.register_blueprint(bp)

    # from linker_app.api import bp
    # app.register_blueprint(bp, url_prefix='/api')

    return app
