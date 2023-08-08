import pytest
from flask import url_for
from http import HTTPStatus
from linker_app.utils.testing import (
    get_correct_links,
    get_failed_links,
    get_csrf_token,
    fake_urls_file_by_count,
    fake_urls_file_by_size,
)
from linker_app.main.routes import links
from linker_app.tests.conftest import client  # noqa: F401


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


# def test_add_file_link_success(client):
#     url = url_for('main.links')
#     pass
#
#
# def test_file_bigger_size(client, app):
#     url = url_for('main.links')
#     size = app.config.get('FILE_MAX_SIZE', 1024)
#     bigger_size = size + 1
#     file = fake_urls_file_by_size(bigger_size)
#     client.post({"file": file})


def test_file_incorrect_extensions():
    pass


def test_file_is_not_set():
    pass
