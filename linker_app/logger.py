import logging


class LogBufferLocal:
    def __init__(self, max_size: int):
        # TODO: create reading from log files for init logs after app restart
        self._max_size = max_size
        if self._max_size < 1:
            raise ValueError("max size must have value more than 0")

        self._size = 0
        self._buffer = []

    def add_message(self, message: dict):
        if self._max_size <= self._size:
            self._buffer.pop(0)
        self._buffer.append(message)
        self._size += 1

    def get_all(self):
        return self._buffer


class WebsocketHandler(logging.Handler):
    def __init__(self, socket_obj, event_name, namespace, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket_obj = socket_obj
        self.event_name = event_name
        self.namespace = namespace

    def emit(self, record: logging.LogRecord) -> None:
        # self.socket_obj.emit(event='new_log', data={'logs': record.getMessage()}, namespace="/logs")
        self.socket_obj.emit(
            event="new_log",
            data={"message": self.formatter.format(record), "level": record.levelname},
            namespace="/logs",
        )
        # self.socket_obj.emit(event=self.event_name, data={'logs': record.getMessage()}, namespace=self.namespace)


class LogBufferHandler(logging.Handler):
    def __init__(self, buffer_obj: LogBufferLocal, max_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._buffer_obj = buffer_obj
        self.size = max_size

    def emit(self, record: logging.LogRecord) -> None:
        self._buffer_obj.add_message(
            dict(level=record.levelname, message=self.formatter.format(record))
        )
