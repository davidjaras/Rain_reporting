'''
File that test the different modules in Rain_reporting Project.

This file contains a class for each .py so the test run independently.

'''

# Python Core Libraries
import unittest
import json
import random
import datetime
import sys

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
    '''
    Class that test pulsed_sensor module.
    '''

    '''
    Following methods are test cases to the function get_current_time()
    '''
    def test_get_current_time(self):
        self.assertIsInstance(pulsed_sensor.get_current_time(), str)


class TestSamplingTime(unittest.TestCase):
    '''
    Class that test sampling_time module.
    '''

    '''
    Following methods are test cases to the function time_to_take_sample()
    '''
    # Given zero params, set default values, must return datetime object
    # and a boolean
    def test_zero_params(self):
        datetime_object, boolean = sampling_time.time_to_take_sample()
        self.assertIsInstance(datetime_object, datetime.datetime)
        self.assertIsInstance(boolean, bool)

    # Given sampletime_unit different of minutes or seconds, set default value
    # must return datetime object and a boolean
    def test_wrong_sampletime_unit(self):
        datetime_object, boolean = (
            sampling_time.time_to_take_sample(sampletime_unit='random_word')
        )
        self.assertIsInstance(datetime_object, datetime.datetime)
        self.assertIsInstance(boolean, bool)

    # Given sampletime out of the range 1 to 59, set default value
    # must return datetime object and a boolean
    def test_wrong_sampletime_range(self):
        max_int = sys.maxsize
        cases = [0, random.randint(60, max_int), -random.randint(1, max_int)]
        for case in cases:
            datetime_object, boolean = (
                sampling_time.time_to_take_sample(sampletime=case)
                )
            self.assertIsInstance(datetime_object, datetime.datetime)
            self.assertIsInstance(boolean, bool)

    # Given correct sampletime, sampletime_unit, and these matches with a
    # current time must return datetime object and a True boolean
    def test_return_true(self):
        cases = ['seconds', 'minutes']
        for case in cases:
            sampletime = random.randint(1, 59)  # set random value to min - sec
            now = datetime.datetime.now()  # get other time values
            date_time_test = datetime.datetime(  # set datetime for test
                                                year=now.year,
                                                month=now.month,
                                                day=now.day,
                                                hour=now.hour,
                                                minute=sampletime,
                                                second=sampletime
                                            )
            datetime_object, boolean = (
                sampling_time.time_to_take_sample(
                                                sampletime=sampletime,
                                                sampletime_unit=case,
                                                now=date_time_test
                                                )
            )
            self.assertIsInstance(datetime_object, datetime.datetime)
            self.assertIsInstance(boolean, bool)
            self.assertTrue(boolean)

    # Given correct sampletime, sampletime_unit, and these doesn't matches
    # with a current time must return datetime object and a False boolean
    def test_return_false(self):
        cases = ['seconds', 'minutes']
        for case in cases:
            sampletime = 13  # set random value to min - sec
            now = datetime.datetime.now()  # get other time values
            date_time_test = datetime.datetime(  # set datetime for test
                                                year=now.year,
                                                month=now.month,
                                                day=now.day,
                                                hour=now.hour,
                                                minute=20,
                                                second=20
                                            )
            datetime_object, boolean = (
                sampling_time.time_to_take_sample(
                                                sampletime=sampletime,
                                                sampletime_unit=case,
                                                now=date_time_test
                                                )
            )
            self.assertIsInstance(datetime_object, datetime.datetime)
            self.assertIsInstance(boolean, bool)
            self.assertFalse(boolean)

    '''
    Following methods are test cases to the function calibrate_minute()
    '''
    # Given a time with second equal to zero must return True
    def test_calibrate_minute_at_second_zero(self):
        now = datetime.datetime.now()
        test_time = datetime.datetime(
                                    year=now.year,
                                    month=now.month,
                                    day=now.day
                                    )
        self.assertTrue(sampling_time.calibrate_minute(test_time))

    # Given a current time wait until second is equal to zero must return True
    def test_calibrate_minute(self):
        self.assertTrue(sampling_time.calibrate_minute())

    # Given objects that are not instances of datetime.datetime set default
    # value to datetime.now() must return True
    def test_calibrate_minute_wrong_param(self):
        cases = [123, [], {}, 1.585, None]
        for case in cases:
            self.assertTrue(sampling_time.calibrate_minute(case))

    '''
    Following methods are test cases to the function delay_to_take_sample()
    '''
    # Given zero params sets default params must return a datetime.datetime
    # instance
    def test_delay_sample_zero_params(self):
        self.assertIsInstance(
                            sampling_time.delay_to_take_sample(),
                            datetime.datetime
                            )

    # Given sampletime_unit different of minutes or seconds, set default
    # value, must return datetime object and a boolean
    def test_delay_sample_wrong_sampletime_unit(self):
        datetime_object = (
            sampling_time.delay_to_take_sample(sampletime_unit='random_word')
        )
        self.assertIsInstance(datetime_object, datetime.datetime)

    # Given sampletime out of the range 1 to 59 (min or sec), set default
    # value must return datetime object and a boolean
    def test_delay_sample_wrong_sampletime_range(self):
        max_int = sys.maxsize
        cases = [0, random.randint(60, max_int), -random.randint(1, max_int)]
        for case in cases:
            datetime_object = (
                sampling_time.delay_to_take_sample(sampletime=case)
                )
            self.assertIsInstance(datetime_object, datetime.datetime)


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
        self.assertIsInstance(
                            settings.read_json('bad_syntax_file.json'),
                            json.decoder.JSONDecodeError
                            )


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=1, exit=False)
