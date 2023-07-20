from flask_socketio import SocketIO
from socketio import Server


def create_app():
    message_queue = "redis://localhost:6379/"
    # socketio = SocketIO(message_queue=message_queue)


class APP:
    def __init__(self, socketio, eventname):
        self.event_name = eventname
        self.socketio = socketio

    def _send_ws_signals_forever(self):
        while True:
            self.socketio.emit(self.event_name, {"data": "hello"}, namespace="/test")

    def __call__(self, *args, **kwargs):
        self._send_ws_signals_forever()
