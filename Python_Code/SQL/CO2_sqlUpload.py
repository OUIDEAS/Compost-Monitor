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
data_frame = pd.DataFrame(columns=['container_no','dateTime', 'CO2_CON'])

startTime = time.time()

# Set up the MySQL connection using SQLAlchemy for pandas to_sql
engine = create_engine("mysql+mysqlconnector://root:pixhawk2@localhost/tutorial")  # Replace 'yourpassword' with your SQL root password

def is_valid_co2_concentration(value):
    """ Check if the value is a valid numeric CO2 concentration. """
    try:
        # Try to convert the value to a float (or int)
        float(value)
        return True
    except ValueError:
        return False

def upload_to_sql(data):
    global data_frame
    
    # with engine.connect() as connection:
    #     connection.execute(text("DELETE FROM CO2;"))
    mycursor.execute("USE tutorial; delete from CO2;")
    # Append new data to the DataFrame
    new_data = pd.DataFrame([data])
    data_frame = pd.concat([data_frame, new_data], ignore_index=True)
    
    # Upload to SQL table 'table1'
    data_frame.to_sql('CO2', con=engine, if_exists='append', index=False)
    print(f"Data uploaded to SQL for Container {args.containernumber}")

readCommand = 'R\r'.encode('utf-8')
loopTimer = 90

while True:
    CO2Serial.reset_input_buffer()
    CO2Serial.reset_output_buffer()
    CO2Serial.write(readCommand)
    loopStartTime = time.time()
    time.sleep(1)
    
    CO2_inbyte = CO2Serial.read(size=1)
    print(f"CO2 Sensor byte: {CO2_inbyte}")
    
    while CO2Serial.in_waiting:
        CO2_inbyte = CO2Serial.read(size=1)
        print(f"CO2 Sensor byte: {CO2_inbyte}")
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

            # Validate if the CO2 concentration is a valid numeric value
            if is_valid_co2_concentration(CO2_Con):
                # Prepare the data to add to the pandas DataFrame
                CO2_DataDict = {
                    'container_no': args.containernumber,
                    'dateTime': overallList[0],
                    'CO2_CON': CO2_Con,
                }
                
                # Upload the new data to the SQL database using pandas
                upload_to_sql(CO2_DataDict)
            else:
                print(f"Invalid CO2 concentration data received: {CO2_Con}")

            # Prepare the data to add to the pandas DataFrame
            # CO2_DataDict = {
            #     'container_no': args.containernumber,
            #     'dateTime': overallList[0],
            #     'CO2_CON': overallList[1],
            # }
            
            # # Upload the new data to the SQL database using pandas
            # upload_to_sql(CO2_DataDict)
            
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
