import time
import serial
import pathlib
import argparse
import multiprocessing
from pymongo import MongoClient
import datetime


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--comport')
parser.add_argument('-f', '--filename')
parser.add_argument('-n', '--containernumber')
args = parser.parse_args()

CO2Port = ''.join(args.comport)
baud_rate = 9600
CO2Serial = serial.Serial(CO2Port, baud_rate, timeout=1)
directoryBase = "{}/{}/Bucket {}/CO2".format(args.filename, time.strftime("%m-%d-%Y"), args.containernumber)
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
logFileCO2  = '{}/CO2_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
csvCO2 = '{}/CO2_Bucket_{}_{}_{}.csv'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))

count = 0
bytearray = []
DataList = []
overallList = [0,0]
CO2_DataDict = {}

header = [ 'Date/Time', 'CO2 Concentration (ppm)']

startTime = time.time()
startup = True

client = MongoClient("mongodb+srv://ouideas:<password>@compostmonitor-1.o0tbgvg.mongodb.net/?retryWrites=true&w=majority")
db = client['CompostMonitor-{}'.format(args.containernumber)]

def upload_to_database(data):
    try:
        # Connect to the collection where the data will be stored
        collection = db['Carbon Dioxide']

        # Insert the data into the collection
        print(data)
        collection.insert_one(data)
    except:
        print('Error uploading to MongoDB')

p = multiprocessing.Process(target=upload_to_database, args=(CO2_DataDict,))

while 1:
    CO2_inbyte = CO2Serial.read(size=1)
    with open(logFileCO2, 'ab') as l:
        l.write(CO2_inbyte)
    # print(CO2_inbyte)
    bytearray.append(CO2_inbyte)
    if CO2_inbyte == b'\r':
        #split it up
        bytearray.pop()
        DataList.append(
            ''.join(str(bytearray)).replace(" ", "").replace('b', '').replace("'", '').replace(",", '')
            .replace('[','').replace(']', ''))
        overallList.append(datetime.datetime.now())
        overallList.append(str(''.join(DataList[count])))
        overallList.pop(0)
        overallList.pop(0)
        print(overallList)
        CO2_DataDict = {'Date_Time': overallList[0], 'CO2 Con': overallList[1]}
        if __name__ == '__main__':
            if startup:
                p.start()
                startup= False
                print('startup == false')
            else:
                p.close()
                p = multiprocessing.Process(target = upload_to_database, args = (CO2_DataDict,))
                p.start()
        bytearray = []
        count += 1
    if time.time() - startTime >= 3600:
        count = 0
        DataList = []
        overallList = [0,0]
        startTime = time.time()
        logFileCO2 = '{}/CO2_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber,
                                                              time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
        csvCO2 = '{}/CO2_Bucket_{}_{}_{}.csv'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"),
                                                      time.strftime("%H;%M;%S"))