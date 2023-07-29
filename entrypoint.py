# from flask.cli import cli
import eventlet

eventlet.monkey_patch()
from linker_app import create_app, socketio

if __name__ == "__main__":
    app = create_app()
    socketio.run(app, port=8000, host='0.0.0.0')  # , cors_allowed_origins="*")
