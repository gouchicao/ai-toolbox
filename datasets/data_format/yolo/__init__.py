import os

from datasets.dataset import DataSet
from datasets.data_format.yolo import builder
from utils import file


class YOLODataSet(DataSet):

    def __init__(self, path):
        super().__init__(path, '.txt')

    def get_annotation_path(self, img_filename):
        return os.path.join(self.labels_path, file.get_file_name(img_filename) + self.label_file_extname)

    def get_annotation_content(self, img_path, annotation_objs, classes):
        print('\n+++', annotation_objs)
        return builder.get_annotation_content(img_path, annotation_objs, classes)


def convert_yolo_size(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
