import logging
import os
import uuid

from flask import flash, current_app
from werkzeug.datastructures import FileStorage
from sqlalchemy.exc import SQLAlchemyError

from linker_app import db, rabbit, BASE_DIR
from linker_app.main.forms import UrlForm, FileForm
from linker_app.database.schema import FileRequest
from linker_app.database.query import upsert_link
from linker_app.service.exceptions import (
    UrlValidationError,
    SaveToDatabaseError,
    SendToQueueError,
    QueueConnectionError
)

logger = logging.getLogger(__name__)


def link_form_handler(url_form: UrlForm) -> tuple[UrlForm, bool]:
    """
    Handler for UrlForm
    return new or previous file_form and bool (success or not)
    """
    approved = False
    if url_form.validate_on_submit():
        url = url_form.link.data
        error_msg = link_handler(url)
        if error_msg:
            url_form.link.errors.append(error_msg)
        else:
            flash("Link saved successfully")
            logger.info(f'Link {url} saved successfully.')
            url_form = UrlForm()
            approved = True
    else:
        flash("Value is not a url")
    return url_form, approved


def link_handler(url: str) -> None | str:
    """ Handle url serialize it and save to db """
    error_msg = None
    try:
        # parsed = parse_url(url)
        upsert_link(db.session, url)
    except (UrlValidationError, SaveToDatabaseError) as e:
        error_msg = "Error due link handle."
        logger.error(f'Error due handle link:\n{e}')
    return error_msg


def file_form_handler(file_form: FileForm) -> tuple[FileForm, bool]:
    """
     Handler for file form
    return new or previous file_form and bool (success handle or not)
    """
    approved = False
    if file_form.validate_on_submit():
        error_msg, filename = file_handler(file_form.file.data)
        if error_msg:
            file_form.errors.append(error_msg)
        else:
            flash("Link saved successfully")
            # TODO: change it to auto url path for request status info
            flash("Uuid of file processing request:\n{0}".format(filename))
            file_form = FileForm()
            approved = True
    else:
        flash("Error due file validation")
    return file_form, approved


def file_handler(file: FileStorage) -> tuple[None | str, str]:
    """ Handle file obj,
     1. give it a name
     2. save at disk
     3. create FileRequest in db
     4. push message in MQ
      return: error_msg (if occur else None), filename """
    error_msg = None
    ext = '.csv'

    # 1. give it uuid as name
    filename = str(uuid.uuid4())
    path = os.path.join(BASE_DIR, current_app.config.get('FILES_STORE_DIR'), filename + ext)
    try:
        # 2. Save fil to disk
        file.save(path)
        # 3. Create FileRequest in db
        db.session.add(FileRequest(uuid=filename))
        db.session.commit()
        # 4. send task to MQ [PASSED]
        rabbit.send_messages('linker_app_file_parser', filename)

    except FileNotFoundError as e:
        error_msg = "Error due save obj to disk. Possibly with App dir path setup."
        logger.error(f"Error due save file to disk. Possibly with App dir path setup. \n {e}")

    except FileExistsError as e:
        # if file with that name already exists (lol uuid4, but ok just for show, and it still may-be)
        # we can retry (if we use auto-generate name) or just raise exception
        error_msg = "Can't save file to disk, try again latter or say system admin."
        logger.error("Error due try to save on disk."
                     f" File with that name already exists: \n {e}")

    except SQLAlchemyError as e:
        # delete file and rollback transaction
        try:
            os.remove(path)

        except OSError as os_e:
            logger.fatal(
                f"Error due try to remove file from disk."
                f"\nFilename: {filename}"
                f"\nFilepath: {path}"
                f"\nError: {os_e}"
            )

        error_msg = "Can't save file to database, try again latter or say system admin."
        logger.error(f"Error due try to save in db. \n {e}")
        db.session.rollback()

    except SendToQueueError as e:
        # error due send to rabbitMQ message
        error_msg = "Error due sending file to parser."
        logger.error(f"Error due send message to RabbitMQ at file handling {e}")

    except QueueConnectionError as e:
        # error due send to rabbitMQ message
        error_msg = "Error due sending file to parser."
        logger.error(f"Error due send message to RabbitMQ at file handling {e}")

    except OSError as e:
        # unknown os error
        current_app.app.logger.error(f"Error due handle incoming file. Filename {filename}", e)
        error_msg = "Error due file handle."

    return error_msg, filename
