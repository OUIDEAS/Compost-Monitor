import time
import serial
import csv
import pathlib

CO2Port = 'COM51'
baud_rate = 9600
CO2Serial = serial.Serial(CO2Port, baud_rate, timeout=1)
directoryBase = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\{}\Bucket 3\CO2".format(time.strftime("%m-%d-%Y"))
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
logFileCO2  = '{}\\CO2_Bucket_3_{}_{}_log.bin'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
csvCO2 = '{}\\CO2_Bucket_3_{}_{}.csv'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))

count = 0
bytearray = []
DataList = []
overallList = [0,0]

header = [ 'Date/Time', 'CO2 Concentration (ppm)']

startTime = time.time()

while 1:
    CO2_inbyte = CO2Serial.read(size=1)
    with open(logFileCO2, 'ab') as l:
        l.write(CO2_inbyte)
    bytearray.append(CO2_inbyte)
    if CO2_inbyte == b'\r':
        #split it up
        bytearray.pop()
        with open(csvCO2, 'a', newline = '') as table:
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
        logFileCO2 = '{}\\CO2_Bucket_3_{}_{}_log.bin'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
        csvCO2 = '{}\\CO2_Bucket_3_{}_{}.csv'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))