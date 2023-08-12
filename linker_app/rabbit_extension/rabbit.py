import logging

import pika
from pika import BlockingConnection, ConnectionParameters, BasicProperties
from pika.exceptions import AMQPConnectionError, ConnectionClosed

from linker_app.service.exceptions import SendToQueueError, QueueConnectionError

logger = logging.getLogger(__name__)


class RQExtension:
    def __init__(self, app=None):
        self.app = None
        self._durable = None
        self._queue_name = None
        self._host = None
        self._port = None
        self.logger = logger

        self._connection = None

        # use persistent messages all time:
        self._properties = BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.logger = self.app.logger
        self._host = app.config["RMQ_HOST"]
        self._port = app.config["RMQ_PORT"]
        self._queue_name = app.config["RMQ_QUEUE"]
        self._durable = app.config["RMQ_DURABLE"]
        # TODO: add more settings (port, etc..)

        # try to create connection
        self._connect()
        app.extensions["rabbitmq"] = self

    def _connect(self):
        self.logger.info('Try to connect to RabbitMQ')
        params = ConnectionParameters(
            host=self._host,
            port=self._port,
            heartbeat=0,
            socket_timeout=5,
        )
        try:
            self._connection = BlockingConnection(params)
        except AMQPConnectionError as e:
            self.logger.error(f"Can't connect to RabbitMQ\n{e}")

    def send_messages(self, routing_key, *messages):
        exchange = ""
        """ Send message to the broker """
        self.logger.info(f'Send message call for queue {routing_key} got messages: {messages}')
        if not self.app:
            self.logger.error("App must be initialized before send message to rabbit")
            raise AttributeError("App must be initialized before send messages.")

        if self._connection is None:
            self._connect()

        try:
            with self._connection.channel() as channel:
                # by rabbitmq doc we must declare queue first, no matter exist it or not
                channel.queue_declare(self._queue_name, durable=self._durable)
                self.logger.info(f'Declare queue {self._queue_name}')
                for message in messages:
                    self.logger.info(f'Publish message {messages}')
                    channel.basic_publish(
                        exchange=exchange,  # we have no exchange by default
                        routing_key=routing_key,
                        body=message,
                        properties=self._properties,
                    )
        except ConnectionClosed as e:
            # TODO: may be add some recursion call with inner counter for try to reconnect
            self.logger.error(f'Connection error due send message to queue {routing_key}\n{e}')
            self._connection = None  # reset connection for try to open it in next time
            raise QueueConnectionError(f'Error due send message to queue: {routing_key}')

        except AMQPConnectionError as e:
            self.logger.error(f'Error due send message to queue {routing_key}\n{e}')
            raise SendToQueueError(f'Error due send message to queue: {routing_key}')

    @property
    def channel(self):
        return self._channel
