import serial
import time
import struct
import pathlib
import csv

Bucket_4_port = 'COM50'
baud_rate = 9600
b1Serial = serial.Serial(Bucket_4_port, baud_rate)

directoryBase = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\{}\Bucket 4\CH4".format(time.strftime("%m-%d-%Y"))
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
logFileCH4  = '{}\\CH4_Bucket_4_{}_{}_log.bin'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
csvCH4 = '{}\\CH4_Bucket_4_{}_{}.csv'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
header = ['Date/Time', 'CH4 Concentration (%)']

overallList = []
count = 0
startTime = time.time()

barray = []

packetstart = False
packetcount = -1
packetsize = -1

b1Serial.reset_input_buffer()

b1_read_command = (b'\x11\x01\x01\xED')
while True:
    with open(logFileCH4, 'ab') as log:
        with open(csvCH4, 'a', newline = '') as c:
            writer = csv.writer(c)
            if count == 0:
                writer.writerow(header)
            b1Serial.write(b1_read_command)
            time.sleep(1)
            while b1Serial.in_waiting:
                newb = b1Serial.read(size=1)
                barray.append(newb)
                log.write(newb)
                # print(barray)

                if (packetstart and packetsize == -1):
                    packetsize = int.from_bytes(newb, 'little')

                if (packetstart and packetsize > 1):
                    packetcount = packetcount + 1

                if (packetcount == packetsize + 1):
                    wholeInput = b''.join(barray)
                    print(wholeInput)

                    unpack = struct.unpack('>BBBHHB', wholeInput)
                    print(unpack)

                    packetstart = False
                    packetsize = -1
                    packetcount = -1

                    wholeInput = b''
                    barray = []
                    overallList.append(time.strftime("%m-%d-%Y %H:%M:%S"))
                    for i in range(len(unpack)):
                        overallList.append(str(unpack[i]))
                    print(overallList)
                    count += 1

                    writer.writerow(overallList)
                    overallList = []
                if (newb == b'\x16'):
                    packetstart = True


    if time.time() - startTime >= 3600:
        count = 0
        DataList = []
        overallList = [0,0]
        startTime = time.time()
        logFileCH4 = '{}\\CH4_Bucket_4_{}_{}_log.bin'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))
        csvCH4 = '{}\\CH4_Bucket_4_{}_{}.csv'.format(directoryBase, time.strftime("%m-%d-%Y"), time.strftime("%H;%M;%S"))