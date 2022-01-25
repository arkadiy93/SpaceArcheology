import os
import shutil
from pathlib import Path
import csv

def create_train_and_val_set(target_path,train_paths,val_paths,class_file_type,image_file_type,subfolder_name=None):
    if target_path.exists() and target_path.is_dir():
        shutil.rmtree(target_path)
    os.mkdir(target_path)
    os.mkdir(os.path.join(target_path, 'train'))
    os.mkdir(os.path.join(target_path, 'val'))
    for phase in [train_paths,val_paths]:
        file_list = []
        for path in phase:
            for file in os.listdir(os.path.join(path,subfolder_name)):
                if file.endswith('.' + class_file_type):
                    file_list.append(os.path.join(path,subfolder_name,file))

        if class_file_type == 'csv':
            if phase == train_paths:
                combine_csv_classification_files(file_list,os.path.join(target_path,'train'))
            else:
                combine_csv_classification_files(file_list, os.path.join(target_path, 'val'))

    for phase in [train_paths, val_paths]:
        for path in phase:
            for file in os.listdir(os.path.join(path,subfolder_name)):
                if file.endswith('.' + image_file_type):
                    if phase == train_paths:
                        shutil.copyfile(os.path.join(path,subfolder_name,file),os.path.join(target_path,'train',file))
                    else:
                        shutil.copyfile(os.path.join(path, subfolder_name, file), os.path.join(target_path,'val', file))

def combine_csv_classification_files(file_list,target_path):
    with open(os.path.join(target_path, "classification.csv"), "w", newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        write_header = True
        for file in file_list:
            with open(file,'r') as read_obj:
                csv_reader = csv.reader(read_obj)
                if write_header == True:
                    write_header = False
                else:
                    next(csv_reader)
                for row in csv_reader:
                    csv_writer.writerow(row)









if __name__ == '__main__':
    train_paths = []
    val_paths = []
    train_paths.append('C:\Bachelor Oppgave\Datasets\Qanats Iran-Afghanistan\Id-1-Iran-58.58042-34.35781-58.60262-34.33726-zoom=17')
    train_paths.append(
        'C:\Bachelor Oppgave\Datasets\Qanats Iran-Afghanistan\Id-4-Iran-56.92319-33.6569-56.93319-33.64689-zoom=17')
    val_paths.append(
        'C:\Bachelor Oppgave\Datasets\Qanats Iran-Afghanistan\Id-5-Iran-58.65562-34.29336-58.71141-34.26783-zoom=17')
    train_paths.append(
        'C:\Bachelor Oppgave\Datasets\Qanats Iran-Afghanistan\Id-6-Iran-58.20017-29.19981-58.24017-29.15981-zoom=17')
    train_paths.append(
        'C:\Bachelor Oppgave\Datasets\Qanats Iran-Afghanistan\Id-8-Iran-58.6836-34.31308-58.71122-34.29256-zoom=17')
    val_paths.append(
        'C:\Bachelor Oppgave\Datasets\Qanats Iran-Afghanistan\Id-9-Iran-52.96904-32.86582-52.99303-32.84661-zoom=17')

    test = create_train_and_val_set(Path('C:\Bachelor Oppgave\Project\Test_Dataset'),train_paths,val_paths,'csv','png','Resized_to_256')