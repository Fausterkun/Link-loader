# from gevent import monkey
# monkey.patch_all()

import eventlet

eventlet.monkey_patch()

from flask import Blueprint
from flask_socketio import SocketIO

message_queue = "redis://localhost:6379/"
socketio = SocketIO(message_queue=message_queue, channel='linker_socketio')
log_buffer = list()
bp = Blueprint("main", __name__)

from .app import create_app

app = create_app()
socketio.init_app(app)  # , engineio_logger=app.logger)
from . import routes

app.register_blueprint(bp)
