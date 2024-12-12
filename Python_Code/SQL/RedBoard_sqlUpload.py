import email
from multiprocessing.reduction import sendfds
import time
import serial
import pathlib
import argparse
import datetime
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy import text
import smtplib
import sys, os

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--containernumber')
try:
    parser.add_argument('-c', '--comport')
    parser.add_argument('-f', '--filename')
    
    # parser.add_argument('-e', '--experimentnumber')
    args = parser.parse_args()


    RBport = ''.join(args.comport)
    baud_rate = 9600
    RBSerial = serial.Serial(RBport, baud_rate, timeout=1)
    directoryBase = "{}/{}/Bucket {}/RB".format(args.filename, time.strftime("%m-%d-%Y"), args.containernumber)
    pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
    logFileRB = '{}/RB_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"),
                                                    time.strftime("%H--%M--%S"))

    startup = True
    sent = False
    count = 0
    byteArray = []
    RB_DataList = []
    RB_DataDict = {}

    mydb = mysql.connector.connect(
    host="100.81.24.41",
    user="root",
    password="pixhawk2",
    database="CompostMonitor"
    )

    mycursor = mydb.cursor()
    # Create a pandas DataFrame to hold the sensor data
    data_frame = pd.DataFrame(columns=['SensID','Sensor','BuckID','ExpNum','DT','dateTime','TVOC_Con','TVOC_Unit','BME_Humidity','Hum_Unit','BME_Pressure','Press_Unit','BME_Temp','Temp_Unit'])

    startTime = time.time()

    # Set up the MySQL connection using SQLAlchemy for pandas to_sql
    engine = create_engine("mysql+mysqlconnector://root:pixhawk2@localhost/CompostMonitor")  # Replace 'yourpassword' with your SQL root password


    readCommand = 'R\r'.encode('utf-8')
    # loopTimer = 90


    humidity_values = {} #Store humidity

    while count < 1:
        # time.sleep(1)
        RB_inbyte = RBSerial.read(size=1)

        with open(logFileRB, 'ab') as l:
            l.write(RB_inbyte)
        byteArray.append(RB_inbyte)
        if RB_inbyte == b'\n':
            # Remove the newline character from the end of the array
            byteArray.pop()

            # Split the data array into a list
            RB_DataSplit = ''.join(str(byteArray)).replace(" ", "").replace('b', '').replace("'", '').replace(",", ''). \
                replace('[', '').replace(']', '').split(';')

            # Start the main list with a timestamp
            RB_DataList.append(datetime.datetime.now())

            # Add the strings from RB_DataSplit to the list
            for i in range(len(RB_DataSplit)):
                RB_DataList.append(RB_DataSplit[i])
            # print(RB_DataList)
            print(RB_DataList)
            # Make a dictionary of the data for PyMongo
            RB_DataDict = {
                'SensID': [RBport],
                'Sensor': ['RedBoard'],
                'BuckID': [args.containernumber],
                'ExpNum': [1],
                'DT': [120],
                'dateTime': [RB_DataList[0]], 
                'TVOC_Con': [RB_DataList[1]], 
                'TVOC_Unit': ['PTS'],
                'BME_Humidity': [RB_DataList[2]],
                'Hum_Unit': ['PCT'],
                'BME_Pressure': [RB_DataList[3]], 
                'Press_Unit': ['Pa'],
                'BME_Temp': [RB_DataList[4]], 
                'Temp_Unit': ['C']
            }
            count += 1
            dfn = pd.DataFrame(RB_DataDict)
            # data_frame = pd.concat([data_frame, dfn], ignore_index=True)
            dfn.to_sql(name = 'RedBoard', con=engine, if_exists='append')
            print(f'Redboard Data from Bucket {args.containernumber} Uploaded to SQL Database!', 'TVOC, Hum, P, T:', RB_DataList[1],RB_DataList[2], RB_DataList[3], RB_DataList[4])
            print(f'RedBoard in container {args.containernumber} good at time {time.strftime("%H:%M:%S")}')

            ## Reset the data list
            RB_DataList = []

            byteArray = []
            RBSerial.close()
            break
                
        # while (time.time() - loopStartTime) < loopTimer:
        #     time.sleep(0.1)

        # if time.time() - startTime >= 3600:
        #     count = 0
        #     RB_DataList = []
        #     startTime = time.time()
        #     logFileRB = '{}/RB_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber,
                                                                # time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))
except Exception as error:
    # print(error)
    # print(f'RedBoard Failure of Bin {args.containernumber}')
    # email_user = 'michaelvariny@outlook.com'
    # send_mail = '8478046268@txt.att.net'
    # server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    # server.starttls()
    # server.login(email_user, 'kcedyafdbqacqrqu')
    # message = f'RedBoard Failure of Bin {args.containernumber}'
    # server.sendmail(email_user, email_user, message)
    # server.quit()
    
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(error)
    email_user = 'ideascompostserver@gmail.com'
    send_mail = '8478046268@txt.att.net'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # server.login(email_user, 'kcedyafdbqacqrqu')
    server.login(email_user, 'ebtn zksf iqzu wipl')
    message = f'RedBoard Failure of Bin {args.containernumber} \n {error} at line {exc_tb.tb_lineno} at {datetime.datetime.now()}'
    server.sendmail(email_user, send_mail, message)
    server.quit()
    # print('too bad')