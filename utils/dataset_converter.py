import os
import shutil

import xml.etree.ElementTree as ET

from tqdm import tqdm

from datasets.data_format import yolo
from utils import file


def voc2yolo(source_dataset, target_dataset):
    target_dataset.create()
    
    images, labels, class_names = source_dataset.load()
    for image_path, label_path in tqdm(zip(images, labels)):
        img_filename = os.path.basename(image_path)

        target_img_path = target_dataset.get_image_path(img_filename)
        shutil.copy(image_path, target_dataset.images_path)

        annotation_path = target_dataset.get_annotation_path(img_filename)
        annotation_content = _voc2yolo(label_path, class_names)
        with open(annotation_path, "w") as f:
            f.write(annotation_content)

    shutil.copy(source_dataset.classes_path, target_dataset.classes_path)
        

def _voc2yolo(voc_label_file, classes):
    yolo_lines = []

    with open(voc_label_file, "r") as in_file:
        tree=ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult)==1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), 
                 float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = yolo.convert_yolo_size((w,h), b)
            yolo_lines.append(str(cls_id) + " " + " ".join([str(a) for a in bb]) + os.linesep)

    return ''.join(yolo_lines)
