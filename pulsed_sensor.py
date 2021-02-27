'''

pulsed_sensor.py

Read GPIO port and count detected pulses, calculate a sample every
specified time and save in database mysql and in a local directory.

'''

# Python Core Libraries
import RPi.GPIO as GPIO
import time
import multiprocessing
import os
import settings
import json
from datetime import datetime

# Project modules
import sampling_time
import dbmanager
import csvwriting


def get_now_time():
    ''' Return actual time in string format. '''
    now = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
    return now


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


def get_sample(CONFIG, is_new_data_send, is_new_data_save, counter, sample):
    '''
    Function that according the params in CONFIG check time
    to take sample and enables the flags is_new_data
    to indicate the other processes that can read sample and go on.
    '''
    sampletime = CONFIG['SAMPLETIME']
    scaletime = CONFIG['SAMPLETIME_UNIT']
    conversion_factor = CONFIG['CONVERSION_FACTOR']

    while True:
        now = sampling_time.delay_to_take_sample(sampletime, scaletime)
        print("Time to measure: " + datetime.strftime(now,'%Y-%m-%d %H:%M:%S'))
        is_new_data_send.value = 1
        is_new_data_save.value = 1
        sample.value = counter.value*conversion_factor
        counter.value = 0


def format_data(credentials, sample):
    '''
    Create a data dictionary with keys called like columns in 
    database according to setup
    '''
    date_time = get_now_time()
    data = {
        credentials['table_field_datetime'] : date_time,
        credentials['table_field_sample'] : sample.value
    }
    return data
    

def send_to_database(credentials, is_new_data_send, sample):
    '''
    Function checks if flag to send measure a database is active, 
    set connection and make insert of the data
    '''
    while True:
        time.sleep(0.1)
        try:
            if is_new_data_send.value:
                is_new_data_send.value = 0
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


def save_in_local_storage(path, table_name, is_new_data_save, sample):
    '''
    Function checks if flag to save measure in local csv files is 
    active, validate duplicates entries and save data
    '''
    while True:
        time.sleep(0.1)
        try:
            if is_new_data_save.value:
                is_new_data_save.value = 0
                
                today = get_now_time()
                today_date = today.split(' ')[0]
                filename = table_name+'_'+today_date+'.csv'
                path_filename = path+filename
                
                duplicates = csvwriting.verify_duplications(
                                    path_filename,
                                    [today, sample.value]
                                    )
                
                if not duplicates:
                    csvwriting.write_file(
                                path_filename,
                                ['Date_Time','muestra'],
                                [today, sample.value]
                                )
                
        except Exception as e:
            print('File was not written because this exception was thrown:')
            print(e)


if __name__ == "__main__":
    
    # Open Settings in variable 'S'. Set CONFIG and DATABASE variables
    S = settings.read_json('settings.json')
    CONFIG = S['CONFIG']
    DATABASE = S['DATABASE']
    PATH = S['LOCAL_STORAGE_PATH']

    # Setup pin configuration
    pin_sensor = CONFIG['GPIO_PIN_SENSOR'] # select GPIO pin
    bouncetime_sensor = CONFIG['BOUNCETIME'] # avoid parasites pulses
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_sensor, GPIO.IN)
    
    # Setup global multiprocessing variables
    counter = multiprocessing.Value('d', 0.0) # pulses counter
    is_new_data_send = multiprocessing.Value('b', 0) # db flag
    is_new_data_save = multiprocessing.Value('b', 0) # csv flag
    sample = multiprocessing.Value('d', 0.0) # phisical measure
    
    # Process to monitor pulsed input
    monitor_ps = multiprocessing.Process(target = monitor_channel,
                                            args = (pin_sensor,
                                                    bouncetime_sensor,
                                                    counter))
    monitor_ps.start()
    
    # Process that manage time and take a sample from counter
    sample_ps = multiprocessing.Process(target = get_sample,
                                        args = (CONFIG,
                                                is_new_data_send,
                                                is_new_data_save,
                                                counter,
                                                sample))
    sample_ps.start()
    
    # Processes to write into database
    database_ps = multiprocessing.Process(target = send_to_database,
                                      args = (DATABASE,
                                              is_new_data_send,
                                              sample))
    database_ps.start()
    
    # Process to write into file. Local Storage
    save_local_ps = multiprocessing.Process(target = save_in_local_storage,
                                 args = (
                                 PATH,
                                 DATABASE['table_name'],
                                 is_new_data_save,
                                 sample))

    save_local_ps.start()
