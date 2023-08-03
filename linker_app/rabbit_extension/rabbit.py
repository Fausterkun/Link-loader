import logging

import yaml
import pika
from pika import BlockingConnection, ConnectionParameters, BasicProperties
from pika.exceptions import AMQPConnectionError

log = logging.getLogger(__name__)


class RQExtension:
    def __init__(self, app=None):
        self._queue_name = None
        self._host = None
        self._port = None
        self.log = log

        self._connection = None
        self._channel = None
        # use persistent messages all time:
        self._properties = BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self._host = app.config["RMQ_HOST"]
        self._port = app.config["RMQ_PORT"]
        # TODO: add more settings (port, etc..)

        # try to create connection
        try:
            self._connect()
        except AMQPConnectionError:
            self.log.error("RabbitMQ is not connected.")
        app.extensions["rabbitmq"] = self

    def _connect(self):
        self._connection = BlockingConnection(ConnectionParameters(self._host))
        self._channel = self._connection.channel()

    @property
    def channel(self):
        return self._channel

    def send_message(self, routing_key, exchange="", *messages):
        """send message to the broker"""
        if not self.app:
            raise AttributeError("App must be initialized before send messages.")

        if self._connection is None:
            try:
                self._connect()
            except AMQPConnectionError:
                self.log.error("RabbitMQ is not connected.")

        with self._connection.channel() as channel:
            # ensure that queue exists
            channel.queue_declare(self._queue_name)
            # TODO: test if rabbit failed
            try:
                for message in messages:
                    self.channel.bassic_publish(
                        exchange=exchange,
                        routing_key=routing_key,
                        body=message,
                        properties=self._properties,
                    )

            except AMQPConnectionError:
                return False
            # TODO: add ack
        return True
