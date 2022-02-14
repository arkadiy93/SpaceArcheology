from pip._vendor import requests
from furl import furl
import mercantile
import os
from PIL import Image
from io import BytesIO
import openpyxl

datasets_path = os.path.join(os.getcwd(), os.pardir, os.pardir, "Datasets")
zoom = 17
TILE_SIZE = 512

MB_KEY = 'sk.eyJ1IjoiZml2ZWwxOTc0IiwiYSI6ImNreHl4b244NTJ2a3AycG12aWVycnRwb2UifQ.C1-Dw9HwshZUzNE7TIKmmQ'
SOURCE_URL = "https://api.mapbox.com/v4/mapbox.satellite"


def download_and_store_datasets(file, folder):
    dataset_list = import_dataset_info(file)
    for i, data in enumerate(dataset_list):
        image_id = i + 1
        download_image(data, folder, image_id)
    print("done")


def import_dataset_info(file):
    dataset_list = []
    workbook = openpyxl.load_workbook(file)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2):
        cell_values = tuple([cell.value for cell in row])
        dataset_list.append(cell_values)

    return dataset_list


def download_image(data, folder, image_id):
    longitude_top_left, latitude_top_left, longitude_bottom_right, latitude_bottom_right, country = data

    # Parameters for mercantile.tiles is (east,south,west,north,zoom).
    tile_list = list(
        mercantile.tiles(longitude_top_left, latitude_bottom_right, longitude_bottom_right, latitude_top_left, zoom)
    )

    if len(tile_list) == 0 or len(tile_list) > 500:
        raise ValueError('Number of tiles returned are 0 or larger than 500. Check coordinate input.')

    parts = [
        'Id',
        image_id,
        country,
        longitude_top_left,
        latitude_top_left,
        longitude_bottom_right,
        latitude_bottom_right,
        'zoom={}'.format(zoom),
    ]

    tiles_folder_name = "-".join(str(value) for value in parts)
    path_to_tiles = os.path.join(folder, tiles_folder_name)

    if not os.path.isdir(path_to_tiles):
        os.mkdir(path_to_tiles)

    first_tile, last_tile = tile_list[0], tile_list[-1]
    xMin, yMin = first_tile.x, first_tile.y
    xMax, yMax = last_tile.x, last_tile.y

    rows = yMax - yMin + 1
    cols = xMax - xMin + 1


    composite_image = Image.new('RGB', (TILE_SIZE * cols, TILE_SIZE * rows))

    x_coords = list(dict.fromkeys([tile.x for tile in tile_list]))
    y_coords = list(dict.fromkeys([tile.y for tile in tile_list]))
    for i, tile in enumerate(tile_list):
        tile_img = download_tile(tile)
        x_position = x_coords.index(tile.x) * TILE_SIZE
        y_position = y_coords.index(tile.y) * TILE_SIZE
        composite_image.paste(tile_img, (x_position, y_position))

    composite_image_name = "_".join(['ID', str(image_id), "composite"])
    composite_image_path = os.path.join(path_to_tiles, "{}.png".format(composite_image_name))
    composite_image.save(composite_image_path)


def download_tile(tile):
    url = furl(SOURCE_URL) \
        .add(path=str(zoom)) \
        .add(path=str(tile.x)) \
        .add(path="{}@2x.pngraw".format(str(tile.y))) \
        .add(query_params={'access_token': str(MB_KEY)}).url

    response = requests.get(url, stream=True)
    return Image.open(BytesIO(response.content))


if __name__ == '__main__':
    print("start")
    # qanat_file = os.path.join(datasets_path, "Qanat_Datasets_Iran-Afghanistan.xlsx")
    # qanat_folder = os.path.join(datasets_path, "Qanats Iran-Afghanistan")
    # fortress_file = os.path.join(datasets_path, "Fortress_Datasets_Iran-Pakistan.xlsx")
    # fortress_folder = os.path.join(datasets_path, "Fortresses Iran-Pakistan")
    fortress_file_uzbek = os.path.join(datasets_path, "Fortress_Datasets_Uzbekistan.xlsx")
    fortress_folder_uzbek = os.path.join(datasets_path, "Fortresses_Uzbekistan")

    download_and_store_datasets(fortress_file_uzbek, fortress_folder_uzbek)
