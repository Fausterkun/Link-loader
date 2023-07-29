import os
import uuid
from types import SimpleNamespace

import pytest
from flask import current_app
from sqlalchemy_utils import create_database, drop_database
from yarl import URL

from linker_app import create_app


# PG_URL = os.getenv('CI_LINKER_APP_PG_URL', DEFAULT_PG_URL)

@pytest.fixture
def app():
    yield create_app()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


# from linker_app.utils.pg import DEFAULT_PG_URL

@pytest.fixture
def alembic_config(app):
    """ Return alembic config obj """
    config = app.extensions['migrate'].migrate.get_config()
    return config


@pytest.fixture
def postgres():
    """ Fixture for create db with random name at start and drop at finish tests"""
    pg_url = current_app.config.get("TEST_LINKER_APP_PG_URL")
    tmp_name = ".".join([uuid.uuid4().hex, 'pytest'])
    tmp_url = str(URL(pg_url).with_path(tmp_name))
    create_database(tmp_url)

    try:
        print('db created')
        yield tmp_url
    finally:
        print('db dropped')
        drop_database(tmp_url)

# @pytest.fixture
# def alembic_config(postgres):
#     """ Create alembic config for tmp database """
#     cmd_options = SimpleNamespace(config='alembic.ini', name='alembic',
#                                   pg_url=postgres)
#     return make_alembic_config(cmd_options)
