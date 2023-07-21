from argparse import ArgumentTypeError


def validate(type: callable, constrain: callable):
    def wrapper(value):
        value = type(value)
        if not constrain(value):
            raise ArgumentTypeError
        return value

    return wrapper


positive_int = validate(int, constrain=lambda x: x > 0)

# clear_environ():
