import random

import pytest
from linker_app.utils.logger import LogBuffer


def test_size_cannot_be_zero():
    with pytest.raises(ValueError):
        max_size = 0
        LogBuffer(max_size=max_size)


def test_max_size_must_be_int():
    max_size = "10"
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        LogBuffer(max_size=max_size)


def test_log_buffer_init():
    max_size = random.randint(1, 100)
    log_buffer = LogBuffer(max_size=max_size)
    assert log_buffer._max_size == max_size


def test_log_buffer_add_message():
    log_buffer = LogBuffer(max_size=10)
    messages = [{"first": 1}, {"second": 2}, {"third": 3}]
    for message in messages:
        log_buffer.add_message(message)
    assert log_buffer.get_last() == messages


def test_log_buffer_size_limit():
    max_size = 3
    log_buffer = LogBuffer(max_size=max_size)
    messages = [{"first": 1}, {"second": 2}, {"third": 3}, {"fourth": 4}]
    for message in messages:
        log_buffer.add_message(message)
    assert log_buffer.get_last() == messages[1:]
