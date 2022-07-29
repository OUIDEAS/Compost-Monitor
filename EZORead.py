import serial
import time
import csv

O2Port = 'COM9'
CO2Port = 'COM8'
RedBoardPort = 'COM7'

baud_rate = 9600


O2Serial = serial.Serial(O2Port, baud_rate, timeout=2)
CO2Serial = serial.Serial(CO2Port, baud_rate, timeout=1)
RedBoardSerial = serial.Serial(RedBoardPort, baud_rate, timeout=1)


header = ['Date', 'Time', 'EZO CO2 Con (ppm)', 'EZO O2 Con (%)', 'SGP CO2 Con (ppm)', 'SGP TVOC (ppb)', 'BME Humidity (%)',
          'BME Pressure (Pa)', 'BME Temp (Deg C)']

data: list[list[str]] = []
row: list[str] = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
CO2line: str
O2line: str
RedBoardline: str

i = 0

with open('C:\\Users\\danbr\\Desktop\\IDEAS Lab Work\\Test Data\\Test_All_Sensors_2.csv', 'w',
          encoding='UTF8', newline='\r') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    while 1:
        O2line = O2Serial.read_until('\r', size = 6)
        #time.sleep(1)

        CO2line = CO2Serial.read_until('\r', size=4)
        time.sleep(1)

        RedBoardline = RedBoardSerial.read_until()
        #time.sleep(1)
        try:
            O2line = O2line.decode("utf-8")
            CO2line = CO2line.decode("utf-8")
            RedBoardline = RedBoardline.decode("utf-8")
            RedBoardData = RedBoardline.split(';')
            testTime = time.strftime("%m/%d/%Y %H:%M:%S")
            nowDate: str = testTime.split(' ').pop(-2)
            nowTime: str = testTime.split(' ').pop()
            row.append(nowDate)
            row.pop(-10)
            row.append(nowTime)
            row.pop(-10)
            row.append(O2line)
            row.pop(-10)
            row.append(CO2line)
            row.pop(-10)
            row.append(RedBoardData[0])
            row.append(RedBoardData[1])
            row.append(RedBoardData[2])
            row.append(RedBoardData[3])
            row.append(RedBoardData[4])
            row.pop(-10)
            row.pop(-10)
            row.pop(-10)
            row.pop(-10)
            row.pop(-10)
            print(row)

            data.append(row)
            writer.writerow(data[i])
            i += 1

        except:
            print("didn't work")