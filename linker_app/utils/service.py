import re

class ValidationError(ValueError):
    pass


def file_reader(filename: str, buffer_size: int):
    remaining = ""
    lines = []
    with open(filename, "r") as file_raw:
        while True:
            chunk = file_raw.read(buffer_size)
            if not chunk:
                break

            lines = chunk.split("\n")
            remaining = lines.pop()


def simple_file_parser(filename: str):
    correct_urls_count = 0
    correct_urls: list = []
    failed_url_count = 0

    parsed_urls = 0

    with open(filename, "r") as file:
        line = file.readline()
        if validate_link(line):
            pass
