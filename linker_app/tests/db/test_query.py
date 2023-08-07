import copy

import pytest

from linker_app.database.query import get_links, create_or_update_links, create_or_update_link
from linker_app.database.schema import Links
from linker_app.service.handlers import parse_link
from linker_app import db
from linker_app.utils.testing import get_fake_urls


def test_get_links(app):
    """ test get links """
    urls = get_fake_urls(100)
    parsed_urls = [parse_link(url) for url in urls]
    with app.app_context():
        with db.session.begin():
            db.session.bulk_insert_mappings(Links, parsed_urls)
        links = get_links(page=1, per_page=100, max_per_page=200)
    assert links.total == 100
    for link in links:
        assert link.url in urls


def test_create_or_update_links(app):
    """ Test create_or_update_links method """
    urls_num = 10
    urls = get_fake_urls(urls_num)
    parsed_urls = [parse_link(url) for url in urls]

    with app.app_context():
        # 1. Check that data inserted
        create_or_update_links(parsed_urls)
        links = Links.query.filter(Links.url.in_(urls)).all()

        # check result nums:
        # copy for exclude mistake due duplicate url possibility
        assert len(links) == urls_num
        checked_urls = copy.copy(urls)
        for link in links:
            assert link.url in checked_urls
            checked_urls.remove(link.url)

        # 2. Update their unavailable_times
        # links = Links.query.filter(Links.url.in_(urls))
        for link in links:
            link.unavailable_times = 2
        # db.session.add_all(links)
        db.session.commit()

        # get it and check that unavailable_times != 0
        links = Links.query.filter(Links.url.in_(urls))
        for link in links:
            assert link.unavailable_times == 2

        # 3. Check that unavailable_times updated to 0 if obj exist
        create_or_update_links(parsed_urls)
        links = Links.query.filter(Links.url.in_(urls))
        for link in links:
            assert link.unavailable_times == 0
