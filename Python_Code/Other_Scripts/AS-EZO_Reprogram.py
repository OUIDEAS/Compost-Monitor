import serial
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--ports')
parser.add_argument('-c', '--command')
args = parser.parse_args()


ports = []
portsString = args.ports
portsString.split(',')

serialPorts = []
baud_rate = 9600
for port in ports:
    serialPort = serial.Serial(port, baud_rate, timeout=1)
    serialPorts.append(serialPort)

for serialPort in serialPorts:
    serialPort.write('{}\r'.format(args.command))
    time.sleep(1)
    while serialPort.in_waiting:
        newb = serialPort.read(size=1)
        print(newb)