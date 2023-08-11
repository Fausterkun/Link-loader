import os
import uuid

from flask import flash, current_app
from werkzeug.datastructures import FileStorage
from sqlalchemy.exc import SQLAlchemyError

from linker_app import db, APP_DIR, rabbit
from linker_app.main.forms import UrlForm, FileForm
from linker_app.utils.query import parse_url
from linker_app.database.schema import FileRequest
from linker_app.database.query import create_or_update_link
from linker_app.service.exceptions import UrlValidationError, SaveToDatabaseError


def link_form_handler(url_form: UrlForm) -> tuple[UrlForm, bool]:
    # TODO: change it to call link_handler(link: str) for repeat use from api
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
            url_form = UrlForm()
            approved = True
    else:
        flash("Value is not a url")
    return url_form, approved


def link_handler(url: str) -> None | str:
    """ Handle url serialize it and save to db """
    error_msg = None
    try:
        parsed = parse_url(url)
        create_or_update_link(**parsed)
    except (UrlValidationError, SaveToDatabaseError) as e:
        # add message about error
        error_msg = e.args[0]
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
            file_form.errors.appen(error_msg)
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
    path = os.path.join(APP_DIR, current_app.config.get('FILES_STORE_DIR'), filename + ext)
    try:
        # 2. Save fil to disk
        file.save(path)
        # 3. Create FileRequest in db
        db.session.add(FileRequest(uuid=filename))
        db.session.commit()
        # 4. send task to MQ [PASSED]
        # rabbit.send_message('linker_app_file_parser')

    except OSError as e:
        error_msg = "Error due save obj to disk"
        current_app.logger.error("Error due save file to disk. \n {0}".format(e))

    except SQLAlchemyError as e:
        # delete file and rollback transaction
        try:
            os.remove(path)

        except OSError as os_e:
            current_app.logger.error("Error due try to remove file from disk. \n {0}".format(os_e))

        db.session.rollback()  # Roll back the transaction in case of an error
        error_msg = "Can't save link to database, try again latter or say system admin."
        current_app.logger.error("Error due try to save in db. \n {0}".format(e))

    # TODO: handle rabbitmq connectio error

    return error_msg, filename
