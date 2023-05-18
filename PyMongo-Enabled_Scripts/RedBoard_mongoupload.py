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

client = MongoClient("mongodb://localhost:27017/")
db = client['CompostMonitor']
collection = db['{}'.format(args.collection)]

def upload_to_database(data):
    try:
        # Insert the data into the collection
        collection.insert_one(data)
        print('Container {} RedBoard saved to MongoDB!'.format(args.containernumber))
    except PyMongoError as e:
        print('Error saving container {} RedBoard to MongoDB \n'.format(args.containernumber), e)


port = ''.join(args.comport)
baud_rate = 9600
RBSerial = serial.Serial(port, baud_rate, timeout=1)
directoryBase = "{}/{}/Bucket {}/RB".format(args.filename, time.strftime("%m-%d-%Y"), args.containernumber)
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
logFileRB = '{}/RB_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"),
                                                   time.strftime("%H--%M--%S"))

startup = True

count = 0
byteArray = []
RB_DataList = []
RB_DataDict = {}

startTime = time.time()

p = multiprocessing.Process(target=upload_to_database, args=(RB_DataDict,))

while 1:
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

        # Make a dictionary of the data for PyMongo
        RB_DataDict = {'Date_Time': RB_DataList[0], 'TVOC_Con': RB_DataList[1], 'BME_Humidity': RB_DataList[2],
                       'BME_Pressure': RB_DataList[3], 'BME_Temp': RB_DataList[4], 'Sensor': 'RedBoard',
                       'Container_No': args.containernumber, 'Experiment_No': args.experimentnumber}
        print('RedBoard in container {} good at time {}'.format(args.containernumber, time.strftime("%H:%M:%S")))

        ## Reset the data list
        RB_DataList = []

        if __name__ == '__main__':
            if startup:
                p.start()
                startup = False
                print('Startup == False')

            else:
                # Close the process instance and start a new one!
                p.join()
                p.close()
                p = multiprocessing.Process(target= upload_to_database, args = (RB_DataDict,))
                p.start()

        byteArray = []
        count += 1

    if time.time() - startTime >= 3600:
        count = 0
        RB_DataList = []
        startTime = time.time()
        logFileRB = '{}/RB_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber,
                                                           time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))
