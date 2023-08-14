import pytest

from unittest.mock import Mock


@pytest.fixture
def mock_channel(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_method():
    return Mock(delivery_tag='delivery_tag')


@pytest.fixture
def mock_properties():
    return Mock()
