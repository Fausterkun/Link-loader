from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize
from wtforms.validators import InputRequired, URL, HostnameValidation


class UrlOnlyValidator(URL):
    """Validator for check url only, failed at ip."""

    def __init__(self, *args, **kwargs):
        self.validate_hostname = HostnameValidation(require_tld=False, allow_ip=False)
        super().__init__(*args, **kwargs)


class UrlForm(FlaskForm):
    """ Form for url only """
    submit_link = SubmitField("Submit link")
    link = URLField(
        "link",
        validators=[
            InputRequired(message="Field can't be empty"),
            UrlOnlyValidator(message="Value not a url."),
        ],
    )


class FileForm(FlaskForm):
    submit_file = SubmitField("Submit file")
    file = FileField(
        label='file',
        validators=[
            FileAllowed(
                message="Not correct file format, only .csv accepted",
                upload_set=(['csv']),
            ),
            FileRequired(message="file required"),
            FileSize(
                message='file size is too large for upload',
                max_size=1024
            )
        ]
    )
