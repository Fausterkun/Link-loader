import logging


class WebsocketHandler(logging.Handler):
    def __init__(self, socket_obj, event_name, namespace, *args, **kwargs):
        self.socket_obj = socket_obj
        self.event_name = event_name
        self.namespace = namespace
        super().__init__(*args, **kwargs)

    def emit(self, record: logging.LogRecord) -> None:
        # self.socket_obj.emit(event='new_log', data={'logs': record.getMessage()}, namespace="/logs")
        self.socket_obj.emit(event='new_log', data={'logs': self.formatter.format(record)}, namespace="/logs")
        # self.socket_obj.emit(event=self.event_name, data={'logs': record.getMessage()}, namespace=self.namespace)
