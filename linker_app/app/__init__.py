from flask import Blueprint, Flask
from flask_socketio import SocketIO

from .logger import LogBuffer

socketio = SocketIO()

log_buffer = LogBuffer(max_size=20)
counter = 0
bp = Blueprint("linker_app", __name__)

app = Flask(__name__)  # , os.path.join(BASE_PATH, 'app/templates'))
from . import routes

app.register_blueprint(bp)
