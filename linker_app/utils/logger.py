import copy
import logging


class HandlerNotImplemented(ValueError):
    """Handler with that name doesn't exist"""


class LogBuffer:
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


class WebsocketHandler(logging.Handler):
    """Log handler for emit log message to the socketio object"""

    def __init__(self, socket_obj, event_name, namespace, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket_obj = socket_obj
        self.event_name = event_name
        self.namespace = namespace

    def emit(self, record: logging.LogRecord) -> None:
        self.socket_obj.emit(
            event="new_log",
            namespace="/logs",
            data={"message": self.formatter.format(record), "level": record.levelname},
        )


class LogBufferHandler(logging.Handler):
    """Logging handler for store new event in local LogBuffer object"""

    def __init__(self, log_buffer: LogBuffer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._log_buffer = log_buffer

    def emit(self, record: logging.LogRecord) -> None:
        self._log_buffer.add_message(
            dict(level=record.levelname, message=self.formatter.format(record))
        )
