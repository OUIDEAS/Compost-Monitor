import time
import serial
import csv
import pathlib

O2Port = 'COM59'
baud_rate = 9600
O2Serial = serial.Serial(O2Port, baud_rate, timeout=1)
directoryBase = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\{}\Bucket 2\O2".format(time.strftime("%m-%d-%Y"))
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
logFileO2  = '{}\\O2_Bucket_2_{}_{}_log.bin'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
csvO2 = '{}\\O2_Bucket_2_{}_{}.csv'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))

count = 0
bytearray = []
DataList = []
overallList = [0,0]

header = [ 'Date/Time', 'O2 Concentration (%)']

startTime = time.time()

while 1:
    O2_inbyte = O2Serial.read(size=1)
    with open(logFileO2, 'ab') as l:
        l.write(O2_inbyte)
    # print(O2_inbyte)
    bytearray.append(O2_inbyte)
    if O2_inbyte == b'\r':
        #split it up
        bytearray.pop()
        with open(csvO2, 'a', newline = '') as table:
            writer = csv.writer(table)
            if count == 0:
                writer.writerow(header)
            DataList.append(''.join(str(bytearray)).replace(" ", "").replace('b', '').replace("'", '').replace(",", '').replace('[', '').replace(']', ''))
            # print(DataList[count])
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
        logFileO2 = '{}\\O2_Bucket_2_{}_{}_log.bin'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
        csvO2 = '{}\\O2_Bucket_2_{}_{}.csv'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))