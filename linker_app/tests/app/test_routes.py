import pytest
from http import HTTPStatus
from linker_app.utils.testing import get_correct_links, get_failed_links, get_csrf_token
from linker_app.tests.conftest import client  # noqa: F401


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
    response = client.post(url, data=dict(link=link, csrf_token=csrf_token))
    assert HTTPStatus.CREATED == response.status_code


@pytest.mark.parametrize("link", get_failed_links())
def test_add_link_failed(client, link):
    url = "/links"
    csrf_token = get_csrf_token(client, url)
    response = client.post(url, data=dict(link=link, csrf_token=csrf_token))
    assert HTTPStatus.BAD_REQUEST == response.status_code
