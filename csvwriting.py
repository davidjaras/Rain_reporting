'''
csvwriting.csv

File that manages the local storage through csv files.
'''
import csv
import time
import datetime
from pathlib import Path


def verify_duplications(filename,data):
    '''
    Validate if the data to save was not saved before.
    '''
    duplicates_found = False
    my_file = Path(filename)

    if not my_file.is_file():
        print('File does not exist. Duplications were not found.')
    else:
        path = open(filename, 'r')
        file_list = ((path.read()).split('\n'))
        matched_data = ';'.join(map(str,data))
        if matched_data in file_list:
            duplicates_found = True
    return duplicates_found   


def write_file(filename, header, data):
    '''
    Save data in specified filename-path.
    '''
    try:
        my_file = Path(filename)
        if not my_file.is_file():
            path = open(filename, 'a',newline='\n')
            writer = csv.writer(path,delimiter=';')
            writer.writerow(header)
        else:
            path = open(filename, 'a')
            writer = csv.writer(path,delimiter=';')
            
        writer.writerow(data)
        path.close()            
        data_written = True
    except Exception as e:
        print("Something happend while trying to save in csv file: ")
        print(e)
        data_written = False

    return data_written


if __name__ == '__main__':
    pass
