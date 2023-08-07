from sqlalchemy.dialects.postgresql import insert

from linker_app.database.schema import Links
from linker_app.utils.db import check_dialect
from linker_app import db

from flask import current_app


def create_or_update_link(**params):
    """Create if link object is not exists yet, or update it unavailable_times to zero"""
    url = params["url"]
    link = Links.query.filter_by(url=url).first()

    if link:
        link.unavailable_times = 0
    else:
        link = Links(**params)
        db.session.add(link)
    db.session.commit()


def create_or_update_links(links: list[Links]):
    """
     Upsert query for update unavailable_times to zero if url already in db
      Note that this dialect dependent feature and used only for postgres
      """
    check_dialect('postgresql')
    query = insert(Links).values(links)
    query = query.on_conflict_do_update(
        index_elements=['url'],
        set_={'unavailable_times': 0}
    )
    db.session.execute(query)
    db.session.commit()


def get_links(page: int = None, per_page: int = None, max_per_page: int = None):
    """
     Query to get all links in db with pagination, max links in query got from config
     At None values params will be gotten from request(see doc or source code)
     """
    if not max_per_page:
        max_per_page = min(max_per_page, current_app.config.get('LINKS_MAX_PER_PAGE', 100))
    links = Links.query.paginate(page=page, per_page=per_page, max_per_page=max_per_page)
    return links
