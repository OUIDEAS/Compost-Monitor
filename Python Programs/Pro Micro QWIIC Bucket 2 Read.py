import time
import serial
import csv
import pathlib


PMQPort = 'COM56'
baud_rate = 9600
PMQSerial = serial.Serial(PMQPort, baud_rate, timeout=1)
directoryBase = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\{}\Bucket 2\PMQ".format(time.strftime("%m-%d-%Y"))
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
logFilePMQ= '{}\\PMQ_Bucket_2_{}_{}_log.bin'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
csvPMQ = '{}\\PMQ_Bucket_2_{}_{}.csv'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))

count = 0
bytearray = []
PMQ_DataList = []

header = ['Date/Time',
          'SGP TVOC (ppb)',
          'BME Humidity (%)',
          'BME Pressure (Pa)',
          'BME Temp (Deg C)']

startTime = time.time()

while 1:
    PMQ_inbyte = PMQSerial.read(size=1)
    with open(logFilePMQ, 'ab') as l:
        l.write(PMQ_inbyte)
    bytearray.append(PMQ_inbyte)
    if PMQ_inbyte == b'\n':
        #split it up
        bytearray.pop()
        with open(csvPMQ, 'a', newline = '') as table:
            writer = csv.writer(table)
            if count == 0:
                writer.writerow(header)
            PMQ_DataSplit = ''.join(str(bytearray)).replace(" ", "").replace('b', '').replace("'", '').replace(",", '').replace('[', '').replace(']', '').split(';')
            PMQ_DataList.append(time.strftime("%m-%d-%Y %H:%M:%S"))
            for i in range(len(PMQ_DataSplit)):
                PMQ_DataList.append(PMQ_DataSplit[i])
            print(PMQ_DataList)
            writer.writerow(PMQ_DataList)
            PMQ_DataList = []

        bytearray = []
        count += 1
    if time.time() - startTime >= 3600:
        count = 0
        PMQ_DataList = []
        startTime = time.time()
        logFilePMQ = '{}\\PMQ_Bucket_2_{}_{}_log.bin'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
        csvPMQ = '{}\\PMQ_Bucket_2_{}_{}.csv'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))