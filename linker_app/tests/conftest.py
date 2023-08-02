import os
import time
import uuid
from types import SimpleNamespace

import pytest
from flask import current_app
from sqlalchemy_utils import create_database, drop_database
from yarl import URL

from linker_app import create_app, db, migrate
from linker_app.utils.config import load_config

config_filename = 'config.yaml'


@pytest.fixture
def postgres() -> str:
    """Fixture for create db with random name at start and drop at finish tests """
    config = load_config(config_filename)
    pg_url = config.get('SQLALCHEMY_DATABASE_URI')
    tmp_name = ".".join([uuid.uuid4().hex, "pytest"])
    tmp_url = str(URL(pg_url).with_path(tmp_name))
    create_database(tmp_url)
    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)


@pytest.fixture
def app(postgres):
    return create_app(SQLALCHEMY_DATABASE_URI=postgres)


@pytest.fixture
def client(app):
    with app.test_client() as client:
        return client


# @pytest.fixture
# def alembic_config(app):
#     """Return alembic config obj"""
#     config = app.extensions["migrate"].migrate.get_config()
#     return config

