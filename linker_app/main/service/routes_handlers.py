import json
import logging
import dataclasses
from typing import Tuple, List, Dict

from urllib.parse import urlparse, parse_qs
from sqlalchemy.exc import SQLAlchemyError

from linker_app import db, rabbit
from linker_app.database.query import create_or_update_link


class ValidationError(ValueError):
    pass


class SaveError(ValueError):
    pass


log = logging.getLogger()


def parse_link(link: str):
    """ serialize str to dict object """
    errors = []
    parsed = None
    try:
        parsed_link = urlparse(link)

        protocol = parsed_link.scheme
        path = parsed_link.path
        domain_with_zone = parsed_link.netloc
        domain, domain_zone = domain_with_zone.rsplit(".", 1)
        params = parse_qs(parsed_link.query)
        fragment = parsed_link.fragment
        parsed = {
            'url': link,
            'protocol': protocol,
            'path': path,
            'domain': domain,
            'domain_zone': domain_zone,
            'params': json.dumps(params),
            'fragment': fragment
        }
    except (ValueError) as e:  # , NameError):
        # TOOO: log that e
        errors.append({'Parser error': 'Cannot parse link.'})

    return parsed, errors


def link_handler(link: str):
    """
     Handle link add to db and return result status and errors
      :return status:bool, errors:list(dict(str, str))
      """
    # serialize to Link obj
    params, errors = parse_link(link)
    # save to db
    if errors:
        return False, errors

    # create link or update it unavailable_times counter
    try:
        create_or_update_link(**params)
    except SQLAlchemyError as e:
        print(e)
        # TODO: add log info with e
        db.session.rollback()  # Roll back the transaction in case of an error
        errors.append(dict(DatabaseError="Cannot add new link to db."))
        return False, errors

    return True, {}


def file_handler(filename):
    # see if any errors
    # save to db if no errors
    # else return to user
    pass
