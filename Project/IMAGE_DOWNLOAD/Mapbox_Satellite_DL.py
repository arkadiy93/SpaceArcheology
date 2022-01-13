from pip._vendor import requests
import shutil
import mercantile
import os
from PIL import Image
import openpyxl



MB_KEY = 'sk.eyJ1IjoiZml2ZWwxOTc0IiwiYSI6ImNreHl4b244NTJ2a3AycG12aWVycnRwb2UifQ.C1-Dw9HwshZUzNE7TIKmmQ'


def download_tiles(longitude_top_left,latitude_top_left,longitude_bottom_right,latitude_bottom_right,country,zoom,folder, image_id):

    #Parameters for mercantile.tiles is (east,south,west,north,zoom).
    tile_list = list(mercantile.tiles(longitude_top_left, latitude_bottom_right, longitude_bottom_right, latitude_top_left, zoom))
    if len(tile_list) == 0 or len(tile_list) > 500:
        print("Number of tiles returned are 0 or larger than 500. Check coordinate input.")
    else:
        os.mkdir(os.path.join(folder,'Id-' + str(image_id) + '-' + str(country) + '-' + str(longitude_top_left) + '-' + str(latitude_top_left) + '-' + str(longitude_bottom_right) + '-' + str(latitude_bottom_right) + '-' + 'zoom=' + str(zoom)))
        folder = os.path.join(folder,'Id-' + str(image_id) + '-' + str(country) + '-' + str(longitude_top_left) + '-' + str(latitude_top_left) + '-' + str(longitude_bottom_right) + '-' + str(latitude_bottom_right) + '-' + 'zoom=' + str(zoom))
        xMax,xMin,yMax,yMin = tile_list[0][0],tile_list[0][0],tile_list[0][1],tile_list[0][1]
        for i in range(len(tile_list)):
            if int(tile_list[i][0]) > xMax:
                xMax = int(tile_list[i][0])
            if int(tile_list[i][0]) < xMin:
                xMin = int(tile_list[i][0])
            if int(tile_list[i][1]) > yMax:
                yMax = int(tile_list[i][1])
            if int(tile_list[i][1]) < yMin:
                yMin = int(tile_list[i][1])


        for i in range(len(tile_list)):

                r = requests.get('https://api.mapbox.com/v4/mapbox.satellite/' +
                                str(zoom) + '/' + str(tile_list[i][0]) + '/' + str(tile_list[i][1]) + '@2x.pngraw?access_token=' + str(MB_KEY), stream=True)

                with open(folder + '\\' + str(tile_list[i][0]) + '.' + str(tile_list[i][1]) + '.png','wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

        create_composite_image(folder,xMin,xMax,yMin,yMax, image_id)

def create_composite_image(folder,xMin,xMax,yMin,yMax,image_id):

    composite_image = Image.new('RGB',(512*(xMax-xMin+1),512*(yMax-yMin+1)))

    for i in range(0,xMax-xMin+1):
        for j in range(0,yMax-yMin+1):
            temp_image = Image.open(folder + '\\' + str(xMin+i) + '.' + str(yMin+j) + '.png')
            composite_image.paste(temp_image,((i)*512, (j)*512))

    composite_image.save(folder + '\\ID_' + str(image_id) + '_composite.png')

def import_dataset_info(file):
    loc = (file)
    wb = openpyxl.load_workbook(loc)
    sheet = wb.active
    nrows = sheet.max_row
    dataset_list = []
    for i in range(2,nrows+1):
        temp_tuple = (sheet.cell(i,1).value,sheet.cell(i,2).value,sheet.cell(i,3).value,sheet.cell(i,4).value,sheet.cell(i,5).value)
        dataset_list.append(temp_tuple)
    return dataset_list

def download_and_store_datasets(file,folder,zoom):
    dataset_list = import_dataset_info(file)
    image_id = 1
    for i in range(len(dataset_list)):
        download_tiles(dataset_list[i][0],dataset_list[i][1], dataset_list[i][2], dataset_list[i][3], dataset_list[i][4],
                       zoom, folder, image_id)
        image_id += 1

if __name__ == '__main__':
    qanat_file = os.path.join("c:\\","Bachelor Oppgave","Datasets","Qanat_Datasets_Iran-Afghanistan.xlsx")
    qanat_folder = os.path.join("c:\\", "Bachelor Oppgave", "Datasets", "Qanats Iran-Afghanistan")
    fortress_file = os.path.join("c:\\", "Bachelor Oppgave", "Datasets", "Fortress_Datasets_Iran-Pakistan.xlsx")
    fortress_folder = os.path.join("c:\\", "Bachelor Oppgave", "Datasets", "Fortresses Iran-Pakistan")
    zoom = 17
    download_and_store_datasets(qanat_file,qanat_folder,17)
    download_and_store_datasets(fortress_file, fortress_folder, 17)