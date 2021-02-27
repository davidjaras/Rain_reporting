'''
sampling_time.py

File with functions that watch time to sampling pulses
'''

from datetime import datetime
import time


def time_to_take_sample(sampletime, sampletime_unit):
    '''
    Depending of sampletime and its unit
    Return if it's time to take a sample.
    '''
    now = datetime.now()
    
    if sampletime_unit == 'seconds':
        step_time = now.second
    if sampletime_unit.lower() == 'minutes':
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


def delay_to_take_sample(sampletime, sampletime_unit):
    '''
    Sets the delay to validate if it is time to take a sample
    '''
    take_sample = False
    sampletime_unit = sampletime_unit.lower()
    
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
    
