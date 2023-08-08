from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError

from linker_app.service.exceptions import SaveToDatabaseError
from linker_app.database.schema import Links
from linker_app.utils.db import check_dialect
from linker_app import db

from flask import current_app


def create_or_update_link(**params):
    """Create if link object is not exists yet, or update it unavailable_times to zero"""
    # TODO: can be improved using upsert
    url = params["url"]
    try:
        link = Links.query.filter_by(url=url).first()

        # if already in db then update, else insert
        if link:
            link.unavailable_times = 0
        else:
            link = Links(**params)
            db.session.add(link)
        db.session.commit()
    except SQLAlchemyError as e:
        # TODO: add log info with e
        current_app.logger.error("Error due try to save in db. \n {0}".format(e))
        db.session.rollback()  # Roll back the transaction in case of an error
        raise SaveToDatabaseError("Can't save link to database, try again latter or say system admin.")


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


def get_links(page: int = None, per_page: int = None, max_per_page: int = None, **params):
    """
     Query to get all links in db with pagination, max links in query got from config
     At None values params will be gotten from request(see doc or source code)
     """
    if not max_per_page:
        max_per_page = current_app.config.get('LINKS_MAX_PER_PAGE', 100)
    max_per_page = min(max_per_page, current_app.config.get('LINKS_MAX_PER_PAGE', 100))
    links = Links.query.paginate(page=page, per_page=per_page, max_per_page=max_per_page)
    return links
