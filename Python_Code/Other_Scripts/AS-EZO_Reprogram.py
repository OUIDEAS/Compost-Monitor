import serial
import time
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--ports')
parser.add_argument('-c', '--command')
parser.add_argument('-vid', '--vendorID')
parser.add_argument('-pid', '--productID')
args = parser.parse_args()

portsString = args.ports
print(portsString)
ports = portsString.split(',')
print(ports)
print("\n\n\n\n\n\n")
command = '{}\r'.format(args.command)
command = command.encode('utf-8')

serialPorts = []
baud_rate = 9600

def getDevicesByID(pid, vid):
    devices = []
    dev_dir = '/dev'
    for entry in os.listdir(dev_dir):
        if (entry.startswith('ttyUSB') or entry.startswith('ttyACM')):
            entryPath = os.path.join(dev_dir, entry)
            try:
                device_pid, device_vid = map(int, entry[7:].split('.'))
                if (device_pid == pid and device_vid == vid):
                    devices.append(entryPath)
            except ValueError:
                pass
    return devices

def sendCommands(ports, commandInput):
    for port in ports:
        newb_array = []
        serialPort = serial.Serial(port, baud_rate, timeout=1)
        serialPort.reset_input_buffer()
        serialPort.reset_output_buffer()
        print('Now sending command "', commandInput,'" to device at ', port,'.')
        serialPort.write(commandInput)
        time.sleep(1)
        while serialPort.in_waiting:
            newb = serialPort.read(size=1)
            newb_array.append(newb)
        print(newb_array)

class pickOne(Exception):
    pass


if __name__ == '__main__':
    if (args.productID is not None and args.vendorID is not None):
        matchingDevices = getDevicesByID(args.productID, args.vendorID)
        sendCommands(matchingDevices, command)
    elif args.ports is not None:
        sendCommands(ports, command)
    else:
        print("\n")
        print("You need to either provide a range of ports or provide BOTH PID and VID for this script.\n")
        raise pickOne