'''
File that read json settings file and return the values
'''

import json


# Constants definition
DEFAULT_SAMPLETIME = 5
DEFAULT_SAMPLETIME_UNIT = 'seconds'
TIME_UNITS = {
    'SECONDS': 'seconds',
    'MINUTES': 'minutes'
}
WAIT = {
    'SECOND': 1,
    'MINUTE': 60  # integer of minute is given by its equivalence in seconds
}
VALID_SECOND_OR_MINUTE = list(range(1, 60))


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
    pass
