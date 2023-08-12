import pytest
from flask import url_for
from http import HTTPStatus

from linker_app.utils.testing import (
    get_correct_links,
    get_failed_links,
    get_csrf_token,
    fake_file_with_urls,
    fake_file_with_urls_with_size,
)
from linker_app.utils.config import FILE_MAX_SIZE
from linker_app import rabbit


# from linker_app.tests.conftest import client  # noqa: F401
# from linker_app.main.routes import links


# TODO: change all urls for usage with url_for

def test_index(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK


def test_logs(client):
    url = "/logs"
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_links(client):
    url = "/links"
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("link", get_correct_links())
def test_add_link_success(client, link):
    # list with test data: tuple(url, status_code, error (if occur else None))
    url = "/links"
    csrf_token = get_csrf_token(client, url)
    response = client.post(url, data=dict(link=link, csrf_token=csrf_token, submit_link=True))
    assert HTTPStatus.CREATED == response.status_code


@pytest.mark.parametrize("link", get_failed_links())
def test_add_link_failed(client, link):
    url = "/links"
    csrf_token = get_csrf_token(client, url)
    response = client.post(url, data=dict(link=link, csrf_token=csrf_token, submit_link=True))
    assert HTTPStatus.BAD_REQUEST == response.status_code

# TODO: add monkey patch for rabbit call
# def test_add_file_link_success(monkeypatch, client):
#     url = '/links'
#     # url = url_for('links')
#     file = fake_file_with_urls(1, extension='.csv')
#     response = client.post(
#         url,
#         data=dict(
#             file=file,
#             csrf_token=get_csrf_token(client, url),
#             submit_file=True
#         )
#     )
#     assert HTTPStatus.CREATED == response.status_code


def test_file_bigger_size(client):
    url = '/links'
    # url = url_for('links')
    # size = client.application.config.get('FILE_MAX_SIZE')  # not use .get for be sure that size setuped
    size = FILE_MAX_SIZE
    bigger_size = size + 1
    file = fake_file_with_urls_with_size(bigger_size, extension='.csv')
    response = client.post(
        url,
        data=dict(
            file=file,
            csrf_token=get_csrf_token(client, url),
            submit_file=True
        )
    )
    assert HTTPStatus.BAD_REQUEST == response.status_code


def test_file_incorrect_extensions():
    pass


def test_file_is_not_set():
    pass
