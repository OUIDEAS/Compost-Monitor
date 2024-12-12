import time
import serial
import pathlib
import argparse
import datetime
import struct
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, false, over
from sqlalchemy import text
import smtplib
import sys, os

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--containernumber')
try:
    parser.add_argument('-c', '--comport')
    parser.add_argument('-f', '--filename')
    # parser.add_argument('-cn', '--collection')
    parser.add_argument('-e', '--experimentnumber')
    args = parser.parse_args()

    CH4Port = ''.join(args.comport)

    baud_rate = 9600
    CH4Serial = serial.Serial(CH4Port, baud_rate)
    directoryBase = "{}/{}/Bucket {}/CH4".format(args.filename, (time.strftime("%m-%d-%Y")), args.containernumber)
    pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
    logFileCH4 = '{}/CH4_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"),
                                                        time.strftime("%H--%M--%S"))
    csvCH4 = '{}/CH4_Bucket_{}_{}_{}.csv'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), 
                                                time.strftime("%H--%M--%S"))
    header = ['Date_Time', 'Parse_1', 'Parse_2', 'Parse_3', 'CH4 Concentration (%)', 'Parse_5', 'Parse_6', 'Sensor', 
            'Container_No', 'Experiment_No']
    sent = False
    count = 0
    barray = []
    DataList = []
    overallList = []
    CH4_DataDict = {}

    packetstart = False
    packetcount = -1
    packetsize = -1
    lencount = 0

    mydb = mysql.connector.connect(
    host="100.81.24.41",
    user="root",
    password="pixhawk2",
    database="CompostMonitor"
    )

    mycursor = mydb.cursor()
    # Create a pandas DataFrame to hold the sensor data
    data_frame = pd.DataFrame(columns=['SensID','Sensor','BuckID','ExpNum','DT','dateTime','CH4_CON','Unit','Parse_1','Parse_2','Parse_3','Parse_5','Parse_6'])

    startTime = time.time()

    # Set up the MySQL connection using SQLAlchemy for pandas to_sql
    engine = create_engine("mysql+mysqlconnector://root:pixhawk2@localhost/CompostMonitor")  # Replace 'yourpassword' with your SQL root password

    # print('RUNNING THIS')
    readCommand = 'R\r'.encode('utf-8')
    # loopTimer = 90

    read_command = (b'\x11\x01\x01\xED')

    while count < 1:
        if not CH4Serial.is_open:
            print('closed')
            break
        CH4Serial.reset_input_buffer()
        CH4Serial.reset_output_buffer()
        CH4Serial.write(read_command)
        CH4Serial.flush()
            # loopStartTime = time.time()
        time.sleep(2)


        while CH4Serial.in_waiting:
            # print('LINE 78')
            newb = CH4Serial.read(CH4Serial.in_waiting or 1)
            # print(newb)
            barray.append(newb)
            # lencount += 1
            # # log.write(newb)
            # # print(barray)
            # ## second byte (status is first byte) shows the size of the packet - use that to set the length of the word
            # if (packetstart and packetsize == -1):
            #     # print('87')
            #     packetsize = int.from_bytes(newb, 'little')

            # ## count up each loop when packetsize is not default value
            # if (packetstart and packetsize > 1):
            #     # print('92')
            #     packetcount = packetcount + 1

            # ## handle status byte and check that incoming byte is actually the status byte, not the last byte in a word
            # if (newb == b'\x16'):
            #     # print('97')
            #     if (lencount != 0 and lencount < packetsize + 1):
            #         # print('lencount is now:', lencount)
            #         # print('packetsize is currently:', packetsize)
            #         lencount = 0
            #     else:
            #         packetstart = True
            
            # ## parse error codes
            # if (lencount == 6 and newb != b'\x00'):
            #     # print('107')
            #     newb_bin = int(newb, 16)
            #     bStr = ''
            #     while newb_bin > 0:
            #         bStr = str(newb_bin % 2) + bStr
            #         newb_bin = newb_bin >> 1   
            #     errorcode = bStr
                # message = f"Methane sensor in container {args.containernumber} has encountered an issue. Error code {errorcode}"
                # send_sms_via_email(number, message, provider, sender_credentials)

            ## if the packetcount and the size of the packet match, the word is finished - now time to decode
            ## and prepare to start over
            
            # if (packetcount == packetsize + 1):
                # print('121')
            wholeInput = b''.join(barray)
            # print(wholeInput)

            unpack = struct.unpack('>BBBHHB', wholeInput)
            # print(unpack)
            # print(len(unpack))
            overallList.append(datetime.datetime.now())
            for i in range(len(unpack)):
                # print(str(unpack[i]))
                # print(unpack(i), type(unpack(i)))
                overallList.append(int(unpack[i]))

            # if count == 0:
            #     overallList[0] = overallList[2]
            #     overallList[2] = 0
            # print(overallList)
            
            CH4_con =  (int(overallList[4])*256 + (overallList[5]))/100
            # print(CH4_con)
            # print('CH4', overallList[6], overallList[7], CH4_con)
            if overallList[4] != '*OK' and count < 1:
                CH4_DataDict = {
                                    'SensID': [CH4Port],
                                    'Sensor': ['Methane'],
                                    'BuckID': [args.containernumber],
                                    'ExpNum': [1],
                                    'DT': [120],
                                    'dateTime': overallList[0],
                                    'CH4_CON': CH4_con,
                                    'Unit': ['PCT VOl'],
                                    'Parse_1': [overallList[1]], 
                                    'Parse_2': [overallList[2]],
                                    'Parse_3': [overallList[3]], 
                                    'Parse_5': [overallList[5]],
                                    'Parse_6': [overallList[6]]}
                count+=1
                # print('Methane in container {} good at time {}'.format(args.containernumber, time.strftime("%H:%M:%S")))
                dfn = pd.DataFrame(CH4_DataDict)
                # data_frame = pd.concat([data_frame, dfn], ignore_index=True)
                dfn.to_sql(name='CH4', con=engine, if_exists='append')
                print(f'CH4 Data from Bucket {args.containernumber} Uploaded to SQL Database!', 'CH4_Con:', CH4_con)
                print(f'CH4 in container {args.containernumber} good at time {time.strftime("%H:%M:%S")}')

            else:
                print(f"Invalid CH4 concentration data from Bucket {args.containernumber} received: {overallList[4]}")

                # if __name__ == '__main__':
                #     if startup:
                #         p.start()
                #         startup = False
                #         print('startup == false')
                #     else:
                #         p.join()
                #         p.close()
                #         p = multiprocessing.Process(target=upload_to_database, args=(methane_DataDict,))
                #         p.start()

            packetstart = False
            packetsize = -1
            packetcount = -1

            wholeInput = b''
            barray = []
            overallList = []

            # print('lencount and packetsize:', lencount, packetsize)
            lencount = 0
            CH4Serial.close()
            break

                # count += 1

    # while (time.time() - loopStartTime) < loopTimer:
    #     time.sleep(0.1)

    # if time.time() - startTime >= 3600:
    #     count = 0
    #     DataList = []
    #     overallList = [0,0]
    #     startTime = time.time()
    #     logFileCH4 = '{}/CH4_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber,
    #                                                         time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))
except Exception as error:
    
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    email_user = 'ideascompostserver@gmail.com'
    send_mail = '8478046268@txt.att.net'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # server.login(email_user, 'kcedyafdbqacqrqu')
    server.login(email_user, 'ebtn zksf iqzu wipl')
    message = f'CH4 Failure of Bin {args.containernumber} \n {error} at line {exc_tb.tb_lineno}at {datetime.datetime.now()}'
    server.sendmail(email_user, send_mail, message)
    server.quit()
    # print('too bad')
        