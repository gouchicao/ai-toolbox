import os

from datasets.open_source import cctsdb
from projects.yolo import yolov5

from datasets.data_format.yolo import YOLODataSet


path = '/Users/wjj/work/tmp/CCTSDB (CSUST Chinese Traffic Sign Detection Benchmark)'


dataset = YOLODataSet(os.path.join(path, 'yolo'))
cctsdb.convert_dataset(path, dataset)

project = yolov5.Project(os.path.join(path, 'project'))
project.create(dataset)
