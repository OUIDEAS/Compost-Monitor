import serial
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--ports')
parser.add_argument('-c', '--command')
args = parser.parse_args()




portsString = args.ports
ports = portsString.split(',')
print(ports)
command = '{}\r'.format(args.command)
command = command.encode('utf-8')


serialPorts = []
baud_rate = 9600
for port in ports:
   newb_array = []
   serialPort = serial.Serial(port, baud_rate, timeout=1)
   serialPort.reset_input_buffer()
   serialPort.reset_output_buffer()
   print('Now sending command to device at ', port,'.')
   serialPort.write(command)
   time.sleep(1)
   while serialPort.in_waiting:
       newb = serialPort.read(size=1)
       newb_array.append(newb)
   print(newb_array)

