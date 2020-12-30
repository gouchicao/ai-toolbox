import logging
import os
import shutil

from tqdm import tqdm
from PIL import Image
from datasets import utils
from utils import file

logger = logging.getLogger('datasets.cctsdb')


def convert_dataset(source_path, dataset):
    logger.debug('Dataset Directory: %s', source_path)

    dataset.create()
    
    paths, datas, class_names = _load_original_data(source_path)
    for src_img_path, data in tqdm(zip(paths, datas)):
        img_filename = os.path.basename(src_img_path)

        target_img_path = dataset.get_image_path(img_filename)
        shutil.copy(src_img_path, dataset.images_path)

        annotation_path = dataset.get_annotation_path(img_filename)
        annotation_content = dataset.get_annotation_content(target_img_path, data, class_names)
        with open(annotation_path, "w") as f:
            f.write(annotation_content)

    file.write_lines(dataset.classes_path, class_names)


def _load_original_data(path):
    ground_truth_path = os.path.join(path, 'GroundTruth/GroundTruth.txt')
    ground_truths = file.get_lines(ground_truth_path)

    filename_and_annotation_info = {}
    for line in ground_truths:
        l = line.split(';')
        filename = l[0]
        if filename not in filename_and_annotation_info:
            filename_and_annotation_info[filename] = []
        filename_and_annotation_info[filename].append(l[1:])
    
    images_path = os.path.join(path, 'Images')
    image_filenames = utils.get_file_paths_by_iteration(images_path)

    filtered_paths = []
    filtered_datas = []
    for filename in image_filenames:
        name = os.path.basename(filename)
        if name in filename_and_annotation_info:
            filtered_paths.append(filename)
            filtered_datas.append(filename_and_annotation_info[name])

    class_names = _get_sorted_class_names(filtered_datas)
    return (filtered_paths, filtered_datas, class_names)    


def _get_sorted_class_names(datas):
    class_names = set()

    for data in datas:
        for item in data:
            _, _, _, _, class_name = item
            class_names.add(class_name)

    return sorted(class_names)
