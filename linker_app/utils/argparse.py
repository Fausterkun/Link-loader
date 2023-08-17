import os
from types import NoneType
from configargparse import ArgumentTypeError


# def validate(type: callable, constrain: callable):
#     def wrapper(value):
#         value = type(value)
#         if not constrain(value):
#             raise ArgumentTypeError
#         return value
#
#     return wrapper

# positive_int = validate(int, constrain=lambda x: x > 0)

def str_or_none(value):
    if type(value) not in (str, NoneType):
        raise ArgumentTypeError
    return value


def clear_environ(rule):
    """Clear env variables after app start for security reasons"""
    for name in filter(rule, tuple(os.environ)):
        os.environ.pop(name)


def get_env_vars_by_prefix(prefix):
    """Get env vars by prefix and return founded keys/values without it"""
    prefix_len = len(prefix)
    env_vars = {}
    for key, value in os.environ.items():
        if key.startswith(prefix):
            # Remove the prefix from the key to get the actual variable name
            actual_key = key[prefix_len:]
            env_vars[actual_key] = value
    return env_vars
