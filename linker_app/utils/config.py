from yaml import safe_load


def load_comfig(file_path):
    with open(file_path, "r") as file:
        config = safe_load(file)
    return config
