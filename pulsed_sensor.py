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


def send_to_database(database_credentials, is_new_data, sample):
    while True:
        time.sleep(0.1)
        if is_new_data.value:
            is_new_data.value = 0
            print("Starting process to send a database MySQL")
        


def write_database(values,index,newdata,credentials):
    
    host = credentials['host']
    database = credentials['database']
    user = credentials ['user']
    password = credentials['password']
    table_name = credentials['table_name']
    
    table = ['rain', 'wind']
    while True:
        time.sleep(0.001)
        try:
            if newdata[index] == 1:
                newdata[index]=0

                today = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')
                now = datetime.datetime.strftime(datetime.datetime.now(),'%H:%M:%S')

                print('Starting connection to database...')
                connection, connected = dbmanager.connect_database(user, password,
                                                         host, database,3307)
                print('Connection to database successful.')
        
##         
                success = dbmanager.write_from_csv(connection,
                                                   '/home/pi/datalogger/backup_'+table[index]+'.csv',
                                                   table_name+'_'+table[index])
                print('Writing backup file...' + str(success))

##                if not dbmanager.check_duplicates(connection, table_name+'_'+table[index],[today, now, values[index]]):
                    
                success = dbmanager.write_into_database(connection, table_name+'_'+table[index],
                                                        [today, now, values[index]])
                print('Insert operation was successful.')
##                else:
##                    print('The row has been written already in the database')
##                    success = True
                connection.close()
        except Exception as e:
            logging.exception(e)
            print('Insert operation into database was not performed'
                  ' due to this exception was thrown:')
            print(e)
            print('Backup file: /home/pi/datalogger/backup_'+table[index]+'.csv')
            if not csvwriting.verifyDuplications('/home/pi/datalogger/backup_'+table[index]+'.csv', [today,now, values[index]]):
                try:
                    csvwriting.writeFile('/home/pi/datalogger/backup_'+table[index]+'.csv',
                                         ['Date','Time',table[index]], [today, now, values[index]])
                    print('New data was registered in backup file. When connection'
                          'to database is restarted, data will be written from csv.')
                except Exception as e:
                    print(e)
                
            else:
                print('Data is already registered in backup file. No new rows were registered.')


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
    
    # Process that manage time and take a sample from counter
    sample_ps = multiprocessing.Process(target = get_sample,
                                        args = (CONFIG['SAMPLETIME'],
                                                CONFIG['SAMPLETIME_UNIT'],
                                                CONFIG['CONVERION_FACTOR'],
                                                is_new_data,
                                                counter,
                                                sample))
    sample_ps.start()
    
    # Processes to write into database
    send_ps = multiprocessing.Process(target = send_to_database,
                                      args = (DATABASE,
                                              is_new_data,
                                              sample))
    send_ps.start()
