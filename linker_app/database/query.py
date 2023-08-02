from linker_app.database.schema import Links
from linker_app import db


def get_all_links(nums, page):
    pass


def create_or_update_link(**params):
    """ Create if link object is not exists yet, or update it unavailable_times to zero """
    url = params['url']
    link = Links.query.filter_by(url=url).first()

    if link:
        link.unavailable_times = 0
    else:
        link = Links(**params)
        db.session.add(link)
    db.session.commit()
