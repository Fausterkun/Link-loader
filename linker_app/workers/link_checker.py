import sys
import os
import asyncio
import datetime
import logging
from logging import StreamHandler
import multiprocessing

import aiohttp
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import select

from linker_app import BASE_DIR
from linker_app.database.schema import Links
from linker_app.utils.config import BASE_CONFIG_NAME, load_config
from linker_app.workers.exceptions import WorkerError, ConnectionToDatabaseError

logger = logging.getLogger(__name__)

config = load_config(os.path.join(BASE_DIR, BASE_CONFIG_NAME))
postgres_db_url = config.get("SQLALCHEMY_DATABASE_URI")

postgres_engine = create_engine(postgres_db_url)
PostgresSession = sessionmaker(bind=postgres_engine)

# local sqlite database used if postgresql database is not available
sqlite_db_url = config.get("SQLITE_DATABASE_URI")
sqlite_engine = create_engine(sqlite_db_url)

proc_num = config.get("WORKER_PROC_NUM", os.cpu_count() or 1)
cpu_count = os.cpu_count()
if cpu_count and proc_num > cpu_count:
    logger.warning("proc_number more than cpu count. This may be not optimal setting.")

chunk_size = config.get("CHUNK_SIZE", 1000)
request_timeout = config.get('REQUEST_TIMEOUT')


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
    logger.info(f'Start Link checker task')

    time_start = datetime.datetime.now()
    # call parallel parser process
    try:
        host_proces()
    except WorkerError as e:
        logger.error(f"Error due check links status code worker. Process not finished.\n{e}")
    processed_time = datetime.datetime.now() - time_start

    max_predicted_time = datetime.timedelta(minutes=10)
    if processed_time > max_predicted_time:
        logger.warning(
            f"Processing time more than predicted period({max_predicted_time}). Processed time: {processed_time}"
        )
    else:
        logger.info(f'Link checker task complete at time: {processed_time}')


def host_proces():
    logger.info(f'Start check links status code. Chunk size: {chunk_size}')
    urls = get_urls()
    chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]
    with multiprocessing.Pool(processes=proc_num) as pool:
        result = pool.map(handle_urls, chunks)
    for _ in result:
        pass


def get_urls():
    try:
        with PostgresSession() as session:
            links = [_[0] for _ in session.query(Links.url).filter(Links.unavailable_times < 4).all()]
        return links
    except SQLAlchemyError as e:
        logger.error('Error due try to get links from db \n', e)
        raise ConnectionToDatabaseError("Can't get actual links from database.")


def handle_urls(urls: list[str]):
    pid = os.getpid()
    logger.info(f'Start handle urls from {pid}')
    # TODO: think about send result into db
    loop = asyncio.get_event_loop()
    tasks = [get_status_code(url) for url in urls]
    result = loop.run_until_complete(asyncio.gather(*tasks))
    logger.info(f'Finish handle urls from {pid}')
    return result


async def get_status_code(url: str):
    pid = os.getpid()
    async with aiohttp.ClientSession() as session:
        try:
            status_code = None
            async with session.get(url, timeout=request_timeout) as response:
                logger.info(f"In process: {pid}. Response code: {response.status} url: {url}")
                status_code = response.status

        except asyncio.TimeoutError as e:
            logger.warning(f"In process: {pid}. Can't process {url} timeout error: \n{e}")
        except aiohttp.ClientError as e:
            logger.warning(f"In process: {pid}. Can't process {url} client error occur: \n{e}")

        return url, status_code


if __name__ == '__main__':
    configure_logging()
    main()
