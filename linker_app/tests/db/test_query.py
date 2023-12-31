import copy
import math

from linker_app.database.query import get_links, upsert_links, upsert_link
from linker_app.database.schema import Links
from linker_app.utils.query import parse_url
from linker_app import db
from linker_app.utils.testing import get_fake_urls, fake


class TestGetLinks:

    def test_get_links(self, app):
        """ test get links query """
        # 1. Crete fake urls
        urls_count = 127
        urls = get_fake_urls(urls_count)

        with app.app_context():
            # 2. Insert new urls
            with db.session() as session:
                parsed_urls = [parse_url(url) for url in urls]
                session.bulk_insert_mappings(Links, parsed_urls)

                # 3. Get links and check pagination
                per_page = 3
                pages_count = math.ceil(urls_count / per_page)

                # prepare check set with urls
                check_urls = copy.copy(urls)

                # iterate over pages and remove url from check set
                for page in range(1, pages_count + 1):
                    links = get_links(page=page, per_page=per_page)  # , max_per_page=max_per_page)

                    # if not last page
                    if page < pages_count:
                        for link in links:
                            assert link.url in check_urls
                            check_urls.remove(link.url)
                        continue

                    # at the last page
                    for link in links:
                        assert link.url in check_urls
                        check_urls.remove(link.url)
                    # check that all urls were in query
                    assert len(check_urls) == 0

    def test_domain_filter(self, app):
        """ We can't use fake.url() here cause half-duplicate urls """
        test_urls_count = 4

        # create urls
        urls = {
            'http://test-url.com/',
            'http://pass-url.cz',
            'https://google.com/',
            'http://test.com',
        }

        # add more urls with same domain
        test_url = "http://cute-cat.su/"
        test_domain = parse_url(test_url)['domain']
        i = 0
        while i < test_urls_count:
            url = test_url + str(i)  # http://cute-cat.su/0 ... 3
            urls.add(url)
            i += 1
        # add parsed_urls in db and test filtered query
        parsed_urls = [parse_url(url) for url in urls]
        with app.app_context():
            # open session and transaction
            with db.session() as session:
                session.add_all([Links(**parsed_url) for parsed_url in parsed_urls])
                result = list(get_links(domain=test_domain))
                assert len(result) == test_urls_count


class TestInsertUpdateLinks:
    def test_create_or_update_link(self, app):
        """ Test create or update single link (without upsert)"""
        url = fake.url()

        with app.app_context():
            # 1. do insert and check it:
            upsert_link(session=db.session, url=url)

            # check that inserted
            link = Links.query.filter_by(url=url).first()
            assert link

            # 2. change unavailable_count
            link.unavailable_times = 2
            db.session.add(link)
            db.session.commit()
            link = Links.query.filter_by(url=url).first()
            # check that changed
            assert link.unavailable_times == 2

            # 3. check that unavailable_count changed to 0 if obj already in db
            upsert_link(session=db.session, url=url)
            link = Links.query.filter_by(url=url).first()
            assert link.unavailable_times == 0

    def test_upsert_links(self, app):
        """ Test upsert_links method """
        urls_num = 10
        urls = get_fake_urls(urls_num)
        parsed_urls = [parse_url(url) for url in urls]

        with app.app_context():
            # 1. Check that data inserted
            upsert_links(session=db.session, links=parsed_urls)
            links = Links.query.filter(Links.url.in_(urls)).all()

            # check result nums:
            assert len(links) == urls_num
            # copy for exclude mistake due duplicate url possibility
            checked_urls = copy.copy(urls)
            for link in links:
                assert link.url in checked_urls
                checked_urls.remove(link.url)

            # 2. Update their unavailable_times
            for link in links:
                link.unavailable_times = 2
            db.session.commit()

            # get it and check that unavailable_times != 0
            links = Links.query.filter(Links.url.in_(urls))
            for link in links:
                assert link.unavailable_times == 2

            # 3. Check that unavailable_times updated to 0 if obj exist
            upsert_links(session=db.session, links=parsed_urls)
            links = Links.query.filter(Links.url.in_(urls))
            for link in links:
                assert link.unavailable_times == 0
