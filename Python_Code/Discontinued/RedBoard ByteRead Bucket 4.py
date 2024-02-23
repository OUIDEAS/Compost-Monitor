import time
import serial
import csv
import pathlib


RBPort = 'COM55'
baud_rate = 9600
RBSerial = serial.Serial(RBPort, baud_rate, timeout=1)
directoryBase = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\{}\Bucket 4\RB".format(time.strftime("%m-%d-%Y"))
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
logFileRB  = '{}\\RB_Bucket_4_{}_{}_log.bin'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
csvRB = '{}\\RB_Bucket_4_{}_{}.csv'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))

count = 0
bytearray = []
RB_DataList = []

header = ['Date/Time',
          # 'SGP CO2 Con (ppm)',
          'SGP TVOC (ppb)',
          'BME Humidity (%)',
          'BME Pressure (Pa)',
          'BME Temp (Deg C)']

startTime = time.time()

while 1:
    RB_inbyte = RBSerial.read(size=1)
    with open(logFileRB, 'ab') as l:
        l.write(RB_inbyte)
    bytearray.append(RB_inbyte)
    if RB_inbyte == b'\n':
        #split it up
        bytearray.pop()
        with open(csvRB, 'a', newline = '') as table:
            writer = csv.writer(table)
            if count == 0:
                writer.writerow(header)
            RB_DataSplit = ''.join(str(bytearray)).replace(" ", "").replace('b', '').replace("'", '').replace(",", '').replace('[', '').replace(']', '').split(';')
            RB_DataList.append(time.strftime("%m-%d-%Y %H:%M:%S"))
            for i in range(len(RB_DataSplit)):
                RB_DataList.append(RB_DataSplit[i])
            print(RB_DataList)
            writer.writerow(RB_DataList)
            RB_DataList = []

        bytearray = []
        count += 1
    if time.time() - startTime >= 3600:
        count = 0
        RB_DataList = []
        startTime = time.time()
        logFileRB = '{}\\RB_Bucket_4_{}_{}_log.bin'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
        csvRB = '{}\\RB_Bucket_4_{}_{}.csv'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))