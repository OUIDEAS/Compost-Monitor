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

client = MongoClient("mongodb+srv://user:pwd@compostmonitor-1.o0tbgvg.mongodb.net/?retryWrites=true&w=majority")
db = client['CompostMonitor']


def upload_to_database(data):
    try:
        # Connect to the collection where the data will be stored
        collection = db['Overall']

        # Insert the data into the collection
        collection.insert_one(data)
    except:
        print('Error uploading to MongoDB')


port = ''.join(args.comport)
baud_rate = 9600
RBSerial = serial.Serial(port, baud_rate, timeout=1)
directoryBase = "{}/{}/Bucket {}/RB".format(args.filename, time.strftime("%m-%d-%Y"), args.containernumber)
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
logFileRB = '{}/RB_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"),
                                                   time.strftime("%H;%M;%S"))

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
        RB_DataDict = {'Date_Time': RB_DataList[0], 'TVOC Con': RB_DataList[1], 'BME Humidity': RB_DataList[2],
                       'BME Pressure': RB_DataList[3], 'BME Temp': RB_DataList[4], 'Sensor': 'RedBoard',
                       'Container No': args.containernumber, 'Experiment No': 0}
        print(RB_DataDict)

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
                                                           time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
