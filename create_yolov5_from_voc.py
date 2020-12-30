import os
import argparse
import shutil

from datasets.data_format.voc import VOCDataSet
from datasets.data_format.yolo import YOLODataSet
from utils import dataset_converter
from projects.yolo import yolov5


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--voc_dataset_dir', type=str, help='pascal voc format dataset directory.')
    parser.add_argument('-p', '--yolov5_project_dir', type=str, help='save yolov5 project directory.')
    
    args = parser.parse_args()

    # path = '/Users/wjj/work/带电检测/infrared_temperature_measurement'

    voc_dataset_dir = args.voc_dataset_dir
    yolo_dataset_dir = os.path.join(os.path.split(voc_dataset_dir)[0], 'tmp_yolo')

    voc_dataset = VOCDataSet(voc_dataset_dir)
    yolo_dataset = YOLODataSet(yolo_dataset_dir)
    dataset_converter.voc2yolo(voc_dataset, yolo_dataset)

    project = yolov5.Project(args.yolov5_project_dir)
    project.create(yolo_dataset)

    shutil.rmtree(yolo_dataset_dir)
