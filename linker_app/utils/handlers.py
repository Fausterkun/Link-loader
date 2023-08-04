import logging
import copy
from logging.handlers import RotatingFileHandler


class LogBuffer(object):
    """
    Object for store last logs in RAM
    Used for quick last system log access
    """

    def __init__(self, max_size: int = 50):
        # TODO: create reading from log files for init logs after app restart
        self._max_size = 0
        self.max_size = max_size
        self._size = 0
        self._buffer = []

    def add_message(self, message: dict):
        if self.max_size <= self._size:
            self._buffer.pop(0)
        self._buffer.append(message)
        self._size += 1

    def get_last(self):
        return copy.copy(self._buffer)

    @property
    def size(self):
        return self._size

    @property
    def max_size(self):
        return self._max_size

    @max_size.setter
    def max_size(self, new_max_size):
        if not isinstance(new_max_size, int):
            raise TypeError("max_size value must be a int")

        if new_max_size < 1:
            raise ValueError("max size must have value more than 0")
        if hasattr(self, "max_size"):
            # TODO: test it
            if new_max_size < self.max_size:
                self._buffer = self.__buffer[-new_max_size:]
        self._max_size = new_max_size

    def __len__(self):
        return self.__size

    @size.setter
    def size(self, value):
        self._size = value


class HandlerNotImplemented(ValueError):
    """ Handler with that name doesn't exist """


class WebsocketHandler(logging.Handler):
    """Log handler for emit log message to the socketio object"""

    def __init__(self, event_name, namespace, *args, **kwargs):
        from linker_app import socketio
        self._socketio = socketio  # current_app.extensions['socketio']
        self.event = event_name
        self.namespace = namespace
        super().__init__(*args, **kwargs)

    def emit(self, record: logging.LogRecord) -> None:
        self._socketio.emit(
            event=self.event,
            namespace=self.namespace,
            data=dict(
                message=self.formatter.format(record),
                level=record.levelname,
            )
        )


class LogBufferHandler(logging.Handler):
    """Logging handler for store new event in local LogBuffer object"""

    def __init__(self, max_size=50, *args, **kwargs):
        from linker_app import log_buffer
        self._buffer_obj: LogBuffer = log_buffer
        self._buffer_obj.max_size = max_size

        super().__init__(*args, **kwargs)

    def emit(self, record: logging.LogRecord) -> None:
        self._buffer_obj.add_message(
            dict(
                message=self.formatter.format(record),
                level=record.levelname
            )
        )


DEFAULT_FORMATTER = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")
BASE_HANDLERS = {
    "RotatingFileHandler": RotatingFileHandler,
}
CUSTOM_HANDLERS = {
    'WS': WebsocketHandler,
    "BUFFER": LogBufferHandler,
}
