import glob
import queue
import logging
from main import app


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
    def __init__(self, buffer_obj, max_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer_obj = buffer_obj
        self.size = max_size

    def emit(self, record: logging.LogRecord) -> None:
        if len(self.buffer_obj) >= self.size:
            self.buffer_obj.pop(-1)
        log = dict(level=record.levelname)
        self.buffer_obj.append(dict(level=record.levelname, message=self.formatter.format(record)))

# def get_last_file_logs(count: int | None = None):
#     """ Get last logs from `"""
#     # init from config
#     if not count:
#         count = logging_conf["SHOWN_DEFAULT"]
#
#     log_files = sorted(app.logger)
