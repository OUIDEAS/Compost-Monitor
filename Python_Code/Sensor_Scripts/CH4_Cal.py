import time
from unittest.mock import sentinel
import serial
import pathlib
import argparse
import datetime
import pandas as pd
import mysql.connector
from sqlalchemy import Null, create_engine, over
from sqlalchemy import text
import smtplib
import sys, os


# Set up argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--containernumber')
parser.add_argument('-c', '--comport')
parser.add_argument('-f', '--filename')

# parser.add_argument('-e', '--experimentnumber')
args = parser.parse_args()

# Serial connection and file paths
CH4Port = ''.join(args.comport)
# print('THE PORT IS THIS:', CH4Port)
baud_rate = 9600
CH4Serial = serial.Serial(CH4Port, baud_rate, timeout=90)
# cal_Command = 'R\r'.encode('utf-8')
# loopTimer = 90

# cal_command = (b'\x11\x02\x4D\x00\x60')
cal_command = (b'\x11\x04\x4B\x00\x00\x00\x86')
# 11 02 4D 00 60


# factory = 'Factory'.encode('utf-8')
# CH4Serial.write(factory)
# CH4Serial.flush()
try:
    # Open serial connection
    with CH4Serial as ser:
        print(f"Connected to {CH4Port}")
        
        # Send the command
        ser.write(cal_command)
        print(f"Sent: {cal_command}")
        CH4Serial.flush()
        
        # Allow some time for the sensor to respond
        time.sleep(2)
        
        # Read the response
        response = ser.read(ser.in_waiting or 1)  # Read all available bytes
        if response:
            print(f"Received: {response}")
        else:
            print("No response received.")
    CH4Serial.close()
            
except serial.SerialException as e:
    print(f"Error: {e}")
# cal_command = 'Cal,clear\r'.encode('utf-8')
# CH4Serial.write(cal_command)
# CH4Serial.flush()
# noOK = '*OK,0\r'.encode('utf-8')
# CH4Serial.write(noOK)
# CH4Serial.flush()


CH4Serial.close()