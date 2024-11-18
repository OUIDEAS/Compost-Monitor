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
O2Port = ''.join(args.comport)
# print('THE PORT IS THIS:', CO2Port)
baud_rate = 9600
O2Serial = serial.Serial(O2Port, baud_rate, timeout=90)





cal_command = 'Cal,20.9\r'.encode('utf-8')
O2Serial.write(cal_command)
O2Serial.flush()
noOK = '*OK,0\r'.encode('utf-8')
O2Serial.write(noOK)
O2Serial.flush()
# O2Percent = 'O,%,0'.encode('utf-8')
# O2Serial.write(O2Percent)
# O2Serial.flush()
O2Ppt = 'O,PPT,1'.encode('utf-8')
O2Serial.write(O2Ppt)
O2Serial.flush()