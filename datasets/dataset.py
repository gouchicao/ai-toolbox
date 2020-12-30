import os
import shutil

from datasets import utils
from utils import file

import xml.etree.ElementTree as ET


class DataSet(object):

    def __init__(self, path, label_file_extname):
        self.base_dir = path
        self.label_file_extname = label_file_extname
        self.images_path = os.path.join(self.base_dir, 'images')
        self.labels_path = os.path.join(self.base_dir, 'labels')
        self.classes_path = os.path.join(self.base_dir, 'classes.txt')

    def create(self):
        if os.path.exists(self.images_path):
            shutil.rmtree(self.images_path)
        if os.path.exists(self.labels_path):
            shutil.rmtree(self.labels_path)

        os.makedirs(self.images_path)
        os.makedirs(self.labels_path)

    def load(self):
        image_paths = utils.get_image_paths(self.images_path)
        label_paths = utils.get_file_paths(self.labels_path, [self.label_file_extname])

        file_names = {file.get_file_name(path) : path for path in label_paths}

        filtered_image_paths = []
        filtered_label_paths = []
        for path in image_paths:
            file_name = file.get_file_name(path)
            if file_name in file_names.keys():
                filtered_image_paths.append(path)
                filtered_label_paths.append(file_names[file_name])

        if not os.path.exists(self.classes_path):
            self._generate_classes_file(filtered_label_paths)

        classes = file.get_lines(self.classes_path)
        if not classes:
            classes

        return (filtered_image_paths, filtered_label_paths, classes)

    def _generate_classes_file(self, label_paths):
        class_names = set()

        for label_path in label_paths:
            with open(label_path, "r") as in_file:
                tree=ET.parse(in_file)
                root = tree.getroot()

                for obj in root.iter('object'):
                    difficult = obj.find('difficult').text
                    cls = obj.find('name').text
                    if int(difficult)==1:
                        continue
                    
                    class_names.add(cls)

        class_names = sorted(class_names)
        file.write_lines(self.classes_path, class_names)
        
    def get_label_paths(self):
        pass

    def get_image_path(self, filename):
        return os.path.join(self.images_path, filename)
    
    def get_annotation_path(self, img_filename):
        return os.path.join(self.images_path, img_filename)
    
    def get_annotation_content(self, img_path, annotation_objs, classes=None):
        pass