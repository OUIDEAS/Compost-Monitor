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



# factory = 'Factory'.encode('utf-8')
# CO2Serial.write(factory)
# CO2Serial.flush()

cal_command = 'Cal,clear\r'.encode('utf-8')
CO2Serial.write(cal_command)
CO2Serial.flush()
noOK = '*OK,0\r'.encode('utf-8')
CO2Serial.write(noOK)
CO2Serial.flush()


CO2Serial.close()