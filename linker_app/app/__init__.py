from flask import Blueprint, Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .logger import LogBuffer

from dotenv import load_dotenv

load_dotenv(".env")

socketio = SocketIO()

log_buffer = LogBuffer(max_size=20)
counter = 0
bp = Blueprint("linker_app", __name__)

app = Flask(__name__)  # , os.path.join(BASE_PATH, 'app/templates'))
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

from . import routes

app.register_blueprint(bp)
