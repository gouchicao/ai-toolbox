import os


def get_file_paths_by_iteration(path):
    paths = []
    for parent, _, filenames in os.walk(path):
        if filenames:
            paths.extend([os.path.join(parent, filename) for filename in filenames])

    return paths


def get_image_paths(path):
    ext_names = ['.png', '.jpg', '.jpeg', '.tif', '.bmp']
    return get_file_paths(path, ext_names)

def get_file_paths(path, ext_names = []):
    image_paths = []
    for filename in os.listdir(path):
        _, ext_name = os.path.splitext(filename.lower())
        if not ext_names or ext_name in ext_names:
            image_paths.append(os.path.join(path, filename))

    return image_paths

