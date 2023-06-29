from flask import Blueprint
from flask_socketio import SocketIO

# socketio = SocketIO(message_queue='redis://')

socketio = SocketIO()
bp = Blueprint("main", __name__)

from .app import create_app

app = create_app()

from . import routes

app.register_blueprint(bp)
socketio.init_app(app)
