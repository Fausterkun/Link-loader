import logging
import os.path
import time

import pika
from pika import ConnectionParameters
from pika.exceptions import AMQPConnectionError

from linker_app.utils.config import BASE_CONFIG_NAME, load_config
from linker_app import BASE_DIR

logger = logging.getLogger(__file__)


def configure_logging(logger: logging.Logger):
    # setup handlers or communicate
    pass


def parse_file(file_name: str, file_dir_name: str):
    file_path = os.path.join(BASE_DIR, file_dir_name, file_name)
    try:
        with open(file_path, 'r'):
            pass

    except FileNotFoundError:
        logger.error("Can't file not exist: ", file_name, '\n', 'At path: ', file_path)


def parse_worker():
    config = load_config(os.path.join(BASE_DIR, BASE_CONFIG_NAME))
    host = config.get('RMQ_HOST', 'localhost')
    port = config.get('RMQ_PORT', '5672')
    queue = config.get('RMQ_QUEUE')
    durable = config.get('RMQ_DURABLE')

    params = ConnectionParameters(
        host=host,
        port=port,
        heartbeat=0,
        socket_timeout=5,
    )
    connection = pika.BlockingConnection(parameters=params)
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=durable)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    # as this one is sync app set 1 task at work at time
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)

    channel.start_consuming()


def main():
    retry_time = 15000  # sec
    while True:
        try:
            parse_worker()
        except AMQPConnectionError as e:
            print(f'Connection error, try next in {retry_time / 1000} sec')
            logger.info(f"ConnectionError, try next in {retry_time / 1000} sec.\n{e}")
            time.sleep(retry_time)


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    # print('\n'.join([ch, method, properties, body]))
    f_name = body.decode()
    print('Assume f_name is: ', f_name)
    # parse_file(f_name)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    configure_logging(logger)
    main()
