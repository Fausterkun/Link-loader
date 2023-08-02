from flask_wtf import FlaskForm
from wtforms import URLField
from wtforms.validators import InputRequired, URL, HostnameValidation


class UrlOnlyValidator(URL):
    """Validator for check url only, failed at ip."""

    def __init__(self, *args, **kwargs):
        self.validate_hostname = HostnameValidation(require_tld=False, allow_ip=False)
        super().__init__(*args, **kwargs)


# form which allow url
class UrlForm(FlaskForm):
    link = URLField(
        "link",
        validators=[
            InputRequired(message="Field can't be empty"),
            UrlOnlyValidator(message="Value not a url."),
        ],
    )
