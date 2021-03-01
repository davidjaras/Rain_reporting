'''
sampling_time.py

File with functions that watch time to sampling pulses
'''

from datetime import datetime
import time


def time_to_take_sample(sampletime=5,
                        sampletime_unit='minutes',
                        now=datetime.now()):
    '''
    Depending of sampletime and its unit
    Return if it's time to take a sample.

    Default values in params are unchangeable by settings or user
    interactions.
    '''
    if sampletime <= 0 or sampletime > 59:
        # here may be a warning notice. Out of range
        sampletime = 5  # Five is a unchangeable default value

    if sampletime_unit.lower() == 'seconds':
        step_time = now.second
    elif sampletime_unit.lower() == 'minutes':
        step_time = now.minute
    else:
        # here may be a warning notice code
        step_time = now.minute

    if step_time % sampletime == 0:
        return now, True

    return now, False


def calibrate_minute():
    '''
    Sets the time step when it is on the minute scale to step every
    time the sencods are zero
    '''
    while True:
        now = datetime.now()
        if now.second == 0:
            break
        time.sleep(1)


def delay_to_take_sample(sampletime=5, sampletime_unit='minutes'):
    '''
    Sets the delay to validate if it is time to take a sample
    '''
    take_sample = False
    sampletime_unit = sampletime_unit.lower()

    if sampletime_unit not in ['seconds', 'minutes']:
        sampletime_unit = 'minutes'

    while not take_sample:
        if sampletime_unit == 'seconds':
            wait = 1
        if sampletime_unit == 'minutes':
            calibrate_minute()
            wait = 60

        time.sleep(wait)
        now, take_sample = (
            time_to_take_sample(sampletime, sampletime_unit)
        )
    return now


if __name__ == '__main__':
    pass
