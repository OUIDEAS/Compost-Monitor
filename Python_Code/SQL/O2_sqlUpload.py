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

header = ['Date/Time', 'O2 Concentration (%)']

startTime = time.time()
startup = True


mydb = mysql.connector.connect(
  host="100.114.38.109",
  user="root",
  password="pixhawk2",
  database="tutorial"
)

mycursor = mydb.cursor()
# Create a pandas DataFrame to hold the sensor data
data_frame = pd.DataFrame(columns=['SensID','Sensor','BuckID','ExpNum','DT','dateTime','O2_CON','Unit'])

startTime = time.time()

# Set up the MySQL connection using SQLAlchemy for pandas to_sql
engine = create_engine("mysql+mysqlconnector://root:pixhawk2@localhost/tutorial")  # Replace 'yourpassword' with your SQL root password

def is_valid_o2_concentration(value):
    """ Check if the value is a valid numeric O2 concentration. """
    if value != '*OK':
        return True
    else:
        return False


readCommand = 'R\r'.encode('utf-8')
loopTimer = 90

while True:
    O2Serial.reset_input_buffer()
    O2Serial.reset_output_buffer()
    O2Serial.write(readCommand)
    loopStartTime = time.time()
    time.sleep(1)
    
    O2_inbyte = O2Serial.read(size=1)
    print(f"O2 Sensor byte: {O2_inbyte}")
    
    while O2Serial.in_waiting:
        O2_inbyte = O2Serial.read(size=1)
        print(f"O2 Sensor byte: {O2_inbyte}")
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
            print('O2 CON:', O2_Con)

            if O2_Con != '*OK':
                # Prepare the data to add to the pandas DataFrame
                O2_DataDict = {
                    'SensID': [O2Port],
                    'Sensor': ['EZO_O2'],
                    'BuckID': [args.containernumber],
                    'ExpNum': [0],
                    'DT': [loopTimer],
                    'dateTime': [overallList[0]],
                    'O2_CON': [O2_Con],
                    'Unit': ['PPM']
                }
                dfn = pd.DataFrame(O2_DataDict)
                data_frame = pd.concat([data_frame, dfn], ignore_index=True)
                print(data_frame)
                data_frame.to_sql(name='O2', con=engine, if_exists='replace')
                print('O2 Data Uploaded to SQL Database!')
            else:
                print(f"Invalid O2 concentration data received: {O2_Con}")

           
            
            bytearray = []
            count += 1

    while (time.time() - loopStartTime) < loopTimer:
        time.sleep(0.1)
    
    if time.time() - startTime >= 3600:
        count = 0
        DataList = []
        overallList = [0, 0]
        startTime = time.time()
        logFileO2 = '{}/O2_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))
        csvO2 = '{}/O2_Bucket_{}_{}_{}.csv'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))
