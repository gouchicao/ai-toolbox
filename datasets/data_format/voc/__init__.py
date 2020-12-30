import os

from datasets.dataset import DataSet
from datasets.data_format.voc import builder
from utils import file


class VOCDataSet(DataSet):
    def __init__(self, path):
        super().__init__(path, '.xml')

    def get_annotation_path(self, img_filename):
        return os.path.join(self.labels_path, file.get_file_name(img_filename) + self.label_file_extname)

    def get_annotation_content(self, img_path, annotation_objs, classes=None):
        return builder.get_annotation_content(img_path, annotation_objs)
