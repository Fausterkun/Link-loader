import uuid

from sqlalchemy.exc import InvalidRequestError
from yarl import URL

from linker_app import db

MAX_QUERY_ARGS = 32767


def gen_test_db_name(url: str):
    """ Generate new db name and return full path to it"""
    url: str = url.rsplit("/", 1)[0]
    tmp_name = ".".join([uuid.uuid4().hex, "pytest"])
    tmp_url = str(URL(url).with_path(tmp_name))
    return tmp_url


def check_dialect(expected_name: str):
    used_dialect = db.engine.dialect.name
    if used_dialect != expected_name:
        raise InvalidRequestError(f'Used {used_dialect} db dialect but {expected_name} expected.')
