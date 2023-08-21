import os
import pytest
from types import SimpleNamespace

from flask_migrate import upgrade
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database

from linker_app.utils.config import load_config, BASE_CONFIG_NAME
from linker_app.utils.db import gen_test_db_name
from linker_app import BASE_DIR, create_app
from linker_app.workers.link_checker.app import LinkCheckerWorker


@pytest.fixture(scope="class")
def worker_db_url():
    config_filename = os.path.join(BASE_DIR, BASE_CONFIG_NAME)
    config = load_config(config_filename)
    pg_url = config.get("CI_DB_URI")

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
def worker_app(worker_db_url):
    args = SimpleNamespace(remote_db=worker_db_url,
                           local_db=None)
    return LinkCheckerWorker(args)


@pytest.fixture(autouse=True, scope='class')
def migrated_db(worker_db_url):
    app = create_app(SQLALCHEMY_DATABASE_URI=worker_db_url)
    with app.app_context():
        upgrade()


@pytest.fixture
def db_session(worker_db_url):
    # upgrade db
    engine = create_engine(worker_db_url)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        yield session
