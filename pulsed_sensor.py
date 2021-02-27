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
import dbmanager
import csvwriting


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


def get_sample(CONFIG, is_new_data_to_send, is_new_data_to_save, counter, sample):
    
    sampletime = CONFIG['SAMPLETIME']
    scaletime = CONFIG['SAMPLETIME_UNIT']
    conversion_factor = CONFIG['CONVERSION_FACTOR']

    while True:
        now = sampling_time.delay_to_take_sample(sampletime, scaletime)
        print("Time to measure: " + datetime.strftime(now,'%Y-%m-%d %H:%M:%S'))
        is_new_data_to_send.value = 1
        is_new_data_to_save.value = 1
        sample.value = counter.value*conversion_factor
        counter.value = 0


def format_data(credentials, sample):
    date_time = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
    data = {
        credentials['table_field_datetime'] : date_time,
        credentials['table_field_sample'] : sample.value
    }
    return data
    

def send_to_database(credentials, is_new_data_to_send, sample):
    while True:
        time.sleep(0.1)
        try:
            if is_new_data_to_send.value:
                is_new_data_to_send.value = 0
                data = format_data(credentials, sample)
                print('Starting connection to database...')
                connection, connected = dbmanager.connect_database(
                                                        credentials
                                                        )
                print('Connection to database successful.')
                print(data)
                success = dbmanager.write_into_database(
                                            connection,
                                            credentials['table_name'],
                                            data        
                                            )
                print('Insert operation was successful.')
                connection.close()
                
        except Exception as e:
            print('Insert operation into database was not performed'
                  ' due to this exception was thrown:')
            print(e)


def save_in_local_storage(table_name, is_new_data_to_save, sample):
    while True:
        time.sleep(0.1)
        try:
            if is_new_data_to_save.value:
                is_new_data_to_save.value = 0
                today_date = datetime.strftime(datetime.now(),'%Y-%m-%d')
                today_time = datetime.strftime(datetime.now(),'%H:%M:%S')
                today = today_date + ' ' + today_time
                filename = table_name+'_'+today_date+'.csv'
                
                if not csvwriting.verifyDuplications('/home/pi/datalogger/'+filename,[today, sample.value]):
                    csvwriting.writeFile('/home/pi/datalogger/'+filename, ['Date_Time','muestra'], [today, sample.value])
                
        except Exception as e:
            print('File was not written because this exception was thrown:')
            print(e)


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
    is_new_data_to_send = multiprocessing.Value('b', 0)
    is_new_data_to_save = multiprocessing.Value('b', 0)
    sample = multiprocessing.Value('d', 0.0)
    
    # Process to monitor pulsed input
    monitor_ps = multiprocessing.Process(target = monitor_channel,
                                            args = (pin_sensor,
                                                    bouncetime_sensor,
                                                    counter))
    monitor_ps.start()
    
    # Process that manage time and take a sample from counter
    sample_ps = multiprocessing.Process(target = get_sample,
                                        args = (CONFIG,
                                                is_new_data_to_send,
                                                is_new_data_to_save,
                                                counter,
                                                sample))
    sample_ps.start()
    
    # Processes to write into database
    database_ps = multiprocessing.Process(target = send_to_database,
                                      args = (DATABASE,
                                              is_new_data_to_send,
                                              sample))
    database_ps.start()
    
    # Process to write into file. Local Storage
    save_local_ps = multiprocessing.Process(target = save_in_local_storage,
                                 args = (
                                 DATABASE['table_name'],
                                 is_new_data_to_save,
                                 sample))

    save_local_ps.start()
