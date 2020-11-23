import os
import shutil

from tqdm import tqdm
from PIL import Image
from datasets import utils
from datasets.data_format.voc import voc


def write_voc(path):
    voc_dir = os.path.join(path, 'voc')
    if os.path.exists(voc_dir):
        shutil.rmtree(voc_dir)
    os.makedirs(voc_dir)

    images_path = os.path.join(voc_dir, 'images')
    labels_path = os.path.join(voc_dir, 'labels')
    os.makedirs(images_path)
    os.makedirs(labels_path)

    paths, labels = _load_data(path)
    for src_img_path, label in tqdm(zip(paths, labels)):
        img_filename = os.path.basename(src_img_path)
        target_img_path = os.path.join(images_path, img_filename)
        shutil.copy(src_img_path, images_path)
        xml_path = os.path.join(labels_path, os.path.splitext(img_filename)[0]+'.xml')
        xml = voc.gen_xml(target_img_path, label)
        with open(xml_path, "w") as xml_file:
            xml_file.write(xml)


def _load_data(path):
    ground_truth_path = os.path.join(path, 'GroundTruth/GroundTruth.txt')
    ground_truths = utils.get_filelines(ground_truth_path)

    d = {}
    for line in ground_truths:
        l = line.split(';')
        filename = l[0]
        if filename not in d:
            d[filename] = []
        d[filename].append(l)
    
    images_path = os.path.join(path, 'Images')
    image_filenames = utils.get_file_paths(images_path)

    filtered_paths = []
    filtered_labels = []
    for filename in image_filenames:
        name = os.path.basename(filename)
        if name in d:
            filtered_paths.append(filename)
            filtered_labels.append(d[name])

    return (filtered_paths, filtered_labels)    
