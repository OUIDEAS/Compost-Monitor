import time
from unittest.mock import sentinel
import serial
import pathlib
import argparse
import datetime
import pandas as pd
import mysql.connector
from sqlalchemy import Null, create_engine, over
from sqlalchemy import text
import smtplib
import sys, os


    # Set up argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--containernumber')
try:
    parser.add_argument('-c', '--comport')
    parser.add_argument('-f', '--filename')
    
    # parser.add_argument('-e', '--experimentnumber')
    args = parser.parse_args()

    # Serial connection and file paths
    CO2Port = ''.join(args.comport)
    # print('THE PORT IS THIS:', CO2Port)
    baud_rate = 9600
    CO2Serial = serial.Serial(CO2Port, baud_rate, timeout=90)
    directoryBase = "{}/{}/Bucket {}/CO2".format(args.filename, time.strftime("%m-%d-%Y"), args.containernumber)
    pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
    logFileCO2 = '{}/CO2_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))
    csvCO2 = '{}/CO2_Bucket_{}_{}_{}.csv'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))

    count = 0
    bytearray = []
    DataList = []
    overallList = [0, 0]
    CO2_DataDict = {}

    sent = False
    mydb = mysql.connector.connect(
    host="100.81.24.41",
    user="root",
    password="pixhawk2",
    database="CompostMonitor"
    )

    mycursor = mydb.cursor()
    # Create a pandas DataFrame to hold the sensor data
    data_frame = pd.DataFrame(columns=['SensID','Sensor','BuckID','ExpNum','DT','dateTime','CO2_CON','Unit'])

    startTime = time.time()

    # Set up the MySQL connection using SQLAlchemy for pandas to_sql
    engine = create_engine("mysql+mysqlconnector://root:pixhawk2@localhost/CompostMonitor")  # Replace 'yourpassword' with your SQL root password


    readCommand = 'R\r'.encode('utf-8')
    # noOK = '*OK,0\r'.encode('utf-8')
    # loopTimer = 90
    # rebootCommand = '*REBOOT\r'.encode('utf-8')  # Reboot command
    # CO2Serial.write(rebootCommand)

    while count < 1:
        # CO2Serial.write(noOK)
        # CO2Serial.flush()
        # print("Disable *OK Response:", response)

        # Send the read command
        # CO2Serial.reset_input_buffer()
        # CO2Serial.write(readCommand)
        # CO2Serial.flush()
        CO2Serial.reset_input_buffer()
        CO2Serial.reset_output_buffer()
        CO2Serial.write(readCommand)
        CO2Serial.flush()
            # loopStartTime = time.time()
            # time.sleep(1)
            
            # CO2_inbyte = CO2Serial.read(size=1)
            # print(f"CO2 Sensor byte: {CO2_inbyte}")
            
        while CO2Serial.in_waiting:
            # response = CO2Serial.readline().decode('utf-8').strip()
            # print(f"Raw Response: {response}")

            CO2_inbyte = CO2Serial.read(size=1)
            # print(f"CO2 Sensor byte: {CO2_inbyte}")
            with open(logFileCO2, 'ab') as l:
                l.write(CO2_inbyte)
            bytearray.append(CO2_inbyte)
            print(bytearray)
            if CO2_inbyte == b'\r':
                bytearray.pop()
                DataList.append(
                    ''.join(str(bytearray)).replace(" ", "").replace('b', '').replace("'", '').replace(",", '')
                    .replace('[', '').replace(']', ''))
                overallList.append(datetime.datetime.now())
                overallList.append(str(''.join(DataList[count])))
                # print(overallList)
                # print(overallList)
                overallList.pop(0)
                overallList.pop(0)

                CO2_Con = overallList[1]
                # if args.containernumber == 4:
                #     CO2_Con = CO2_Con*-1
                # print(CO2_Con)
                # print(CO2_Con)
                # Validate if the CO2 concentration is a valid numeric value
                if ('*' or 'U' or '\'' or 'K') not in CO2_Con and CO2_Con is not Null and count < 1 and CO2_Con != '':
                    # Prepare the data to add to the pandas DataFrame
                    CO2_DataDict = {
                        'SensID': [CO2Port],
                        'Sensor': ['EZO_CO2'],
                        'BuckID': [args.containernumber],
                        'ExpNum': [0],
                        'DT': [60],
                        'dateTime': [overallList[0]],
                        'CO2_CON': [CO2_Con],
                        'Unit': ['PPM']
                    }
                    count += 1
                    dfn = pd.DataFrame(CO2_DataDict)
                    # data_frame = pd.concat([data_frame, dfn], ignore_index=True)
                    dfn.to_sql(name='CO2', con=engine, if_exists='append')
                    print(f'CO2 Data from Bucket {args.containernumber} Uploaded to SQL Database!', 'CO2_CON:', CO2_Con)
                    print(f'CO2 in container {args.containernumber} good at time {time.strftime("%H:%M:%S")}')


                else:
                    print(f"Invalid CO2 concentration data from Bucket {args.containernumber} received: {CO2_Con}")

                
                bytearray = []
                CO2Serial.close()

        # while (time.time() - loopStartTime) < loopTimer:
        #     time.sleep(0.1)
    
    # if time.time() - startTime >= 3600:
    #     count = 0
    #     DataList = []
    #     overallList = [0, 0]
    #     startTime = time.time()
    #     logFileCO2 = '{}/CO2_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))
    #     csvCO2 = '{}/CO2_Bucket_{}_{}_{}.csv'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))
except Exception as error:
    # print(f'CO2 Failure of Bin {args.containernumber}')
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    email_user = 'ideascompostserver@gmail.com'
    send_mail = '8478046268@txt.att.net'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # server.login(email_user, 'kcedyafdbqacqrqu')
    server.login(email_user, 'ebtn zksf iqzu wipl')
    message = f'CO2 Failure of Bin {args.containernumber} \n {error} at line {exc_tb.tb_lineno}'
    server.sendmail(email_user, send_mail, message)
    server.quit()