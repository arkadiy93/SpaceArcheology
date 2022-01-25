import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets,models,transforms
from torch.utils.data import Dataset
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, Subset
import time
import os
import copy
import pandas as pd
from skimage import io
from CustomDatasets import *
import torchvision.transforms as transforms


torch.manual_seed(0)


#Parameters for training and validation
in_channels = 1
num_classes = 2
learning_rate = 0.0001
batch_size = 10
num_epochs = 15
momentum = 0.9
step_size = 5
gamma = 0.1

#Image Transforms
image_transforms = {
    "train": transforms.Compose([
       transforms.RandomResizedCrop(224),
       transforms.RandomHorizontalFlip(),
       transforms.ToTensor(),
       transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ]),
    "val": transforms.Compose([
       transforms.Resize(224),
       transforms.ToTensor()
    ])
}

#Loading data sets should be functions
train_set = LoadBinaryDataSet(csv_file='classification.csv',img_dir='C:\Bachelor Oppgave\Project\Test_Dataset\\train',filetype='png',transform=image_transforms['train'])
val_set = LoadBinaryDataSet(csv_file='classification.csv',img_dir='C:\Bachelor Oppgave\Project\Test_Dataset\\val',filetype='png',transform=image_transforms['val'])


train_loader = DataLoader(dataset=train_set,batch_size=batch_size,shuffle=True)
val_loader = DataLoader(dataset=val_set,batch_size=batch_size,shuffle=True)

#Device setup
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#device = torch.device("cpu")

#Transfer learning and validation loop.
def train_and_validate_model(model,criterion,optimizer,scheduler,num=num_epochs):
    since = time.time()

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0



    for epoch in range(num_epochs):

        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            running_train_loss = 0.0
            running_train_corrects = 0.0
            running_val_loss = 0.0
            running_val_corrects = 0.0

            #Iterate data
            if phase == 'train':
                for image, label in train_loader:
                    inputs = image
                    labels = label
                    inputs = inputs.to(device)
                    labels = labels.to(device)

                    # zero parameter gradients
                    optimizer.zero_grad()


                    with torch.set_grad_enabled(phase == 'train'):
                        outputs = model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs,labels)

                        loss.backward()
                        optimizer.step()

                    running_train_loss += loss.item() * inputs.size(0)
                    running_train_corrects += torch.sum(preds == labels.data)
                scheduler.step()
            else:
                for image, label in val_loader:
                    inputs = image
                    labels = label
                    inputs = inputs.to(device)
                    labels = labels.to(device)

                    # zero parameter gradients
                    optimizer.zero_grad()

                    with torch.set_grad_enabled(phase == 'train'):
                        outputs = model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)

                    running_val_loss += loss.item() * inputs.size(0)
                    running_val_corrects += torch.sum(preds == labels.data)

            if phase == 'train':
                epoch_loss = running_train_loss / len(train_set)
                epoch_acc = running_train_corrects / len(train_set)
            else:
                epoch_loss = running_val_loss / len(val_set)
                epoch_acc = running_val_corrects / len(val_set)
            print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                phase, epoch_loss, epoch_acc))

            if phase == 'val' and best_acc > epoch_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
        print()

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model

#Store model

#Write results

#Test stored model


# Initialize network
model = models.resnet18(pretrained=True)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs,2)

model = model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=momentum)
exp_lr_scheduler = lr_scheduler.StepLR(optimizer,step_size=step_size,gamma=gamma)

model = train_and_validate_model(model,criterion,optimizer,exp_lr_scheduler,num_epochs)





