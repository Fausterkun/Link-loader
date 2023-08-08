from flask import flash

from linker_app.main.forms import UrlForm
from linker_app.utils.query import parse_url
from linker_app.database.query import create_or_update_link
from linker_app.service.exceptions import UrlValidationError, SaveToDatabaseError


def link_form_handler(url_form: UrlForm) -> tuple[UrlForm, bool]:
    """
    Handle UrlForm obj, check and save to db returning new obj or flush error and return previous
    """
    approved = False
    if url_form.validate_on_submit():
        try:
            url = url_form.link.data
            # serialize to Link obj
            parsed = parse_url(url)
            # add link to db or update it unavailable_times counter
            create_or_update_link(**parsed)
        except (UrlValidationError, SaveToDatabaseError) as e:
            # add message about error
            error_msg = e.args[0]
            url_form.link.errors.append(error_msg)
        else:
            flash("Link saved successfully")
            url_form = UrlForm()
            approved = True
    else:
        flash("Value is not a url")
    return url_form, approved
