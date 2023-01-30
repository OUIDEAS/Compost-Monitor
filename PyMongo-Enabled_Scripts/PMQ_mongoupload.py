import time
import serial
import pathlib
import argparse
import multiprocessing
from pymongo import MongoClient

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--comport')
parser.add_argument('-f', '--filename')
parser.add_argument('-n', '--containernumber')
args = parser.parse_args()

port = ''.join(args.comport)
baud_rate = 9600
PMQSerial = serial.Serial(port, baud_rate, timeout=1)
directoryBase = "{}/{}/Bucket {}/PMQ".format(args.filename, time.strftime("%m-%d-%Y"), args.containernumber)
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
logFilePMQ= '{}/PMQ_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))

count = 0
bytearray = []
PMQ_DataList = []
PMQ_DataDict = {}

client = MongoClient("mongodb+srv://ouideas:<password>@compostmonitor-1.o0tbgvg.mongodb.net/?retryWrites=true&w=majority")
db = client['CompostMonitor-{}'.format(args.containernumber)]

def upload_to_database(data):
    try:
        # Connect to the collection where the data will be stored
        collection = db.PMQ

        # Insert the data into the collection
        print(data)
        collection.insert_one(data)
    except:
        print('Error uploading to MongoDB')

p = multiprocessing.Process(target=upload_to_database, args=(PMQ_DataDict,))

startTime = time.time()
startup = True
while 1:
    PMQ_inbyte = PMQSerial.read(size=1)
    with open(logFilePMQ, 'ab') as l:
        l.write(PMQ_inbyte)
    bytearray.append(PMQ_inbyte)
    if PMQ_inbyte == b'\n':
        #split it up
        bytearray.pop()
        PMQ_DataSplit = ''.join(str(bytearray)).replace(" ", "").replace('b', '').replace("'", '').replace(",",'')\
            .replace('[', '').replace(']', '').split(';')
        PMQ_DataList.append(time.strftime("%m-%d-%Y %H:%M:%S"))
        for i in range(len(PMQ_DataSplit)):
            PMQ_DataList.append(PMQ_DataSplit[i])
        print(PMQ_DataList)
        PMQ_DataDict = {'Date_Time': PMQ_DataList[0], 'TVOC Con': PMQ_DataList[1], 'BME Humidity': PMQ_DataList[2],
                       'BME Pressure': PMQ_DataList[3], 'BME Temp': PMQ_DataList[4]}
        if __name__ == '__main__':
            if startup:
                p.start()
                startup= False
                print('startup == false')
            else:
                p.close()
                p = multiprocessing.Process(target = upload_to_database, args = (PMQ_DataDict,))
                p.start()
        PMQ_DataList = []
        bytearray = []
        count += 1
    if time.time() - startTime >= 3600:
        count = 0
        PMQ_DataList = []
        startTime = time.time()
        logFilePMQ = '{}/PMQ_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber,
                                                              time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))