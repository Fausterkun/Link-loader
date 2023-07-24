import argparse
import logging
import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate.cli import db
from alembic.config import CommandLine
from dotenv import load_dotenv

import configargparse
# from utils.pg import make_alembic_config, DEFAULT_PG_URL
from dotenv import load_dotenv
from linker_app.app import app
from configargparse import ArgumentParser
from flask import Flask

from linker_app.app.settings import configure_app

load_dotenv('.env')

# parser = ArgumentParser(
#     # auto_env_var_prefix=ENV_VAR_PREFIX,
#     allow_abbrev=False,
#     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
# )
#
# parser.add_argument(
#     "--config-file", default="config.yaml", help="Url for .yaml config file"
# )

app = Flask(__name__)
args = {'config_file': "config.yaml"}
configure_app(app, conf_file=args["config_file"])  # , args=args)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#
#
# def main():
#     # args = parser.parse_args()
#     args = {'config_file': "config.yaml"}
#     configure_app(app, conf_file=args["config_file"])  # , args=args)
#     db = SQLAlchemy(app)
#     migrate = Migrate(app, db)
#
#
# if __name__ == "__main__":
#     main()
