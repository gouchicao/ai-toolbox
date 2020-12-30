from PIL import Image


def get_image_size(img_path):
    with Image.open(img_path) as img:
        width, height = img.size

    return (width, height)
    