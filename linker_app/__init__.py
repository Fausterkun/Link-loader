# import eventlet
# eventlet.monkey_patch()

from flask import Blueprint
from flask_socketio import SocketIO

from linker_app.logger import LogBufferLocal

# message_queue = "redis://redis:6379/"
socketio = SocketIO()
# socketio = SocketIO(
#     message_queue=message_queue,
#     channel="linker_socketio",
#     logger=True,
#     engineio_logger=True,
#     cors_allowed_origins="*",
# )
#TODO: update to setup this from settings
log_buffer = LogBufferLocal(max_size=20)
counter = 0
bp = Blueprint("linker_app", __name__)

from .app import create_app, init_socketio

app = create_app()

init_socketio(socketio, app)
# socketio.init_app(app)  # , engineio_logger=app.logger)
from . import routes

app.register_blueprint(bp)
