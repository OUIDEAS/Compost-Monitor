import serial
import time
import struct
import pathlib
import argparse
import multiprocessing
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import datetime
import csv

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--comport')
parser.add_argument('-f', '--filename')
parser.add_argument('-n', '--containernumber')
parser.add_argument('-cn', '--collection')
parser.add_argument('-e', '--experimentnumber')
args = parser.parse_args()

''' UNCOMMENT THESE LINES ONLY FOR DEBUGGING '''
''' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV '''
# args.comport = "/dev/ttyUSB0"
# args.filename = "/home/dan/sensorTest"
# args.containernumber = 1234
# args.collection = 'dn'
# args.experimentnumber = 1234
''' ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ '''
''' UNCOMMENT THESE LINES ONLY FOR DEBUGGING '''


port = ''.join(args.comport)
baud_rate = 9600
serialPort = serial.Serial(port, baud_rate)

directoryBase = "{}/{}/Bucket {}/CH4".format(args.filename, (time.strftime("%m-%d-%Y")), args.containernumber)
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
logFileCH4 = '{}/CH4_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"),
                                                     time.strftime("%H--%M--%S"))
csvCH4 = '{}/CH4_Bucket_{}_{}_{}.csv'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), 
                                             time.strftime("%H--%M--%S"))
header = ['Date_Time', 'Parse_1', 'Parse_2', 'Parse_3', 'CH4 Concentration (%)', 'Parse_5', 'Parse_6', 'Sensor', 
          'Container_No', 'Experiment_No']

overallList = []
count = 0
startTime = time.time()

barray = []
methane_DataDict = {}

packetstart = False
packetcount = -1
packetsize = -1
lencount = 0

serialPort.reset_input_buffer()

startup = True

client = MongoClient("mongodb://localhost:27017/")
db = client['CompostMonitor']
collection = db['{}'.format(args.collection)]

def upload_to_database(data):
    try:
        # Insert the data into the collection
        # collection.insert_one(data)
        print('Container {} methane saved to MongoDB!'.format(args.containernumber))
    except PyMongoError as e:
        print('Error saving container {} methane to MongoDB \n'.format(args.containernumber), e)

p = multiprocessing.Process(target = upload_to_database, args = (methane_DataDict,))

read_command = (b'\x11\x01\x01\xED')
loopTimer    = 90.0



try:
    while True:

        with open(logFileCH4, 'ab') as log:
            with open(csvCH4, 'a', newline = '') as c:
                writer = csv.writer(c)
                if count == 0:
                    writer.writerow(header)

                readingSend = time.time()

                serialPort.write(read_command)
                time.sleep(0.1)

                while serialPort.in_waiting:
                    newb = serialPort.read(size=1)
                    # print(newb)
                    barray.append(newb)
                    lencount += 1
                    log.write(newb)

                    ''' second byte (status is first byte) shows the size of the packet - use that to set the length 
                                                                                                    of the word'''
                    if (packetstart and packetsize == -1):
                        packetsize = int.from_bytes(newb, 'little')

                    ## count up each loop when packetsize is not default value
                    if (packetstart and packetsize > 1):
                        packetcount = packetcount + 1

                    ''' handle status byte and check that incoming byte is actually the status byte, not the last 
                                                                                                    byte in a word'''
                    if (newb == b'\x16'):
                        if (lencount != 0 and lencount < packetsize + 1):
                            print('lencount is now:', lencount)
                            print('packetsize is currently:', packetsize)
                            lencount = 0
                        else:
                            packetstart = True

                    ''' if the packetcount and the size of the packet match, the word is finished - now time to decode
                                                                                        and prepare to start over'''
                    if (packetcount == packetsize + 1):
                        wholeInput = b''.join(barray)
                        # print(wholeInput)

                        unpack = struct.unpack('>BBBHHB', wholeInput)
                        # print(unpack)
                        serialPort.reset_input_buffer

                        overallList.append(datetime.datetime.now())
                        for i in range(len(unpack)):
                            overallList.append(str(unpack[i]))
                        # print(overallList)
                        overallList.append(args.containernumber)
                        overallList.append(args.experimentnumber)
                        writer.writerow(overallList)

                        methane_DataDict = {'Date_Time': overallList[0], 'Parse_1': overallList[1], 'Parse_2': overallList[2],
                                            'Parse_3': overallList[3], 'Methane_Con': overallList[4], 'Parse_5': overallList[5],
                                            'Parse_6': overallList[6], 'Sensor': 'Methane',
                                            'Container_No': args.containernumber, 'Experiment_No': args.experimentnumber}
                        print('Methane in container {} good at time {}. Concentration: {}. Current file: CH4_Bucket_{}_{}_{}_log.bin'.format(
                            args.containernumber, time.strftime("%H:%M:%S"), overallList[4], args.containernumber, time.strftime("%m-%d-%Y"),
                            time.strftime("%H--%M--%S")))

                        if __name__ == '__main__':
                            if startup:
                                p.start()
                                startup = False
                                print('startup == false')
                            else:
                                p.join()
                                p.close()
                                p = multiprocessing.Process(target=upload_to_database, args=(methane_DataDict,))
                                p.start()

                        packetstart = False
                        packetsize = -1
                        packetcount = -1

                        wholeInput = b''
                        barray = []
                        overallList = []

                        # print('lencount and packetsize:', lencount, packetsize)
                        lencount = 0

                        count += 1
            while (time.time() - readingSend <= loopTimer):
                time.sleep(0.1)
except IOError as e:
    current_date = datetime.datetime.now()
    errorMessage = 'IOError at {}. CH4 sensor at {} has disconnected.'.format(current_date, args.comport)
    print(errorMessage)
    with open(logFileCH4, 'ab') as log:
        date_binary = current_date.strftime("%m-%d-%Y %H:%M:%S").encode('utf-8')
        log.write(struct.pack(f"{len(date_binary)}s", date_binary))





    if (count > 499):
        count = 0
        DataList = []
        overallList = [0,0]
        startTime = time.time()
        logFileCH4 = '{}/CH4_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber,
                                                              time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))

        csvCH4 = '{}/CH4_Bucket_{}_{}_{}.csv'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), 
                                                    time.strftime("%H--%M--%S"))
