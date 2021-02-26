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
import datetime


def monitorchannel(channel, bouncetime, counter):
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


if __name__ == "__main__":
    
    # Open Settings in variable 'S'
    S = settings.read_json('settings.json')
    CONFIG = S['CONFIG']
    DATABASE = S['DATABASE']

    # Setup pin configuration
    pin_sensor = CONFIG['GPIO_PIN_SENSOR'] # select GPIO pin
    bouncetime_sensor = CONFIG['BOUNCETIME'] # avoid parasites pulses
    resolution = CONFIG['RESOLUTION_PER_PULSE'] # physical pulse unit
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_sensor, GPIO.IN)
    
    print('Pin sensor: ')
    print(pin_sensor)
    print('bouncetime_sensor: ')
    print(bouncetime_sensor)
    
    counter = multiprocessing.Value('d', 0.0)
    #values = multiprocessing.Array('d',[0]*2)
    #newdata = multiprocessing.Array('i',[0]*4)
    
    # Process to monitor pulsed input
    monitor_process = multiprocessing.Process(target = monitorchannel,
                                            args = (pin_sensor,
                                                    bouncetime_sensor,
                                                    counter))
    monitor_process.start()
