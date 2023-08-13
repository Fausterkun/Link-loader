import logging
import os.path
import time

import pika
from pika import ConnectionParameters
from pika.exceptions import AMQPConnectionError

from linker_app.utils.config import BASE_CONFIG_NAME, load_config
from linker_app.service.validators import UrlValidator
from linker_app.service.exceptions import ValidationError, UrlValidationError
from linker_app import BASE_DIR

logger = logging.getLogger(__file__)

config = load_config(os.path.join(BASE_DIR, BASE_CONFIG_NAME))


def configure_logging(logger: logging.Logger):
    # setup handlers or communicate
    pass


def parse_file(file_name: str):
    file_dir_name = config.get('FILES_STORE_DIR')
    file_name += '.' + config.get("FILE_EXTENSION")
    file_path = os.path.join(BASE_DIR, file_dir_name, file_name)

    validators = [UrlValidator()]
    validated = []

    line_num = success_num = error_nums = 0
    try:
        with open(file_path, 'r') as file:
            line = file.readline()
            while line:
                line = line.replace('\n', "")
                for validator in validators:
                    try:
                        validator(line)
                        validated.append(line)
                        success_num += 1
                    except ValidationError:
                        logger.info(f"Validation error due parse line in file {file_name}.")
                        error_nums += 1
                line_num += 1
                line = file.readline()
        print('All links count: ', line_num)
        print('Success links count: ', success_num)
        print('Errors links count: ', error_nums)
        print('Success links: \n', validated)


    except FileNotFoundError:
        logger.error(f"Can't file not exist: {file_name}\nAt path: {file_path}")


def parse_worker():
    params = ConnectionParameters(
        host=config.get('RMQ_HOST', 'localhost'),
        port=config.get('RMQ_PORT', '5672'),
        heartbeat=0,
        socket_timeout=5,
    )
    connection = pika.BlockingConnection(parameters=params)
    channel = connection.channel()

    channel.queue_declare(
        queue=config.get('RMQ_QUEUE'),
        durable=config.get('RMQ_DURABLE')
    )
    print(' [*] Waiting for messages. To exit press CTRL+C')

    # as this one is sync app set 1 task at work at time
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=config.get("RMQ_QUEUE"),
        on_message_callback=callback
    )
    channel.start_consuming()


def main():
    retry_time = 15  # sec
    while True:
        try:
            parse_worker()
        except AMQPConnectionError as e:
            print(f'Connection error, try next in {retry_time} sec')
            logger.info(f"ConnectionError, try next in {retry_time} sec.\n{e}")
            time.sleep(retry_time)


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    f_name = body.decode()
    print(f' [x] Assume f_name is: {f_name}')
    parse_file(f_name)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    configure_logging(logger)
    main()
