import pandas as pd
from PIL import Image
from skimage import io, transform
import torch
from torch.utils.data import Dataset
import os
import numpy as np



class LoadBinaryDataSet(Dataset):
    def __init__(self,csv_file,img_dir,filetype,transform=None):
        #get image file names
        file_names = os.listdir(img_dir)
        self.full_filenames = []
        for f in file_names:
            if f.endswith('.' + filetype):
                self.full_filenames.append(os.path.join(img_dir,f))

        #get labels for images
        labels_data = os.path.join(img_dir,csv_file)
        labels_df = pd.read_csv(labels_data)
        labels_df.set_index("filename",inplace=True)
        self.labels = []
        for f in file_names:
            if f.endswith('.' + filetype):
                self.labels.append(labels_df.loc[f][0])
        self.transform = transform


    def __len__(self):
        return len(self.full_filenames)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        image = Image.open(self.full_filenames[idx])
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label