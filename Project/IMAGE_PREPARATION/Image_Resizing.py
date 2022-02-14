import os
from PIL import Image

datasets_path = os.path.join(os.getcwd(), os.pardir, os.pardir, "Datasets")


def resize_composite_images(path, max_size, filetype):
    subfolder_list = [f.path for f in os.scandir(path) if f.is_dir()]
    for folder in subfolder_list:
        resize_image(max_size, folder, filetype)


def resize_image(max_size, folder, filetype):
    for file in os.listdir(folder):
        if file.endswith('composite.' + filetype):
            temp_id = file.split('_')
            dataset_id = temp_id[1]
            filename = os.path.join(folder, file)
            temp_image = Image.open(filename)
            width, height = temp_image.size
            if width >= height and width > max_size:
                factor = width / max_size
                new_width = int(width / factor)
                new_height = int(height // factor)
            else:
                factor = height / max_size
                new_width = int(width / factor)
                new_height = int(height / factor)
            img = temp_image.resize((new_width, new_height))
            img.save(os.path.join(folder, 'ID_' + dataset_id + '_composite_resized.' + filetype))


if __name__ == '__main__':
    images_path = os.path.join(datasets_path, "Fortresses_Uzbekistan")
    resize_composite_images(images_path, 1024, 'png')
