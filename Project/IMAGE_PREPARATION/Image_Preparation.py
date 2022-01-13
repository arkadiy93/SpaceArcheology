import os
import shutil
from pathlib import Path
from PIL import Image


def image_splitter(model_type, path):
    if model_type == 'DenseNet-201':
        store_path = Path(os.path.join(path, model_type))
        if store_path.exists() and store_path.is_dir():
            shutil.rmtree(store_path)
        os.mkdir(store_path)
        size = 256
    elif model_type == 'EfficientNet-B3':
        store_path = Path(os.path.join(path, model_type))
        if store_path.exists() and store_path.is_dir():
            shutil.rmtree(store_path)
        os.mkdir(store_path)
        size = 256
    elif model_type == 'ResNet-152':
        store_path = Path(os.path.join(path, model_type))
        if store_path.exists() and store_path.is_dir():
            shutil.rmtree(store_path)
        os.mkdir(store_path)
        size = 224
    temp_id = path.split('Id-')
    id = temp_id[-1][0]
    for file in os.listdir(path):
        if file.endswith('composite.png'):
            filename = os.path.join(path, file)
    split_image(size, filename, store_path, id)


def split_image(size,filename,store_path,id):
    temp_image = Image.open(filename)
    image_width, image_height = temp_image.size
    temp_size = 256
    for i in range(image_height // temp_size):
        for j in range(image_width // temp_size):
            box = (j * temp_size, i * temp_size, (j + 1) * temp_size, (i + 1) * temp_size)
            img = Image.new('RGB', (temp_size, temp_size), 255)
            img.paste(temp_image.crop(box))
            if size != 256:
                img = img.resize((size,size))
            path = os.path.join(store_path, 'ID=' + str(id) + '_x=' + str(j) + '_y=' + str(i) + '.png')
            img.save(path)


def prepare_images(path, model_list):
    if len(model_list) == 0:
        print('No models are specified for preparation of images')
    else:
        subfolders_list = [f.path for f in os.scandir(path) if f.is_dir()]
        for folder in subfolders_list:
            for model in model_list:
                image_splitter(model,folder)



if __name__ == '__main__':
    model_list = ['DenseNet-201','EfficientNet-B3','ResNet-152']
    prepare_images(os.path.join("c:\\", "Bachelor Oppgave", "Datasets", "Fortresses Iran-Pakistan"),model_list)