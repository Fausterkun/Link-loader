from sqlalchemy.exc import InvalidRequestError

from linker_app import db

MAX_QUERY_ARGS = 32767


def check_dialect(expected_name: str):
    used_dialect = db.engine.dialect.name
    if used_dialect != expected_name:
        raise InvalidRequestError(f'Used {used_dialect} db dialect but {expected_name} expected.')
