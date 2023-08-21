import os
import asyncio
from types import SimpleNamespace
from unittest.mock import Mock

import faker
import aiohttp
import pytest
from flask_migrate import upgrade
from sqlalchemy import insert, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database

from linker_app import BASE_DIR, create_app
from linker_app.database.schema import Links
from linker_app.utils.db import gen_test_db_name
from linker_app.utils.query import parse_url
from linker_app.utils.testing import get_fake_urls
from linker_app.utils.config import load_config, BASE_CONFIG_NAME
from linker_app.workers.link_checker import LinkCheckerWorker
from linker_app.workers.link_checker.app import get_status_code, handle_urls

faker = faker.Faker()


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


class TestGetStatusCode:
    def test_run(self, mock_response, db_session, worker_db_url, monkeypatch):
        chunk_size = 25
        urls_count = 100
        # mock_handle_urls = lambda x: [None for _ in range(chunk_size)]
        # mock_handle_urls.return_value = [None for _ in range(chunk_size)]
        # monkeypatch.setattr('linker_app.workers.link_checker.app.handle_urls', mock_handle_urls)

        urls = list(get_fake_urls(urls_count))
        for url in urls:
            mock_response.get(url, status=200)
        # chunks = [urls[i:i + chunk_size] for i in range(0, urls_count, chunk_size)]
        mock_get_urls = Mock()
        mock_get_urls.return_value = urls
        monkeypatch.setattr(LinkCheckerWorker, '_get_urls', mock_get_urls)

        args = SimpleNamespace(
            remote_db=worker_db_url,
            local_db=None,
            chunk_size=chunk_size
        )
        worker_app = LinkCheckerWorker(args)
        result = worker_app.run()
        assert result == [(url, 200) for url in urls]
        mock_get_urls.assert_called_once()

    # def test_run_update_links(self, mock_response, db_session, worker_app):
    #     urls = get_fake_urls(100)
    #     for url in urls:
    #         mock_response.get(url, status=200)
    #
    #     links = [parse_url(url) for url in urls]
    #     query = insert(Links).values(links)
    #
    #     # add test urls in db:
    #     worker_app.run()
    #     try:
    #         # add test objs
    #         session.execute(query)
    #         session.commit()
    #
    #         test_links = session.query(Links).limit(5)
    #         worker_app.run()
    #
    #     finally:
    #         session.query(Links).all().delete()
    #         session.commit()

    @pytest.mark.asyncio
    async def test_get_status_code_success(self, mock_response):
        url = faker.url()
        mock_response.get(url, status=200)
        result = await get_status_code(url)
        assert result == (url, 200)

    @pytest.mark.asyncio
    async def test_get_status_code_timeout(self, mock_response):
        # for mock recognize success url append 'success' at the end
        url = faker.url()
        mock_response.get(url, exception=asyncio.TimeoutError)
        result = await get_status_code(url)
        assert result == (url, None)

    @pytest.mark.asyncio
    async def test_get_status_code_error(self, mock_response):
        # for mock recognize success url append 'success' at the end
        url = faker.url()
        mock_response.get(url, exception=aiohttp.ClientError)
        result = await get_status_code(url)
        assert result == (url, None)

    def test_handle_urls(self, mock_response):
        urls = list(get_fake_urls(5))
        for url in urls:
            mock_response.get(url, status=200)
        result = handle_urls(urls)
        assert [(url, 200) for url in urls] == result


class TestWorker:
    def test_get_urls(self, worker_app, db_session):
        # create links in db
        urls = get_fake_urls(33)
        links = [parse_url(url) for url in urls]
        query = insert(Links).values(links)
        db_session.execute(query)
        db_session.commit()

        # call check function
        result = worker_app._get_urls()
        assert list(urls) == result
        db_session.query(Links).filter(Links.url in urls).delete(synchronize_session=False)
