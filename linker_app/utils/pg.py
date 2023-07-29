import os
import uuid
from types import SimpleNamespace
from pathlib import Path

from alembic.config import Config
from configargparse import Namespace

# CENSORED = "***"
# DEFAULT_PG_URL = "postgresql://test:test@localhost/test_db"
# BASE_PATH = Path(__file__).parent.parent.resolve()


# def make_alembic_config(cmd_options: Namespace | SimpleNamespace, base_path: str = BASE_PATH) -> Config:
#     if not os.path.isabs(cmd_options.config):
#         cmd_options.config = os.path.join(base_path, cmd_options.config)
#
#     config = Config(
#         file_=cmd_options.config, ini_section=cmd_options.name, cmd_opts=cmd_options
#     )
#     alembic_location = config.get_main_option("script_location")
#
#     # if not os.path.isabs(alembic_location):
#     #     config.set_main_option(
#     #         "script_location", os.path.join(base_path, alembic_location)
#     #     )
#
#     if cmd_options.pg_url:
#         config.set_main_option("sqlalchemy.url", cmd_options.pg_url)
#
#     return config
#

def get_str_uuid4():
    """ generate str with uuid (created for default va;ues in db columns) """
    return str(uuid.uuid4())
