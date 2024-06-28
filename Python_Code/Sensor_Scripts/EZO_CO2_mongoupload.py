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

CO2Port = ''.join(args.comport)
baud_rate = 9600
CO2Serial = serial.Serial(CO2Port, baud_rate, timeout=90)
directoryBase = "{}/{}/Bucket {}/CO2".format(args.filename, time.strftime("%m-%d-%Y"), args.containernumber)
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
logFileCO2  = '{}/CO2_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))
csvCO2 = '{}/CO2_Bucket_{}_{}_{}.csv'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))

count = 0
bytearray = []
DataList = []
overallList = [0,0]
CO2_DataDict = {}

header = ['Date/Time', 'CO2 Concentration (ppm)']

startTime = time.time()
startup = True

client = MongoClient("mongodb://localhost:27017/")
db = client['CompostMonitor']
collection = db['{}'.format(args.collection)]

def upload_to_database(data):
    try:
        # Insert the data into the collection
        collection.insert_one(data)
        print('Container {} CO2 saved to MongoDB!'.format(args.containernumber))
    except PyMongoError as e:
        print('Error saving container {} CO2 to MongoDB \n'.format(args.containernumber), e)

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
        # print(overallList)
        CO2_DataDict = {'Date_Time': overallList[0], 'CO2_Con': overallList[1], 'Sensor': 'EZO-CO2',
                        'Container_No': args.containernumber, 'Experiment_No': args.experimentnumber}
        print('CO2 in container {} good at time {}'.format(args.containernumber, time.strftime("%H:%M:%S")))
        if __name__ == '__main__':
            if startup:
                p.start()
                startup= False
                print('startup == false')
            else:
                p.join()
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
                                                              time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))
        csvCO2 = '{}/CO2_Bucket_{}_{}_{}.csv'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"),
                                                      time.strftime("%H--%M--%S"))
