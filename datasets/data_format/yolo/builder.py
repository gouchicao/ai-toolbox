import os

from utils import image
from datasets.data_format import yolo


def get_annotation_content(img_path, annotation_objs, classes):
    """
        annotation_objs: xmin, ymin, xmax, ymax, obj_name
    """

    w, h = image.get_image_size(img_path)

    yolo_lines = []
    for obj in annotation_objs:
        xmin, ymin, xmax, ymax, obj_name = obj

        cls_id = classes.index(obj_name)
        b = (float(xmin), float(xmax), float(ymin), float(ymax))
        bb = yolo.convert_yolo_size((w,h), b)
        yolo_lines.append(str(cls_id) + " " + " ".join([str(a) for a in bb]) + os.linesep)

    return ''.join(yolo_lines)
