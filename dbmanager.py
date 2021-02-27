import mysql.connector as mysql
import time
import datetime
import os


import random


def connect_database(credentials):
    
    host = credentials['host']
    port = credentials['port']
    database = credentials['database']
    user = credentials ['user']
    password = credentials['password']
    table_name = credentials['table_name']
    
    global connection
    connected = False
    print("The port is: %s" %port)
    try:
        connection = mysql.connect(user = user,
                                   password = password,
                                   host = host,
                                   database = database,
                                   port = port)
        connected = True

    except Exception as e:
        print(e)
        time.sleep(1)
        connected = False
        connection.close()
        
    return connection, connected

    
def write_into_database(connection, table, data):
    success = False
    cursor = connection.cursor()
    
    fields = '('
    values = '('
    
    for field, value in data.items():
        fields += ''+field+', '
        if isinstance(value, str):
            values += '"'+value+'", '
        else:
            values += str(value)+', '

    
    # number -2 is for the length of the comma and space <', '> at last
    # iteration from the for cicle above.
    fields = fields[:-2]+')'
    values = values[:-2]+')'
    
    sentence = ('INSERT INTO '+table+' '+fields+' VALUES '+values+';')

    print(sentence)    

    try:
        cursor.execute(sentence)
        connection.commit()
        success = True
    except Exception as e:
        success = False
        print(e)

    return success

    

if __name__ == '__main__':
    
    DATABASE = {
		"host": "",
		"port": ,
		"database": "",
		"user": "",
		"password": "",
		"table_name": "",
		"table_fields": ['date_estacion', 'muestra']
	}
    
    muestra = random.randint(0,10)*0.254
    date_time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
    mock_data = {
        'muestra': muestra,
        'date_estacion': date_time
    }
    
    print(mock_data)
    

    try: 
        connection, connected = connect_database(DATABASE)
        write_into_database(connection, DATABASE['table_name'], mock_data)
    except Exception as e:
        print(e)
    
    connection.close()

