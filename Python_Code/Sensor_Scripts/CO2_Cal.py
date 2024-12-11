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
CO2Port = ''.join(args.comport)
# print('THE PORT IS THIS:', CO2Port)
baud_rate = 9600
CO2Serial = serial.Serial(CO2Port, baud_rate, timeout=90)



cal_command = 'Cal,clear\r'.encode('utf-8')

CO2Serial.write(cal_command)
CO2Serial.flush()
time.sleep(1)
# factory = 'Factory'.encode('utf-8')
# CO2Serial.write(factory)
# CO2Serial.flush()
# time.sleep(1)
# # # 
# noOK = '*OK,0\r'.encode('utf-8')
# CO2Serial.write(noOK)
# CO2Serial.flush()
# time.sleep(1)
# stat_command = 'Status\r'.encode('utf-8')
# CO2Serial.write(stat_command)
# CO2Serial.flush()
# CO2Serial.reset_input_buffer()
# CO2Serial.reset_output_buffer()
# readCommand = 'R\r'.encode('utf-8')
# CO2Serial.write(readCommand)
# CO2Serial.flush()
# time.sleep(.5)
# while :
response = CO2Serial.read(CO2Serial.in_waiting or 1)  # Read all available bytes
if response:
    try:
        # Decode the byte response to a string
        response_str = response.decode('utf-8').strip()  # Strip removes any extraneous \r or \n

        # Convert the string to a floating-point number
        co2_value = float(response_str)
        print(f"CO₂ Reading: {co2_value} ppm")  # Output the CO₂ reading in parts per million (ppm)
    except ValueError:
        print(f"Failed to parse CO₂ reading: {response_str}")
else:
    print("No response received.")

CO2Serial.close()
