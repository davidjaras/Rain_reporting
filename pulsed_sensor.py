'''

pulsed_sensor.py

Read GPIO port and count detected pulses, calculate a sample every
specified time and save in database mysql and in a local directory.

'''

import RPi.GPIO as GPIO
import time
import multiprocessing
import os
import settings
import json
from datetime import datetime
import sampling_time


def monitor_channel(channel, bouncetime, counter):
    '''
    Function used in a multiprocessing thread to count pulses
    detected in a specified GPIO port stablished in setting.json file
    '''
    last_edge = time.time()
    while True:
        if  GPIO.input(channel):
            current_edge = time.time()
            if current_edge - last_edge > bouncetime:
                counter.value += 1
                print('Counter pulses: %s' % counter.value)
            else:
                pass
            last_edge = current_edge
        time.sleep(bouncetime/10)


def get_sample(sampletime, scaletime, cf, is_new_data, counter, sample):

    while True:
        now = sampling_time.delay_to_take_sample(sampletime, scaletime)
        print("Time to measure: " + datetime.strftime(now,'%Y-%m-%d %H:%M:%S'))
        is_new_data.value = 1
        sample.value = counter.value*cf
        counter.value = 0


if __name__ == "__main__":
    
    # Open Settings in variable 'S'
    S = settings.read_json('settings.json')
    CONFIG = S['CONFIG']
    DATABASE = S['DATABASE']

    # Setup pin configuration
    pin_sensor = CONFIG['GPIO_PIN_SENSOR'] # select GPIO pin
    bouncetime_sensor = CONFIG['BOUNCETIME'] # avoid parasites pulses
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_sensor, GPIO.IN)
    
    # Setup global multiprocessing variables
    counter = multiprocessing.Value('d', 0.0)
    is_new_data = multiprocessing.Value('b', 0)
    sample = multiprocessing.Value('d', 0.0)
    
    # Process to monitor pulsed input
    monitor_ps = multiprocessing.Process(target = monitor_channel,
                                            args = (pin_sensor,
                                                    bouncetime_sensor,
                                                    counter))
    monitor_ps.start()
    
    # Process to scale pulses into physical variables    
    sample_ps = multiprocessing.Process(target = get_sample,
                                        args = (CONFIG['SAMPLETIME'],
                                                CONFIG['SAMPLETIME_UNIT'],
                                                CONFIG['CONVERION_FACTOR'],
                                                is_new_data,
                                                counter,
                                                sample))
    sample_ps.start()
