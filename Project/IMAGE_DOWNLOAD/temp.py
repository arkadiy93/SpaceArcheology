import csv
import os
import np

datasets_path = os.path.join(os.getcwd(), os.pardir, os.pardir, "Datasets")

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

if __name__ == '__main__':
    folder = os.path.join(datasets_path, "Asia", 'test')
    file = os.path.join(folder, 'asian_classification.csv')
    data = os.path.join(folder, 'data')
    filenames = [f for f in os.listdir(data) if os.path.isfile(os.path.join(data, f))]
    filenamescsv = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count = line_count + 1
                continue
            filenamescsv.append(row[0])
    print(len(filenames))
    # for file in filenames:
    #     if file in filenamescsv:
    #         continue
        #os.remove(os.path.join(data, file))
    # non_exist = []
    #
    # for file in filenamescsv:
    #     if not file in inter:
    #         non_exist.append(file)
    #
    # print(non_exist)