'''
File that read json settings file and return the values
'''

import json


def read_json(filename):
    ''' Read json file specified in filename param. '''
    if type(filename) not in [str]:
        return TypeError('File name must be a string')
    try:
        with open(filename, 'r') as file:
            settings = json.load(file)
        return settings
    except Exception as e:
        return e

if __name__ == '__main__':

    settings = read_json('')
    print(settings)
