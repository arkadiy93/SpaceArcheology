import os
import csv


def calc_stats(file):
    tp_dict = {}
    fp_dict = {}
    value_list = []
    with open(file, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        next(csv_reader)
        for row in csv_reader:
            value_list.append((row[15], row[14]))

    for i in range(len(value_list)):
        classification = value_list[i][0]
        value = value_list[i][1]

        if classification == 'tp':
            temp = tp_dict.get(value)
            if temp is None:
                tp_dict[value] = 1
            else:
                temp += 1
                tp_dict[value] = temp
        else:
            temp = fp_dict.get(value)
            if temp is None:
                fp_dict[value] = 1
            else:
                temp += 1
                fp_dict[value] = temp


    print(tp_dict)
    print(fp_dict)





if __name__ == '__main__':
    input_file = os.path.join('C:/Bachelor Thesis','SpaceArcheology','Datasets','SLRM_test.csv')
    calc_stats(input_file)