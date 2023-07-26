from http import HTTPStatus

from utils import client  # noqa: F401


def test_logs(client):
    response = client.get("/logs")
    assert response.status_code == HTTPStatus.OK


def test_links(client):
    response = client.get("/links")
    assert response.status_code == HTTPStatus.OK
