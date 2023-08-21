import os
import asyncio
import datetime
import logging
import multiprocessing
from argparse import Namespace
from types import SimpleNamespace

import aiohttp
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from linker_app import BASE_DIR
from linker_app.database.schema import Links
from linker_app.utils.config import BASE_CONFIG_NAME, load_config
from linker_app.workers.exceptions import ConnectionToDatabaseError

logger = logging.getLogger(__name__)


def handle_urls(urls: list[str]):
    """Asynchronously get status code from urls"""
    pid = os.getpid()
    logger.info(f"Start handle urls from {pid}")
    # TODO: think about send result into db from here for reduce query size
    loop = asyncio.get_event_loop()
    tasks = [get_status_code(url) for url in urls]
    # Todo: test with creating tasks - not coroutines at straightforward way
    # task = asyncio.create_task()
    result = loop.run_until_complete(asyncio.gather(*tasks))
    logger.info(f"Finish handle urls from {pid}")
    return result


async def get_status_code(url: str, timeout: int = 600):
    """Coroutine for open session and make request to url"""
    pid = os.getpid()
    async with aiohttp.ClientSession() as session:
        try:
            status_code = None
            async with session.get(url, timeout=timeout) as response:
                logger.info(
                    f"In process: {pid}. Response code: {response.status} url: {url}"
                )
                status_code = response.status

        except asyncio.TimeoutError as e:
            logger.warning(
                f"In process: {pid}. Can't process {url} timeout error: \n{e}"
            )
        except aiohttp.ClientError as e:
            logger.warning(
                f"In process: {pid}. Can't process {url} client error occur: \n{e}"
            )

        return url, status_code


class LinkCheckerWorker:
    def __init__(self, args: Namespace | SimpleNamespace):
        # setup config by args path
        self._setup(args)
        self.engine = create_engine(self._db_url)
        self.Session = sessionmaker(bind=self.engine)

        self.local_engine = create_engine(self._local_db_url)
        self.LocalSession = sessionmaker(bind=self.local_engine)

        self.logger = logger

    def _setup(self, args: Namespace | SimpleNamespace):
        """ setup configs from args and envs and from base"""
        if hasattr(args, "config"):
            self._config_filename = args.config
        else:
            self._config_filename = BASE_CONFIG_NAME

        self.config = load_config(os.path.join(BASE_DIR, self._config_filename))

        self._db_url = (
            args.remote_db if args.remote_db else self.config["DB_URI"]
        )
        self._local_db_url = (
            args.local_db if args.local_db else self.config["LOCAL_DB_URI"]
        )

        self.chunk_size = (
            args.chunk_size
            if hasattr(args, "chunk_size")
            else self.config["CHUNK_SIZE"]
        )
        self.request_timeout = (
            args.request_timeout
            if hasattr(args, "request_timeout")
            else self.config["REQUEST_TIMEOUT"]
        )
        self.proc_num = self.config.get("PROC_NUM", os.cpu_count() or 1)
        self.predicted_time = datetime.timedelta(
            seconds=self.config.get("PREDICTED_TIME", 600)
        )

    def run(self):
        """ Create and run processes with async self._get_status_code task"""
        time_start = datetime.datetime.now()
        self.logger.info(f"Start check links status code. Chunk size: {self.chunk_size}")
        urls = self._get_urls()
        chunks = [
            urls[i: i + self.chunk_size] for i in range(0, len(urls), self.chunk_size)
        ]
        full_result = []
        with multiprocessing.Pool(processes=self.proc_num) as pool:
            result = pool.map(handle_urls, chunks)
            for chunk in result:
                full_result.extend(chunk)
        for _ in result:
            # update values in db
            # add news values in db
            return full_result

        processed_time = datetime.datetime.now() - time_start
        if processed_time > self.predicted_time:
            logger.warning(
                f"Processing time more than predicted period({self.predicted_time}). Processed time: {processed_time}"
            )
        else:
            logger.info(f"Link checker task complete at time: {processed_time}")

    def _get_urls(self) -> list:
        try:
            with self.Session() as session:
                links = (
                    session.query(Links.url)
                    .filter(Links.unavailable_times < 4)
                    .all()
                )
            return [link[0] for link in links]
        except SQLAlchemyError as e:
            self.logger.error("Error due try to get links from db \n", e)
            raise ConnectionToDatabaseError("Can't get actual links from database.")
