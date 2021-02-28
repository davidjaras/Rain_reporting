'''
File that test the different modules in Rain_reporting Project.

This file contains a class for each .py so the test run independently.

'''

# Python Core Libraries
import unittest
import json
import random

# Project modules
import csvwriting
import dbmanager
import pulsed_sensor
import sampling_time
import settings


class TestCsvWritting(unittest.TestCase):
    pass


class TestDBManager(unittest.TestCase):
    pass


class TestPulsedSensor(unittest.TestCase):
    pass


class TestSamplingTime(unittest.TestCase):
    pass


class TestSettings(unittest.TestCase):
    '''
    Class that test settings module.
    '''

    '''
    Following methods are test cases to the function read_json()
    '''
    # Given a correct filename return a json object
    def test_read_json(self):
        self.assertIsInstance(settings.read_json('settings.json'), dict)
    
    # Given a wrong param type (not string) raise an error
    def test_wrong_param_type(self):
        cases = [123, [], {}, 1.585, None]
        for case in cases:
            self.assertRaises(TypeError, settings.read_json(case), True)

    # Given a string with wrong filename param raise a FileNotFoundError
    def test_wrong_filename(self):
        self.assertIsInstance(settings.read_json(''), FileNotFoundError)
    
    # Given a right param but settings.json file contains errors raise an error
    def test_wrong_sintax_json(self):
        self.assertIsInstance(settings.read_json('bad_syntax_file.json'), json.decoder.JSONDecodeError)


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=1, exit=False)