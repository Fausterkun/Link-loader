import os
import uuid
from types import SimpleNamespace

import pytest
from sqlalchemy_utils import create_database, drop_database
from yarl import URL

from linker_app.utils.pg import make_alembic_config, DEFAULT_PG_URL

PG_URL = os.getenv('CI_LINKER_APP_PG_URL', DEFAULT_PG_URL)


@pytest.fixture
def postgres():
    tmp_name = ".".join([uuid.uuid4().hex, 'pytest'])
    tmp_url = str(URL(PG_URL).with_path(tmp_name))
    create_database(tmp_url)

    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)


@pytest.fixture
def alembic_config(postgres):
    """ Create alembic config for tmp database """
    cmd_options = SimpleNamespace(config='alembic.ini', name='alembic',
                                  pg_url=postgres)
    return make_alembic_config(cmd_options)
