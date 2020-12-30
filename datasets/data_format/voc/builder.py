import os

from utils import file
from utils import image


def get_annotation_content(img_path, annotation_objs):
    """
        annotation_objs: xmin, ymin, xmax, ymax, obj_name
    """

    template_main_path = _get_local_file_path('template_main.xml')
    template_main = file.get_content(template_main_path)

    template_object_path = _get_local_file_path('template_object.xml')
    template_object = file.get_content(template_object_path)

    folder, filename, img_path, width, height = _get_image_info(img_path)

    object_strs = []
    for obj in annotation_objs:
        xmin, ymin, xmax, ymax, obj_name = obj
        object_strs.append(template_object.format(obj_name=obj_name, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax))

    return template_main.format(folder=folder, filename=filename, path=img_path, width=width, height=height, 
                                objects=''.join(object_strs))


def _get_local_file_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def _get_image_info(img_path):
    dir_path, filename = os.path.split(img_path)
    folder = os.path.basename(dir_path)
    width, height = image.get_image_size(img_path)

    return folder, filename, img_path, width, height
