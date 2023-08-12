class ServerError(ConnectionError):
    """Error at server, try latter"""


class SaveToDatabaseError(ServerError):
    """"Error due save to database, pls try latter"""


class SendToQueueError(ServerError):
    """"Error due save to database, pls try latter"""


class QueueConnectionError(ServerError):
    """ Error with connection to RabbitMQ """


class ValidationError(ValueError):
    """Error due check value"""


class UrlValidationError(ValidationError):
    """Value is not a url"""
