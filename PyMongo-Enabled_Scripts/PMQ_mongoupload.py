import time
import serial
import pathlib
import argparse
import multiprocessing
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--comport')
parser.add_argument('-f', '--filename')
parser.add_argument('-n', '--containernumber')
parser.add_argument('-cn', '--collection')
parser.add_argument('-e', '--experimentnumber')
args = parser.parse_args()



# args.comport = '/dev/ttyACM0'
# args.filename = '/home/dan/TestData'
# args.containernumber = 2
port = ''.join(args.comport)
baud_rate = 9600
PMQSerial = serial.Serial(port, baud_rate, timeout=1)
directoryBase = "{}/{}/Bucket {}/PMQ".format(args.filename, time.strftime("%m-%d-%Y"), args.containernumber)
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
logFilePMQ= '{}/PMQ_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))

fileCount = 1
count = 0
bytearray = []
PMQ_DataList = []
PMQ_DataDict = {}

client = MongoClient("mongodb://localhost:27017/")
db = client['CompostMonitor']
collection = db['{}'.format(args.collection)]

def upload_to_database(data):
    try:
        # Insert the data into the collection
        collection.insert_one(data)
        print('Container {} PMQ saved to MongoDB!'.format(args.containernumber))
    except PyMongoError as e:
        print('Error saving container {} PMQ to MongoDB \n'.format(args.containernumber), e)

p = multiprocessing.Process(target=upload_to_database, args=(PMQ_DataDict,))

startTime = time.time()
startup = True

PMQSerial.reset_input_buffer()
while 1:
    PMQ_inbyte = PMQSerial.read(size=1)
    with open(logFilePMQ, 'ab') as l:
        l.write(PMQ_inbyte)
    bytearray.append(PMQ_inbyte)

    if (fileCount ==1 and count >= 1 and PMQ_inbyte == b'\n'):
        print(bytearray)
        bytearray.pop()
        PMQ_DataSplit = ''.join(str(bytearray)).replace(" ", "").replace('b', '').replace("'", '').replace(",",'')\
            .replace('[', '').replace(']', '').split(';')
        PMQ_DataList.append(datetime.datetime.now())
        for i in range(len(PMQ_DataSplit)):
            PMQ_DataList.append(PMQ_DataSplit[i])
        print(PMQ_DataList)
        PMQ_DataDict = {'Date_Time': PMQ_DataList[0], 'TVOC Con': PMQ_DataList[1], 'BME Humidity': PMQ_DataList[2],
                        'BME Pressure': PMQ_DataList[3], 'BME Temp': PMQ_DataList[4], 'Sensor': 'PMQ',
                        'Container No': args.containernumber, 'Experiment No': args.experimentnumber}
        print('PMQ in container {} good at time {}'.format(args.containernumber, time.strftime("%H:%M:%S")))
        if startup:
            p.start()
            startup= False
            print('startup == false')
        else:
            p.join()
            p.close()
            p = multiprocessing.Process(target = upload_to_database, args = (PMQ_DataDict,))
            p.start()
        PMQ_DataList = []
        bytearray = []
        count += 1

    if (fileCount >= 2 and PMQ_inbyte == b'\n'):
        print(bytearray)
    # if PMQ_inbyte == b'\n':
        #split it up
        bytearray.pop()
        PMQ_DataSplit = ''.join(str(bytearray)).replace(" ", "").replace('b', '').replace("'", '').replace(",",'')\
            .replace('[', '').replace(']', '').split(';')
        PMQ_DataList.append(datetime.datetime.now())
        for i in range(len(PMQ_DataSplit)):
            PMQ_DataList.append(PMQ_DataSplit[i])
        print(PMQ_DataList)
        PMQ_DataDict = {'Date_Time': PMQ_DataList[0], 'TVOC Con': PMQ_DataList[1], 'BME Humidity': PMQ_DataList[2],
                       'BME Pressure': PMQ_DataList[3], 'BME Temp': PMQ_DataList[4]}
        if startup:
            p.start()
            startup= False
            print('startup == false')
        else:
            p.join()
            p.close()
            p = multiprocessing.Process(target = upload_to_database, args = (PMQ_DataDict,))
            p.start()
        PMQ_DataList = []
        bytearray = []
        count += 1

    if (fileCount == 1 and count == 0 and PMQ_inbyte == b'\n'):
        print(bytearray)
        count += 1
    if time.time() - startTime >= 3600:
        count = 0
        PMQ_DataList = []
        startTime = time.time()
        logFilePMQ = '{}/PMQ_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber,
                                                              time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
        fileCount += 1
