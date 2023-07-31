import re


class ValidationError(ValueError):
    pass


class RegexValidator:
    def __init__(self, regex, flags=0):
        self.regex = re.compile(regex, flags=flags)

    def __call__(self, text: str):
        match = self.regex.match(text or "")
        if match:
            return match
        raise ValidationError


class UrlValidator(RegexValidator):
    """
    Url validator obj. Created as singleton
    Validator code similar for code from wtforms.validators:URL module
    which used at single link validation due request from
     client with tld_part=False and not suggest that ip is url (allow_ip=False)

     Usage:
     url_validator = UrlValidator()
     is_url: bool = url_validator("some_text")
    """

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.regex = (
            r"^[a-z]+://"
            r"(?P<host>[^\/\?:]+)"
            r"(?P<port>:[0-9]+)?"
            r"(?P<path>\/.*?)?"
            r"(?P<query>\?.*)?$"
        )
        # create regex obj from regex string for url
        super().__init__(self.regex)

    def __call__(self, text):
        # check that text is url
        match = super().__call__(text)
        # check that hostname in that url is correct
        if not self.validate_hostname(match.group("host")):
            raise ValidationError
        return True

    @staticmethod
    def validate_hostname(hostname: str):
        # assign pattern for hostname validations
        hostname_part = re.compile(r"^(xn-|[a-z0-9_]+)(-[a-z0-9_-]+)*$", re.IGNORECASE)
        try:
            hostname = hostname.encode("idna")
        except UnicodeError:
            pass

        # Turn back into a string in Python 3x
        if not isinstance(hostname, str):
            hostname = hostname.decode("ascii")

        if len(hostname) > 253:
            return False

        # Check that all labels in the hostname are valid
        parts = hostname.split(".")
        for part in parts:
            if not part or len(part) > 63:
                return False
            if not hostname_part.match(part):
                return False

        return True
