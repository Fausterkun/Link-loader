class WorkerError(RuntimeError):
    """ Error due worker runtime """


class ConnectionToDatabaseError(WorkerError):
    """ Error connection to database """
