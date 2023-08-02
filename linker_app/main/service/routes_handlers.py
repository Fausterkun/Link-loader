import json
import logging
import dataclasses
from typing import Tuple, List, Dict

from urllib.parse import urlparse, parse_qs
from sqlalchemy.exc import SQLAlchemyError

from linker_app import db, rabbit
from linker_app.database.query import create_or_update_link
from linker_app.main.exceptions import ServerError, UrlValidationError,SaveToDatabaseError

log = logging.getLogger()


def parse_link(link: str):
    """ serialize str to dict object """
    try:
        parsed_link = urlparse(link)
        protocol = parsed_link.scheme
        path = parsed_link.path
        domain_with_zone = parsed_link.netloc
        domain, domain_zone = domain_with_zone.rsplit(".", 1)
        params = parse_qs(parsed_link.query)
        parsed = {
            'url': link,
            'protocol': protocol,
            'path': path,
            'domain': domain,
            'domain_zone': domain_zone,
            'params': json.dumps(params),
        }
    except ValueError as e:
        # TODO: log it e
        raise UrlValidationError("Value not a link.")

    return parsed


def link_handler(link: str):
    """
     Handle link add to db and return result status and errors
      :return status:bool, errors:list(dict(str, str))
      """
    # serialize to Link obj
    parsed = parse_link(link)

    # add link to db or update it unavailable_times counter
    try:
        create_or_update_link(**parsed)
    except SQLAlchemyError as e:
        # TODO: add log info with e
        db.session.rollback()  # Roll back the transaction in case of an error
        raise SaveToDatabaseError("Can't save link to database, try again latter or say system admin.")

    return True, {}


def file_handler(filename):
    # see if any errors
    # save to db if no errors
    # else return to user
    pass
