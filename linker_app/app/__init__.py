import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Blueprint, Flask
from flask_socketio import SocketIO

from .logger import LogBufferLocal

socketio = SocketIO()

log_buffer = LogBufferLocal(max_size=20)
counter = 0
bp = Blueprint("linker_app", __name__)

app = Flask(__name__)  # , os.path.join(BASE_PATH, 'app/templates'))
from . import routes
