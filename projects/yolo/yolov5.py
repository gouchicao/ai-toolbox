import os
import sys
import shutil
import random

from tqdm import tqdm
from datasets.data_format.voc import VOCDataSet
from datasets.data_format.yolo import builder


class Project(object):
    """目录结构
    project
    ├── data.yaml           #数据集配置文件
    ├── models              #网络模型（可以使用下面的脚本自动生成）
    │   ├── yolov5s.yaml    #Small
    │   ├── yolov5m.yaml    #Medium
    │   ├── yolov5l.yaml    #Large
    │   └── yolov5x.yaml    #XLarge
    ├── images              #图片
    │   ├── train           #训练集
    │   │   ├── 000001.jpg
    │   │   ├── 000002.jpg
    │   │   └── 000003.jpg
    │   └── val             #验证集
    │       ├── 000010.jpg
    │       └── 000011.jpg
    ├── labels              #YOLO格式的标注
    │   ├── train           #训练集
    │   │   ├── 000001.txt
    │   │   ├── 000002.txt
    │   │   └── 000003.txt
    │   └── val             #验证集
    │       ├── 000010.txt
    │       └── 000011.txt
    └── inference           #推理
        ├── images          #原图
        └── output          #推理后的标注图片
    """

    def __init__(self, project_dir='project', dataset_split_radio=0.2):
        train_dir = 'train'
        val_dir = 'val'

        self.project_dir = project_dir
        self.dataset_images_dir = os.path.join(project_dir, 'images')
        self.dataset_images_train_dir = os.path.join(self.dataset_images_dir, train_dir)
        self.dataset_images_val_dir = os.path.join(self.dataset_images_dir, val_dir)

        self.dataset_labels_dir = os.path.join(project_dir, 'labels')
        self.dataset_labels_train_dir = os.path.join(self.dataset_labels_dir, train_dir)
        self.dataset_labels_val_dir = os.path.join(self.dataset_labels_dir, val_dir)

        self.dataset_split_radio = dataset_split_radio


    def create(self, dataset):
        if os.path.exists(self.dataset_images_dir):
            shutil.rmtree(self.dataset_images_dir)

        os.makedirs(self.dataset_images_train_dir)
        os.makedirs(self.dataset_images_val_dir)

        if os.path.exists(self.dataset_labels_dir):
            shutil.rmtree(self.dataset_labels_dir)
            
        os.makedirs(self.dataset_labels_train_dir)
        os.makedirs(self.dataset_labels_val_dir)

        self._build_dataset(dataset)


    def _build_dataset(self, dataset):
        image_paths, label_paths, _ = dataset.load()
        
        assert(len(image_paths) == len(label_paths))

        image_size = len(image_paths)
        indexs = list(range(0, image_size))
        random.shuffle(indexs)

        split_size = int(image_size*self.dataset_split_radio)
        train_indexs, val_indexs = indexs[split_size:], indexs[:split_size]

        for i in tqdm(train_indexs):
            shutil.copy(image_paths[i], self.dataset_images_train_dir)
            shutil.copy(label_paths[i], self.dataset_labels_train_dir)

        for i in tqdm(val_indexs):
            shutil.copy(image_paths[i], self.dataset_images_val_dir)
            shutil.copy(label_paths[i], self.dataset_labels_val_dir)

        shutil.copy(dataset.classes_path, self.project_dir)
        