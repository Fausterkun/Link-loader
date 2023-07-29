import uuid4


def get_str_uuid4():
    """ generate str with uuid (created for default va;ues in db columns) """
    return str(uuid.uuid4())
