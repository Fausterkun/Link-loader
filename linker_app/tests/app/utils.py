import pytest
from linker_app.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
