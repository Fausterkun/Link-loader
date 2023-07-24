import argparse
import logging
import os

from flask_sqlalchemy import SQLAlchemy
from alembic.config import CommandLine
from dotenv import load_dotenv

import configargparse
from utils.pg import make_alembic_config, DEFAULT_PG_URL

load_dotenv('.env')


def main():
    logging.basicConfig(level=logging.DEBUG)
    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
    alembic.parser.add_argument(
        '--pg-url',
        default=os.getenv('LINKER_PG_URL', DEFAULT_PG_URL),
        help='Database URL [env var: LINKER_PG_URL]'
    )
    options = alembic.parser.parse_args()
    if 'cmd' not in options:
        alembic.parser.error('not enough arguments')
        exit(128)
    else:
        config = make_alembic_config(options)
        exit(alembic.run_cmd(config, options))


if __name__ == "__main__":
    main()
    # args = parser.parse_args()
    # db = SQLAlchemy()
