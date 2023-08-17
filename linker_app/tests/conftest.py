import pytest

from sqlalchemy_utils import create_database, drop_database
from aioresponses import aioresponses

from flask_migrate import upgrade
from linker_app import create_app
from linker_app.utils.config import load_config, BASE_CONFIG_NAME
from linker_app.utils.db import gen_test_db_name


@pytest.fixture(scope="module")
def app_db_url() -> str:
    """Fixture for create db with random name at start and drop at finish tests"""
    config = load_config(BASE_CONFIG_NAME)
    pg_url = config.get("CI_LINKER_APP_PG_URI")

    # get path without table name
    tmp_url = gen_test_db_name(pg_url)

    create_database(tmp_url)
    print('database created')
    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)
        print('database dropped')


@pytest.fixture
def app(app_db_url):
    app = create_app(SQLALCHEMY_DATABASE_URI=app_db_url)
    with app.app_context():
        upgrade()
    return app


@pytest.fixture
def client(app):
    with app.app_context():
        with app.test_client() as client:
            return client


@pytest.fixture
def mock_response():
    with aioresponses(passthrough=["127.0.0.1"]) as mock_resp:
        yield mock_resp
