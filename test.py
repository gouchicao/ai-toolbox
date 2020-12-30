import os

from datasets.open_source import cctsdb
from projects.yolo import yolov5

from datasets.data_format.voc import VOCDataSet
from datasets.data_format.yolo import YOLODataSet

from utils import dataset_converter


path = 'CCTSDB (CSUST Chinese Traffic Sign Detection Benchmark)'


def to_voc():
    dataset = VOCDataSet(os.path.join(path, 'voc'))
    cctsdb.convert_dataset(path, dataset)


def to_yolo():
    dataset = YOLODataSet(os.path.join(path, 'yolo'))
    cctsdb.convert_dataset(path, dataset)


def voc2yolo():
    voc_dataset = VOCDataSet(os.path.join(path, 'voc'))
    yolo_dataset = YOLODataSet(os.path.join(path, 'voc2yolo'))

    dataset_converter.voc2yolo(voc_dataset, yolo_dataset)


def create_project_yolov5():
    # dataset = VOCDataSet(os.path.join(path, 'voc'))
    dataset = YOLODataSet(os.path.join(path, 'yolo'))
    project = yolov5.Project(os.path.join(path, 'project'))
    project.create(dataset)


if __name__ == "__main__":
    to_voc()
    to_yolo()
    voc2yolo()
    create_project_yolov5()
