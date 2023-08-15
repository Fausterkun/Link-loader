from sqlalchemy import Engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import InvalidRequestError

from linker_app.database.schema import Links


def check_dialect(expected: str, engine: Engine):
    used_dialect = engine.dialect.name
    if used_dialect != expected:
        raise InvalidRequestError(
            f"Used {used_dialect} db dialect but {expected} expected."
        )


def upsert_links_query(engine: Engine, links: list[dict]):
    check_dialect("postgresql", engine)
    query = insert(Links).values(links)
    query = query.on_conflict_do_update(
        index_elements=["url"], set_={"unavailable_times": 0}
    )
    return query
