import time
import serial
import pathlib
import argparse
import datetime
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, null
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
    O2Port = ''.join(args.comport)
    baud_rate = 9600
    O2Serial = serial.Serial(O2Port, baud_rate, timeout=1)
    directoryBase = "{}/{}/Bucket {}/O2".format(args.filename, time.strftime("%m-%d-%Y"), args.containernumber)
    pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
    logFileO2 = '{}/O2_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))

    count = 0
    bytearray = []
    DataList = []
    overallList = [0,0]
    O2_DataDict = {}

    sent = False
    mydb = mysql.connector.connect(
    host="100.81.24.41",
    user="root",
    password="pixhawk2",
    database="CompostMonitor"
    )

    mycursor = mydb.cursor()
    # Create a pandas DataFrame to hold the sensor data
    data_frame = pd.DataFrame(columns=['SensID','Sensor','BuckID','ExpNum','DT','dateTime','O2_CON','Unit'])

    startTime = time.time()

    # Set up the MySQL connection using SQLAlchemy for pandas to_sql
    engine = create_engine("mysql+mysqlconnector://root:pixhawk2@localhost/CompostMonitor")  # Replace 'yourpassword' with your SQL root password



    readCommand = 'R\r'.encode('utf-8')
    noOK = '*OK,0\r'.encode('utf-8')
    # loopTimer = 90
    while count < 1:
        O2Serial.write(noOK)
        O2Serial.flush()

        O2Serial.reset_input_buffer()
        O2Serial.reset_output_buffer()
        O2Serial.write(readCommand)
        O2Serial.flush()
        # loopStartTime = time.time()
        # time.sleep(1)
        
        # O2_inbyte = O2Serial.read(size=1)
        # print(f"O2 Sensor byte: {O2_inbyte}")
        
        while O2Serial.in_waiting:
            O2_inbyte = O2Serial.read(size=1)
            # print(f"O2 Sensor byte: {O2_inbyte}")
            with open(logFileO2, 'ab') as l:
                l.write(O2_inbyte)
            bytearray.append(O2_inbyte)
            
            if O2_inbyte == b'\r':
                bytearray.pop()
                DataList.append(
                    ''.join(str(bytearray)).replace(" ", "").replace('b', '').replace("'", '').replace(",", '')
                    .replace('[', '').replace(']', ''))
                overallList.append(datetime.datetime.now())
                overallList.append(str(''.join(DataList[count])))
                overallList.pop(0)
                overallList.pop(0)

                O2_Con = overallList[1]
                # print('O2 CON:', O2_Con)

                if '*' not in O2_Con and O2_Con is not null:
                    # Prepare the data to add to the pandas DataFrame
                    O2_DataDict = {
                        'SensID': [O2Port],
                        'Sensor': ['EZO_O2'],
                        'BuckID': [args.containernumber],
                        'ExpNum': [1],
                        'DT': [120],
                        'dateTime': [overallList[0]],
                        'O2_CON': [O2_Con],
                        'Unit': ['PPT']
                    }
                    count += 1

                    # sent = True
                    dfn = pd.DataFrame(O2_DataDict)
                    # data_frame = pd.concat([data_frame, dfn], ignore_index=True)
                    dfn.to_sql(name='O2', con=engine, if_exists='append')
                    print(f'O2 Data from Bucket {args.containernumber} Uploaded to SQL Database!', 'O2 CON:', O2_Con)
                    print(f'O2 in container {args.containernumber} good at time {time.strftime("%H:%M:%S")}')

                else:
                    print(f"Invalid O2 concentration data from Bucket {args.containernumber} received: {O2_Con}")


            
                dfn.iloc[0:0]
                bytearray = []
                mydb.close()
                mycursor.close()
                O2Serial.close()
                break

    # while (time.time() - loopStartTime) < loopTimer:
    #     time.sleep(0.1)
    
    # if time.time() - startTime >= 3600:
    #     count = 0
    #     DataList = []
    #     overallList = [0, 0]
    #     startTime = time.time()
    #     logFileO2 = '{}/O2_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))
    #     csvO2 = '{}/O2_Bucket_{}_{}_{}.csv'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))
except Exception as error:
    # print(error)
    # print(f'O2 Failure of Bin {args.containernumber}')
    # email_user = 'michaelvariny@outlook.com'
    # send_mail = '8478046268@txt.att.net'
    # server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    # server.starttls()
    # # server.login(email_user, 'kcedyafdbqacqrqu')
    # message = f'O2 Failure of Bin {args.containernumber}'
    # server.sendmail(email_user, email_user, message)
    # server.quit()
    
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    email_user = 'ideascompostserver@gmail.com'
    send_mail = '8478046268@txt.att.net'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # print(server)
    server.starttls()
    # server.login(email_user, 'kcedyafdbqacqrqu')
    server.login(email_user, 'ebtn zksf iqzu wipl')
    message = f'O2 Failure of Bin {args.containernumber} \n {error} at line {exc_tb.tb_lineno}at {datetime.datetime.now()}'
    server.sendmail(email_user, send_mail, message)
    server.quit()
    # print('too bad')