import time
import serial
import pathlib
import argparse
import datetime
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy import text

# Set up argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--comport')
parser.add_argument('-f', '--filename')
parser.add_argument('-n', '--containernumber')
# parser.add_argument('-e', '--experimentnumber')
args = parser.parse_args()

# Serial connection and file paths
CO2Port = ''.join(args.comport)
print('THE PORT IS THIS:', CO2Port)
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


mydb = mysql.connector.connect(
  host="100.114.38.109",
  user="root",
  password="pixhawk2",
  database="tutorial"
)

mycursor = mydb.cursor()
# Create a pandas DataFrame to hold the sensor data
data_frame = pd.DataFrame(columns=['SensID','Sensor','BuckID','ExpNum','DT','dateTime','CO2_CON','Unit'])

startTime = time.time()

# Set up the MySQL connection using SQLAlchemy for pandas to_sql
engine = create_engine("mysql+mysqlconnector://root:pixhawk2@localhost/tutorial")  # Replace 'yourpassword' with your SQL root password


readCommand = 'R\r'.encode('utf-8')
loopTimer = 90

while True:
    CO2Serial.reset_input_buffer()
    CO2Serial.reset_output_buffer()
    CO2Serial.write(readCommand)
    loopStartTime = time.time()
    time.sleep(1)
    
    CO2_inbyte = CO2Serial.read(size=1)
    # print(f"CO2 Sensor byte: {CO2_inbyte}")
    
    while CO2Serial.in_waiting:
        CO2_inbyte = CO2Serial.read(size=1)
        # print(f"CO2 Sensor byte: {CO2_inbyte}")
        with open(logFileCO2, 'ab') as l:
            l.write(CO2_inbyte)
        bytearray.append(CO2_inbyte)
        
        if CO2_inbyte == b'\r':
            bytearray.pop()
            DataList.append(
                ''.join(str(bytearray)).replace(" ", "").replace('b', '').replace("'", '').replace(",", '')
                .replace('[', '').replace(']', ''))
            overallList.append(datetime.datetime.now())
            overallList.append(str(''.join(DataList[count])))
            overallList.pop(0)
            overallList.pop(0)

            CO2_Con = overallList[1]
            # print(CO2_Con)

            # Validate if the CO2 concentration is a valid numeric value
            if CO2_Con != '*OK':
                # Prepare the data to add to the pandas DataFrame
                CO2_DataDict = {
                    'SensID': [CO2Port],
                    'Sensor': ['EZO_CO2'],
                    'BuckID': [args.containernumber],
                    'ExpNum': [0],
                    'DT': [loopTimer],
                    'dateTime': [overallList[0]],
                    'CO2_CON': [CO2_Con],
                    'Unit': ['PPM']
                }
                dfn = pd.DataFrame(CO2_DataDict)
                data_frame = pd.concat([data_frame, dfn], ignore_index=True)
                data_frame.to_sql(name='CO2', con=engine, if_exists='replace')
                print('CO2 Data Uploaded to SQL Database!', 'CO2_CON:', CO2_Con)
                print('CO2 in container {} good at time {}'.format(args.containernumber, time.strftime("%H:%M:%S")))


            else:
                print(f"Invalid CO2 concentration data received: {CO2_Con}")

            
            bytearray = []
            count += 1

    while (time.time() - loopStartTime) < loopTimer:
        time.sleep(0.1)
    
    if time.time() - startTime >= 3600:
        count = 0
        DataList = []
        overallList = [0, 0]
        startTime = time.time()
        logFileCO2 = '{}/CO2_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))
        csvCO2 = '{}/CO2_Bucket_{}_{}_{}.csv'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))
