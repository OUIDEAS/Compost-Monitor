
import serial
import time


serialPort_1 = 'COM3'
baud_rate = 9600
write_to_file_path = "test 1 7-21-22.txt"

output_file = open(write_to_file_path, "w+")
ser1 = serial.Serial(serialPort_1, baud_rate, timeout=4)

while 1:
    line1 = ser1.readline()
    try:
        line1 = line1.decode("utf-8")
        print(time.strftime("%m/%d/%Y %H:%M:%S") + ' ' + line1)
        #output_file.write(time.strftime("%m/%d/%Y %H:%M:%S") + ' ' + line1)
        output_file.write(time.strftime("%m/%d %H:%M:%S") + ' ' + line1)
    except:
        print('skip')

