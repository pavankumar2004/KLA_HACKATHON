import pandas as pd
import csv
import math


carearea = pd.read_csv("CareAreas.csv",header=None)
metadata = pd.read_csv("metadata.csv")


main_field_size = metadata.iloc[0, 0]
sub_field_size = metadata.iloc[0, 1]
print(main_field_size)
print(sub_field_size)


def main_field_placer():
    main_field_list = []
    for index, row in carearea.iterrows():
        x1 = row.iloc[1]
        x2 = row.iloc[2]
        y1 = row.iloc[3]
        y2 = row.iloc[4]
        print(x1," ",x2," ",y1," ",y2)
        x = math.ceil((x2-x1)/main_field_size)
        y = math.ceil((y2-y1)/main_field_size)
        for i in range(x):
            for j in range(y):
                main_field_x1 = x1 + (i * main_field_size)
                main_field_x2 = main_field_x1 + main_field_size
                main_field_y1 = y1 + (j * main_field_size)
                main_field_y2 = main_field_y1 + main_field_size
                main_field_list.append([main_field_x1,main_field_x2,main_field_y1,main_field_y2])
    return main_field_list

main_field = main_field_placer()
main_field = pd.DataFrame(main_field)
main_field.to_csv('Mainfield.csv',header=False)   

def subfield():
    sf = []
    for index, row in carearea.iterrows():
        x1 = row.iloc[1]
        x2 = row.iloc[2]
        y1 = row.iloc[3]
        y2 = row.iloc[4]
        
        nx = math.ceil((x2-x1)/sub_field_size)
        ny = math.ceil((y2-y1)/sub_field_size)

        for i in range(nx):
            for j in range(ny):
                sf_x1 = x1 + i * sub_field_size
                sf_x2 = sf_x1 + sub_field_size
                sf_y1 = y1 + j * sub_field_size
                sf_y2 = sf_y1 + sub_field_size
                sf.append([sf_x1,sf_x2,sf_y1,sf_y2,index]) 
    return pd.DataFrame(sf, columns=['x1', 'x2', 'y1', 'y2','MainFieldID'])

subfields = subfield()
subfields.to_csv("subfields.csv", header=False)


