from flask import current_app
from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize
from wtforms.validators import InputRequired, URL, HostnameValidation

from flask import current_app


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
    submit_link = SubmitField("Submit link")


class FileForm(FlaskForm):
    def __init__(self, max_file_size: int = 1024, *args, **kwargs):
        self.max_file_size = max_file_size
        super().__init__(*args, **kwargs)

    file = FileField(
        label='file',
        validators=[
            FileAllowed(
                message="Not correct file format, only .csv accepted",
                upload_set=(['.csv']),
            ),
            FileRequired(message="file required"),
            FileSize(
                message='file size is too large for upload',
                max_size=1024
            )
        ]
    )
    submit_file = SubmitField("Submit file")

    # self.file = FileField(
    #     label='file',
    #     validators=[
    #         FileAllowed(
    #             message="Not correct file format, only .csv accepted",
    #             upload_set=(['.csv']),
    #         ),
    #         FileRequired(message="file required"),
    #         FileSize(
    #             message='file size is too large for upload',
    #             max_size=self.max_file_size
    #         )
    #     ]
    # )
