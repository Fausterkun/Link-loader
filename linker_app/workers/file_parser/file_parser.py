import sys
import time
import os.path
import logging
from logging import StreamHandler

import pika
from pika import ConnectionParameters
from pika.exceptions import AMQPConnectionError
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import create_engine

from linker_app import BASE_DIR
from linker_app.utils.query import parse_url
from linker_app.utils.config import BASE_CONFIG_NAME, load_config
from linker_app.database.schema import FileRequest
from linker_app.service.validators import UrlValidator
from linker_app.service.exceptions import ValidationError
from linker_app.workers.query import upsert_links_query

logger = logging.getLogger(__name__)

config = load_config(os.path.join(BASE_DIR, BASE_CONFIG_NAME))

db_url = config.get("SQLALCHEMY_DATABASE_URI")
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)


def configure_logging():
    # set log level and handler to stdout
    logger.setLevel(logging.INFO)
    stream_handler = StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def main():
    configure_logging()
    retry_time = 15  # sec
    while True:
        try:
            worker()
        except AMQPConnectionError as e:
            print(f"Connection error, try next in {retry_time} sec")
            logger.info(f"ConnectionError, try next in {retry_time} sec.\n{e}")
            time.sleep(retry_time)


def worker():
    params = ConnectionParameters(
        host=config.get("RMQ_HOST", "localhost"),
        port=config.get("RMQ_PORT", "5672"),
        heartbeat=0,
        socket_timeout=5,
    )
    connection = pika.BlockingConnection(parameters=params)
    channel = connection.channel()

    channel.queue_declare(
        queue=config.get("RMQ_QUEUE"), durable=config.get("RMQ_DURABLE")
    )
    print(" [*] Waiting for messages. To exit press CTRL+C")

    # as this one is sync app set 1 task at work at time
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=config.get("RMQ_QUEUE"), on_message_callback=callback)
    channel.start_consuming()


def callback(ch, method, properties, body):
    f_name = body.decode()
    logger.info(f" [x] Received message with filename: {f_name}")
    try:
        links, all_urls, success_count, fail_count = parse_file(f_name)
        with Session() as session:
            query = upsert_links_query(engine=engine, links=list(links.values()))
            session.execute(query)
            file_request_query = (
                update(FileRequest)
                .where(FileRequest.uuid == f_name)
                .values(
                    fail_count=fail_count,
                    success_count=success_count,
                    all_urls=all_urls,
                    finished=True,
                )
            )
            session.execute(file_request_query)
            session.commit()
        logger.info(
            f"Add {success_count} links in db by file request {f_name}:\n{links.keys()}"
        )
        logger.info(f"Add links in db: {links.keys()}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # print(" [x] Done")
        logger.info(" [x] Done")
    except FileNotFoundError:
        logger.error(f"Can't file not exist: {f_name}")

    except SQLAlchemyError as e:
        logger.error(f"Can't save links in db\n{e}")


def parse_file(file_name: str) -> tuple[dict[str, dict], int, int, int]:
    """
    Parse and count links in file, duplicated marked as successful
    return: links: dict[url: parsed_url], all_urls:int, success_count:int, fail_count: int
    """
    file_dir_name = config.get("FILES_STORE_DIR")
    file_name += "." + config.get("FILE_EXTENSION")
    file_path = os.path.join(BASE_DIR, file_dir_name, file_name)

    validator = UrlValidator()
    # use url as key in dict for remove duplicates in one query
    links = dict()

    all_urls = success_count = fail_count = 0
    with open(file_path, "r") as file:
        line = file.readline()
        while line:
            line = line.replace("\n", "")
            try:
                # validate line
                validator(line)
                # parse it
                links[line] = parse_url(line)
                success_count += 1
            except ValidationError:
                logger.info(f"Validation error due parse line in file {file_name}.")
                fail_count += 1
            all_urls += 1
            line = file.readline()
    return links, all_urls, success_count, fail_count


if __name__ == "__main__":
    main()
