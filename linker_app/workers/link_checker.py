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

from linker_app import BASE_DIR
from linker_app.utils.config import BASE_CONFIG_NAME, load_config

logger = logging.getLogger(__name__)

config = load_config(os.path.join(BASE_DIR, BASE_CONFIG_NAME))
postgres_db_url = config.get("SQLALCHEMY_DATABASE_URI")

postgres_engine = create_engine(postgres_db_url)
PostgresSession = sessionmaker()

# local sqlite database used if postgresql database is not available
sqlite_db_url = config.get("SQLITE_DATABASE_URI")
sqlite_engine = create_engine(sqlite_db_url)

proc_num = config.get("WORKER_PROC_NUM", os.cpu_count() or 1)


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
    # count time start
    time_start = datetime.datetime.now()
    configure_logging()
    # call host process
    host_proces()
    # count processed_time
    processed_time = datetime.datetime.now() - time_start
    max_predicted_time = datetime.timedelta(minutes=10)
    if processed_time > max_predicted_time:
        logger.warning(
            f"Processing time more than predicted period({max_predicted_time}). Processed time: {processed_time}"
        )
    else:
        logger.info(f'Task complete  at time: {processed_time}')


def host_proces():
    urls = [str(_) for _ in range(1000)]
    chunk_size = 7
    chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]
    with multiprocessing.Pool(processes=proc_num) as pool:
        result = pool.map(handle_urls, chunks)
    print('Host process result: ', result)
    for res_chunk in result:
        print(res_chunk)

    # save it in db


def handle_urls(urls: list[str]):
    loop = asyncio.get_event_loop()
    tasks = [get_status_code(url) for url in urls]
    result = loop.run_until_complete(asyncio.gather(*tasks))
    return result


async def get_status_code(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                logger.error(f"In process: {os.getpid()}. Response code: {response.status} url: {url}")
                return url, response.status

        except aiohttp.ClientError as e:
            logger.error(f"In process: {os.getpid()}. Can't process {url} client error occur: \n{e}")
            return url, None


if __name__ == '__main__':
    main()
