from flask import Flask
from flask_socketio import SocketIO

from flask_sqlalchemy import SQLAlchemy

from linker_app.utils.logger import LogBuffer

socketio = SocketIO()
db = SQLAlchemy()

counter = 0
log_buffer = LogBuffer()

from linker_app.utils.config import load_config


def create_app(conf_file="config.yaml", **kwargs):
    app = Flask(__name__)

    # configure app
    config = load_config(conf_file)
    # config.update(**kwargs)
    # app.config.from_file(conf_file, load=yaml.safe_load)
    app.config.from_mapping(config, **kwargs)
    from linker_app.utils.config import configure_logging
    configure_logging(app)

    # init modules
    socketio.init_app(app)
    db.init_app(app)

    from linker_app.main import bp
    app.register_blueprint(bp)

    # from linker_app.api import bp
    # app.register_blueprint(bp, url_prefix='/api')

    return app
