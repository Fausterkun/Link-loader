import os.path
import pathlib

import sqlalchemy.exc
from flask import Flask
from sqlalchemy import text
# from redis import connection
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

from linker_app.utils.logger import LogBuffer
from linker_app.db.schema import metadata

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

socketio = SocketIO()
db = SQLAlchemy(metadata=metadata)
# init migrations in db directory
migrate = Migrate(directory=os.path.join(BASE_DIR, 'db', 'migrations'))
csrf = CSRFProtect()

counter = 0
log_buffer = LogBuffer()

from linker_app.utils.config import load_config


def create_app(conf_file="config.yaml", **kwargs):
    app = Flask(__name__)

    # configure app
    config = load_config(conf_file)
    app.config.from_mapping(config, **kwargs)

    # configure logging
    from linker_app.utils.config import configure_logging
    configure_logging(app)
    # TODO add configuration for all modules to use app logging

    # init all modules
    socketio.init_app(app, **app.config['SOCKETIO'])
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Check connection to database and redis mq:
    with app.app_context():
        try:
            result = db.session.query(text("1")).from_statement(text("SELECT 1")).first  # register routes:
            app.logger.info("Database ready to accept connections.")
        except sqlalchemy.exc.SQLAlchemyError:
            app.logger.error("Cannot connect to database, check url, connection and try again")
            # print("Cannot connect to database, check url, connection and try again")
            exit(128)
        # TODO check also redis

    from linker_app.main import bp
    app.register_blueprint(bp)

    # from linker_app.api import bp
    # app.register_blueprint(bp, url_prefix='/api')

    return app
