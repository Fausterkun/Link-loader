# from linker_app.service.handlers import (
#     file_handler,
#     file_form_handler,
#     link_form_handler,
#     link_handler
# )
from linker_app.utils.testing import fake_file_with_urls, fake_file_with_urls_with_size


# Tests for

def test_file_handler_success():
    # check that return uuid
    # and created file with that uuid
    # and reqeust obj created in db
    # rabbitmq message sent
    pass


def test_file_handler_fail():
    # check that flash msg occur
    # and file not created
    # and reqeust obj not created in db
    # rabbitmq message not sent
    pass


def test_file_form_handler_success():
    # check that flush message occur and return new form
    pass


def test_file_form_handler_fail():
    # check that flush message occur and return previous form in data
    pass
