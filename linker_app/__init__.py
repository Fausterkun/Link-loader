import os.path
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from dotenv import load_dotenv

from linker_app.database.base import metadata, IdModel
from linker_app.utils.argparse import clear_environ, get_env_vars_by_prefix
from linker_app.utils.config import load_config  # noqa: E402
from linker_app.utils.logger import LogBuffer  # noqa: E402

from linker_app.rabbit_extension.rabbit import RQExtension
from linker_app.utils.config import BASE_FILES_STORE_DIR

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

    # create dir for files
    file_dir = app.config.get('FILES_STORE_DIR', None)
    if not file_dir:
        file_dir = BASE_FILES_STORE_DIR
    file_path = os.path.join(BASE_DIR, file_dir)
    os.makedirs(file_path, exist_ok=True)

    # set default(in memory) message queue while debug
    if os.environ.get("FLASK_DEBUG"):
        socketio.init_app(
            app,
            cors_allowed_origins=app.config["CORS_ALLOWED_ORIGINS"],
            engineio_logger=True,
            logger=True,
            # engineio_logger= app.logger,
            # logger = app.logger,
        )
    else:
        # if not debug, then set external message queue from config
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
    # init all modules
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from linker_app.utils.config import configure_logging
    configure_logging(app, socketio, log_buffer)

    # register routes from all modules:
    from linker_app.main import bp
    app.register_blueprint(bp)

    return app
