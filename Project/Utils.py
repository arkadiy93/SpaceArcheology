import openpyxl
import os
import json

datasets_path = os.path.join(os.getcwd(), os.pardir, "Datasets")
source_file = os.path.join(datasets_path, "coords.txt")
target_file = os.path.join(datasets_path, "Fortress_Datasets_Uzbekistan.xlsx")
json_file = os.path.join(datasets_path, "2022-02-13T004540.200.json")
json_file2 = os.path.join(datasets_path, "2022-02-13T010907.200.json")
country = "Uzbekistan"
L = 0.001


def format(num):
    return round(num, 5)


def writeToTarget(data):
    workbook = openpyxl.load_workbook(target_file)
    sheet = workbook.active
    sheet.delete_rows(2, sheet.max_row)

    for data_entry in data:
        lat, long = data_entry

        longitude_top_left = long - L
        longitude_bottom_right = long + L
        latitude_bottom_right = lat - L
        latitude_top_left = lat + L
        sheet.append([
            format(longitude_top_left),
            format(latitude_top_left),
            format(longitude_bottom_right),
            format(latitude_bottom_right),
            country
        ])

    workbook.save(target_file)


def create_list_from_text_file():
    source = os.path.join(source_file)
    file = open(source, "r")
    content = file.read()
    lines = content.split("\n")
    data = []
    for line in lines:
        if not line.strip():
            continue
        lat, long, _ = line.split(",")
        data.append((float(lat), float(long)))

    writeToTarget(data)


def load_json():
    forts = []
    data = open(json_file)
    content = json.load(data)
    for entry in content.get('features'):
        props = entry.get('properties')
        if props.get('kind') == 'fort':
            forts.append(entry)


    coordinates = [(fort.get('geometry').get('coordinates'), fort.get('properties').get('id')) for fort in forts]
    return coordinates[:20]

def create_source_file(coords):
    source = os.path.join(source_file)
    with open(source, 'w') as file:
        for (coord, id) in coords:
            long, lang = coord
            file.write(",".join([str(lang), str(long), str(id)]))
            file.write("\n")


if __name__ == "__main__":
    coords = load_json()
    create_source_file(coords)

    create_list_from_text_file()
