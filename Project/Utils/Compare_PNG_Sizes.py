import shutil
from PIL import Image
import os
import xlrd
from pathlib import Path


def compare_image_sizes(folder_list,start_image_number,end_image_number):
    error_list = []
    size_dict = {}
    counter = 0
    for folder in folder_list:
        counter += 1
        if counter == 1:
            for i in range(start_image_number,end_image_number+1):
                temp_image = Image.open(os.path.join(folder_list[counter-1], str(i) + ".png"))
                image_width, image_height = temp_image.size
                size_dict[i] = (image_width,image_height)
        else:
            for i in range(start_image_number,end_image_number+1):
                temp_image = Image.open(os.path.join(folder_list[counter-1], str(i) + ".png"))
                image_width, image_height = temp_image.size
                if size_dict[i][0] != image_width or size_dict[i][1] != image_height:
                    error_list.append((i, folder))


    print(error_list)



if __name__ == '__main__':
    folder_list = []
    folder_list.append("C:/Bachelor Thesis/Mound PNG/Slope")
    folder_list.append("C:/Bachelor Thesis/Mound PNG/MSRM_x1")
    folder_list.append("C:/Bachelor Thesis/Mound PNG/MSRM_x2")
    folder_list.append("C:/Bachelor Thesis/Mound PNG/SLRM")
    folder_list.append("C:/Bachelor Thesis/Mound PNG/MSRM_x1_No_RGB")
    folder_list.append("C:/Bachelor Thesis/Mound PNG/MSRM_x2_No_RGB")
    folder_list.append("C:/Bachelor Thesis/Mound PNG/Slope_No_RGB")
    folder_list.append("C:/Bachelor Thesis/Mound PNG/SLRM_No_RGB")
    compare_image_sizes(folder_list,398,2567)