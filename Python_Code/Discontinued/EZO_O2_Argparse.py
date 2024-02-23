import time
import serial
import csv
import pathlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--comport')
parser.add_argument('-f', '--filename')
parser.add_argument('-n', '--containernumber')
args = parser.parse_args()

port = ''.join(args.comport)
baud_rate = 9600
serialPort = serial.Serial(port, baud_rate, timeout=1)
directoryBase = "{}/{}/Bucket {}/O2".format(args.filename, time.strftime("%m-%d-%Y"), args.containernumber)
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
logFileO2 = '{}/O2_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
csvO2 = '{}/O2_Bucket_{}_{}_{}.csv'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))

count = 0
bytearray = []
DataList = []
overallList = [0,0]

header = ['Date/Time', 'O2 Concentration (%)']

startTime = time.time()

while 1:
    O2_inbyte = serialPort.read(size=1)
    with open(logFileO2, 'ab') as l:
        l.write(O2_inbyte)
    bytearray.append(O2_inbyte)
    if O2_inbyte == b'/r':
        bytearray.pop()
        with open(csvO2, 'a', newline = '') as table:
            writer = csv.writer(table)
            if count == 0:
                writer.writerow(header)
            DataList.append(''.join(str(bytearray)).replace(" ", "").replace('b', '').replace("'", '').replace(",", '').replace('[', '').replace(']', ''))
            overallList.append(time.strftime("%m-%d-%Y %H:%M:%S"))
            overallList.append(str(''.join(DataList[count])))
            overallList.pop(0)
            overallList.pop(0)
            print(overallList)
            writer.writerow(overallList)

        bytearray = []
        count += 1
    if time.time() - startTime >= 3600:
        count = 0
        DataList = []
        overallList = [0,0]
        startTime = time.time()
        logFileO2 = '{}/O2_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber,
                                                            time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
        csvO2 = '{}/O2_Bucket_{}_{}_{}.csv'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"),
                                                    time.strftime("%H;%M;%S"))