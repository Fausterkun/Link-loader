class ServerError(ConnectionError):
    """ Error at server, try latter """


class ValidationError(ValueError):
    """ Error due check value """


class UrlValidationError(ValidationError):
    """ Value is not a url """
