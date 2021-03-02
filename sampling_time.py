'''
sampling_time.py

File with functions that watch time to sampling pulses
'''

# Python Core Libraries
from datetime import datetime, timedelta
import time

# Project modules
import settings as S


def time_to_take_sample(sampletime=S.DEFAULT_SAMPLETIME,
                        sampletime_unit=S.DEFAULT_SAMPLETIME_UNIT,
                        now=datetime.now()):
    '''
    Depending of sampletime and its unit
    Return if it's time to take a sample.

    Default values in params are unchangeable by settings or user
    interactions.
    '''
    if sampletime not in S.VALID_SECOND_OR_MINUTE:
        # here may be a warning notice. Out of range
        sampletime = S.DEFAULT_SAMPLETIME

    if sampletime_unit.lower() == S.TIME_UNITS.get('SECONDS'):
        step_time = now.second
    elif sampletime_unit.lower() == S.TIME_UNITS.get('MINUTES'):
        step_time = now.minute
    else:
        # here may be a warning notice code
        step_time = now.minute

    if step_time % sampletime == 0:
        return now, True

    return now, False


def calibrate_minute(now=datetime.now()):
    '''
    Sets the time step when it is on the minute scale to step every
    time the sencods are zero
    '''
    if not isinstance(now, datetime):
        now = datetime.now()

    second = now.second
    if second == 0:
        return True
    wait_to_second_zero = 60 - second
    time.sleep(wait_to_second_zero)
    return True


def delay_to_take_sample(sampletime=S.DEFAULT_SAMPLETIME,
                         sampletime_unit=S.DEFAULT_SAMPLETIME_UNIT):
    '''
    Sets the delay to validate if it is time to take a sample
    '''
    take_sample = False
    sampletime_unit = sampletime_unit.lower()

    if sampletime not in S.VALID_SECOND_OR_MINUTE:
        # here may be a warning notice. Out of range
        sampletime = S.DEFAULT_SAMPLETIME

    if sampletime_unit not in S.TIME_UNITS.values():
        sampletime_unit = S.DEFAULT_SAMPLETIME_UNIT

    if sampletime_unit == S.TIME_UNITS.get('SECONDS'):
        wait = S.WAIT.get('SECOND')
    if sampletime_unit == S.TIME_UNITS.get('MINUTES'):
        calibrate_minute()
        wait = S.WAIT.get('MINUTE')

    while not take_sample:
        time.sleep(wait)
        now, take_sample = (
            time_to_take_sample(sampletime, sampletime_unit, datetime.now())
        )
    return now


if __name__ == '__main__':
    pass
