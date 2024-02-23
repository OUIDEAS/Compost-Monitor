import serial
import time


ports = []
serialPorts = []
baud_rate = 9600
for port in ports:
    serialPort = serial.Serial(port, baud_rate, timeout=1)
    serialPorts.append(serialPort)

for serialPort in serialPorts:
    serialPort.write('C,90\r')
    time.sleep(1)
    while serialPort.in_waiting:
        newb = serialPort.read(size=1)
        print(newb)