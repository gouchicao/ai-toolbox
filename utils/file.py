import os


def get_file_name(filename):
    return os.path.splitext(os.path.basename(filename))[0]


def get_lines(filename):
    with open(filename, "r") as f:
        return f.read().splitlines()


def write_lines(filename, lines):
    with open(filename, 'w') as f:
        for line in lines:
            f.write(line+os.linesep)


def get_content(filename):
    with open(filename, "r") as f:
        return f.read()
