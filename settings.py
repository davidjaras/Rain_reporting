'''
File that read json settings file and return the values
'''

import json


def read_json(filename):
    ''' Read json file specified in filename param. '''
    with open(filename, 'r') as file:
        settings = json.load(file)
    return settings


if __name__ == '__main__':

    settings = read_json('settings.json')
    print(settings)
