import csv
import os

def renumber_images(number_of_digits,base_folder,image_type,classification_type):
    for dir in os.listdir(base_folder):
        for file in os.listdir(os.path.join(base_folder,dir)):
            if file.endswith('.' + image_type):
                file_number, file_type = file.split('.')[0], file.split('.')[1]
                digits_to_add = number_of_digits - len(file_number)
                os.rename(os.path.join(base_folder,dir,file), os.path.join(base_folder,dir,digits_to_add*'0' + file_number + '.' + file_type))
            if file.endswith('.' + classification_type):
                file_number, file_type = file.split('.')[0], file.split('.')[1]
                digits_to_add = number_of_digits - len(file_number)
                with open(os.path.join(base_folder,dir,digits_to_add*'0' + file_number + '.' + file_type), "w", newline='') as write_obj:
                    csv_writer = csv.writer(write_obj)
                    with open(os.path.join(base_folder,dir,file), "r", newline='') as read_obj:
                        csv_reader = csv.reader(read_obj)
                        for row in csv_reader:
                            if row[0] == (file_number + '.' + image_type):
                                row[0] = digits_to_add*'0' + file_number + '.' + image_type
                            csv_writer.writerow(row)
                os.remove(os.path.join(base_folder,dir,file_number + '.' + file_type))








if __name__ == '__main__':
    renumber_images(5,'C:\Bachelor Thesis\Mound PNG','png','csv')