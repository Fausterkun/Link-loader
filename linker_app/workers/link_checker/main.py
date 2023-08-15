import sys
import argparse
import logging
from logging import StreamHandler

from configargparse import ArgumentParser

from linker_app.workers.link_checker import LinkCheckerWorker
from linker_app.workers.exceptions import WorkerError

ENV_VAR_PREFIX = "LINK_CHECKER_"

parser = ArgumentParser(
    auto_env_var_prefix=ENV_VAR_PREFIX,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("--config", type=str, default="config.yaml", help="Config filename")
parser.add_argument(
    "--remote-db",
    type=str,
    default=None,
    help="Url for main database, in not setup -" " value got from config file",
)
parser.add_argument(
    "--local-db",
    type=str,
    default=None,
    help="Url for local database, in not setup -" " value got from config file",
)

logger = logging.getLogger(__name__)


def configure_logging():
    # set log level and handler to stdout
    # TODO: add logging setup from args
    logger.setLevel(logging.INFO)
    stream_handler = StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


if __name__ == "__main__":
    args = parser.parse_args()
    configure_logging()
    app = LinkCheckerWorker(args)
    try:
        logger.info("Start Link checker task")
        app.run()
    except WorkerError as e:
        logger.error(
            f"Error due check links status code worker. Process not finished.\n{e}"
        )
