import pytest
import uuid

from sqlalchemy_utils import create_database, drop_database
from yarl import URL

from flask_migrate import upgrade
from linker_app import create_app, db, migrate
from linker_app.utils.config import load_config, BASE_CONFIG_NAME


@pytest.fixture(scope="module")
def postgres() -> str:
    """Fixture for create db with random name at start and drop at finish tests"""
    config = load_config(BASE_CONFIG_NAME)
    pg_url = config.get("CI_LINKER_APP_PG_URI")

    # get path without table name
    pg_url: str = pg_url.rsplit("/", 1)[0]
    tmp_name = ".".join([uuid.uuid4().hex, "pytest"])
    tmp_url = str(URL(pg_url).with_path(tmp_name))

    create_database(tmp_url)
    print('database created')
    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)
        print('database dropped')


@pytest.fixture
def app(postgres):
    app = create_app(SQLALCHEMY_DATABASE_URI=postgres)
    with app.app_context():
        upgrade()
    return app


@pytest.fixture
def client(app):
    with app.app_context():
        with app.test_client() as client:
            return client
