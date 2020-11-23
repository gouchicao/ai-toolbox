import os

from PIL import Image
from datasets.utils import get_txt_from_file


def gen_xml(img_path, annotation_objs):
    template_main_path = get_local_file_path('template_main.xml')
    template_main = get_txt_from_file(template_main_path)

    template_object_path = get_local_file_path('template_object.xml')
    template_object = get_txt_from_file(template_object_path)

    folder, filename, img_path, width, height = _get_image_info(img_path)

    object_strs = []
    for obj in annotation_objs:
        _, xmin, ymin, xmax, ymax, obj_name = obj
        object_strs.append(template_object.format(obj_name=obj_name, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax))

    return template_main.format(folder=folder, filename=filename, path=img_path, width=width, height=height, 
                                objects=''.join(object_strs))


def get_local_file_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def _get_image_info(img_path):
    dir_path, filename = os.path.split(img_path)
    folder = os.path.basename(dir_path)

    with Image.open(img_path) as img:
        width, height = img.size

    return folder, filename, img_path, width, height
