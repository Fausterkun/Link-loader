from io import BytesIO
from typing import Tuple, Any

from bs4 import BeautifulSoup
from faker import Faker

LINKS_IN_TEST_DATABASE = 300
FILE_SIZE_IN_TEST = 1024  # kb

fake = Faker()


def get_csrf_token(client, url):
    """find first csrf token on page"""
    response = client.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"}).get("value")
    return csrf_token


def get_correct_links():
    success_data = (
        "https://www.some-url.com/path",
        "https://chat.openai.com/",
        "https://flask-wtf.readthedocs.io/en/",
        "http://www.google.com",
        "https://www.google.com",
        "http://google.com",
        "https://google.com",
        "http://www.google.com/~as_db3.2123/134-1a",
        "https://www.google.com/~as_db3.2123/134-1a",
        "http://google.com/~as_db3.2123/134-1a",
        "https://google.com/~as_db3.2123/134-1a",
        # .co.uk top level
        "http://www.google.co.uk",
        "https://www.google.co.uk",
        "http://google.co.uk",
        "https://google.co.uk",
        "http://www.google.co.uk/~as_db3.2123/134-1a",
        "https://www.google.co.uk/~as_db3.2123/134-1a",
        "http://google.co.uk/~as_db3.2123/134-1a",
        "https://google.co.uk/~as_db3.2123/134-1a",
    )
    return success_data


def get_failed_links():
    failed_data = (
        # "http://127.0.0.1:5000/links",  # TODO: solve it using more tadious validator
        "not-url",
        "1231.com",
        # data without protocol
        "google.com",
        "google.co.uk",
        "google.co.uk/~as_db3.2123/134-1a",
        "www.google.com",
        "www.google.co.uk",
        "www.google.com/~as_db3.2123/134-1a",
        "google.com/~as_db3.2123/134-1a",
    )
    return failed_data


def get_fake_urls(count: int = None) -> set:
    """ generate unique fake urls """
    if not count:
        count = LINKS_IN_TEST_DATABASE
    fake_urls = set()
    while len(fake_urls) < count:
        fake_urls.add(fake.url())
    return fake_urls


def fake_urls_file_by_size(file_size: int = None, url_size: int = 255, extension: str = None) -> tuple[
    BytesIO, str]:
    """ create struct for flask file handler with current size """

    # set given or random extension
    if extension:
        file_name = fake.file_name(extension=extension)
    else:
        file_name = fake.file_name()
    if file_size is None:
        file_size = FILE_SIZE_IN_TEST
    url_str = ''
    # add fake urls
    while len(url_str) < file_size - url_size:
        url_str += fake.url() + '\n'

    # add useless char at the end of file for set correct file size
    while len(url_str) < file_size:
        url_str += 'f'
    file = (BytesIO(url_str.encode()), file_name)
    return file


def fake_urls_file_by_count(count: int = None, extension: str = None) -> tuple[BytesIO, str]:
    """ create struct for flask file handler with current number of urls """
    # set given or random extension
    if extension:
        file_name = fake.file_name(extension=extension)
    else:
        file_name = fake.file_name()
    # add fake urls
    urls = get_fake_urls(count)
    urls_str = "\n".join(urls)
    file = (BytesIO(urls_str.encode()), file_name)
    return file
