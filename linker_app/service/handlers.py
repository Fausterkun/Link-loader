from flask import flash, current_app
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from io import BytesIO

from linker_app.main.forms import UrlForm, FileForm
from linker_app.utils.query import parse_url
from linker_app.database.query import create_or_update_link
from linker_app.service.exceptions import UrlValidationError, SaveToDatabaseError


def link_form_handler(url_form: UrlForm) -> tuple[UrlForm, bool]:
    # TODO: change it to call link_handler(link: str) for repeat use from api
    """
    Handle UrlForm obj, check and save to db returning new obj or flush error and return previous
    """
    approved = False
    if url_form.validate_on_submit():
        # try:
        #     # serialize to Link obj
        #     parsed = parse_url(url)
        #     # add link to db or update it unavailable_times counter
        #     create_or_update_link(**parsed)
        # except (UrlValidationError, SaveToDatabaseError) as e:
        #     # add message about error
        #     error_msg = e.args[0]
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
    error_msg = None
    try:
        parsed = parse_url(url)
        # add link to db or update it unavailable_times counter
        create_or_update_link(**parsed)
    except (UrlValidationError, SaveToDatabaseError) as e:
        # add message about error
        error_msg = e.args[0]
    return error_msg


#
# def file_form_handler(file_form: FileForm) -> tuple[FileForm, bool]:
#     approved = False
#     if file_form.validate_on_submit():
#         try:
#             # f = file_form.file.data
#             file_handler(file_form.file.data)
#             # filename = secure_filename(file_form.submit_file(f.filename))
#


def file_handler(file: FileStorage):
    """ Get file,give it a name, save in filesystem and create task in db """
    # 1. save file in db
    # give it uuid as name
    # try to save it with that uuid
    # if error then change uuid and remove previous,
    # create new request in db
    file.save(current_app.instance_path, current_app.config.get('FILES_STORE_DIR'), )
