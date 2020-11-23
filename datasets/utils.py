import os


def get_file_paths(path):
    paths = []
    for parent, _, filenames in os.walk(path):
        if filenames:
            paths.extend([os.path.join(parent, filename) for filename in filenames])

    return paths


def get_filelines(path):
    with open(path, "r") as f:
        return f.read().splitlines()


def get_txt_from_file(path):
    with open(path, "r") as f:
        return f.read()
