import serial
import time
import struct
import pathlib
import argparse
import multiprocessing
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import datetime
import smtplib
import ssl
from providers import PROVIDERS

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--comport')
parser.add_argument('-f', '--filename')
parser.add_argument('-n', '--containernumber')
parser.add_argument('-cn', '--collection')
parser.add_argument('-e', '--experimentnumber')
args = parser.parse_args()

port = ''.join(args.comport)
baud_rate = 9600
serialPort = serial.Serial(port, baud_rate)

directoryBase = "{}/{}/Bucket {}/CH4".format(args.filename, (time.strftime("%m-%d-%Y")), args.containernumber)
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
logFileCH4 = '{}/CH4_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber, time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))

overallList = []
count = 0
startTime = time.time()

barray = []
methane_DataDict = {}

packetstart = False
packetcount = -1
packetsize = -1
lencount = 0

serialPort.reset_input_buffer()

startup = True

client = MongoClient("mongodb://localhost:27017/")
db = client['CompostMonitor']
collection = db['{}'.format(args.collection)]

def upload_to_database(data):
    try:
        # Insert the data into the collection
        collection.insert_one(data)
        print('Container {} methane saved to MongoDB!'.format(args.containernumber))
    except PyMongoError as e:
        print('Error saving container {} methane to MongoDB \n'.format(args.containernumber), e)

p = multiprocessing.Process(target = upload_to_database, args = (methane_DataDict,))

def send_sms_via_email(
        number: str,
        message: str,
        provider: str, 
        sender_credentials: tuple,
        subject: str = "Compost Monitor Reports",
        smtp_server = "smtp.gmail.com",
        smtp_port: int = 465,
):
    sender_email, email_password = sender_credentials
    receiver_email = f"{number}@{PROVIDERS.get(provider).get('sms')}"

    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ssl.create_default_context()) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)

number = "4407498307"
provider = "T-Mobile"
sender_credentials = ("ideascompostmonitor@gmail.com", "uptrrccfbehyrxso")

read_command = (b'\x11\x01\x01\xED')
while True:
    try:
        with open(logFileCH4, 'ab') as log:


            serialPort.write(read_command)
            time.sleep(1)


            while serialPort.in_waiting:
                newb = serialPort.read(size=1)
                print(newb)
                barray.append(newb)
                lencount += 1
                log.write(newb)

                ## second byte (status is first byte) shows the size of the packet - use that to set the length of the word
                if (packetstart and packetsize == -1):
                    packetsize = int.from_bytes(newb, 'little')

                ## count up each loop when packetsize is not default value
                if (packetstart and packetsize > 1):
                    packetcount = packetcount + 1

                ## handle status byte and check that incoming byte is actually the status byte, not the last byte in a word
                if (newb == b'\x16'):
                    if (lencount != 0 and lencount < packetsize + 1):
                        # print('lencount is now:', lencount)
                        # print('packetsize is currently:', packetsize)
                        lencount = 0
                    else:
                        packetstart = True
                
                ## parse error codes
                if (lencount == 6 and newb != b'\x00'):
                    newb_bin = int(newb, 16)
                    bStr = ''
                    while newb_bin > 0:
                        bStr = str(newb_bin % 2) + bStr
                        newb_bin = newb_bin >> 1   
                    errorcode = bStr
                    message = f"Methane sensor in container {args.containernumber} has encountered an issue. Error code {errorcode}"
                    send_sms_via_email(number, message, provider, sender_credentials)

                ## if the packetcount and the size of the packet match, the word is finished - now time to decode
                ## and prepare to start over
                if (packetcount == packetsize + 1):
                    wholeInput = b''.join(barray)
                    # print(wholeInput)

                    unpack = struct.unpack('>BBBHHB', wholeInput)
                    # print(unpack)

                    overallList.append(datetime.datetime.now())
                    for i in range(len(unpack)):
                        # print(unpack(i), type(unpack(i)))
                        overallList.append(str(unpack[i]))
                    # print(overallList)

                    methane_DataDict = {'Date_Time': overallList[0], 'Parse_1': overallList[1], 'Parse_2': overallList[2],
                                        'Parse_3': overallList[3], 'Methane_Con': overallList[4], 'Parse_5': overallList[5],
                                        'Parse_6': overallList[6], 'Sensor': 'Methane',
                                        'Container_No': args.containernumber, 'Experiment_No': args.experimentnumber}
                    print('Methane in container {} good at time {}'.format(args.containernumber, time.strftime("%H:%M:%S")))

                    if __name__ == '__main__':
                        if startup:
                            p.start()
                            startup = False
                            print('startup == false')
                        else:
                            p.join()
                            p.close()
                            p = multiprocessing.Process(target=upload_to_database, args=(methane_DataDict,))
                            p.start()

                    packetstart = False
                    packetsize = -1
                    packetcount = -1

                    wholeInput = b''
                    barray = []
                    overallList = []

                    # print('lencount and packetsize:', lencount, packetsize)
                    lencount = 0

                    count += 1

                    time.sleep(4)

        if time.time() - startTime >= 3600:
            count = 0
            DataList = []
            overallList = [0,0]
            startTime = time.time()
            logFileCH4 = '{}/CH4_Bucket_{}_{}_{}_log.bin'.format(directoryBase, args.containernumber,
                                                                time.strftime("%m-%d-%Y"), time.strftime("%H--%M--%S"))

    except Exception as e:
        message = f"Methane sensor in container {args.containernumber} has encountered an issue: {Exception}"
        send_sms_via_email(number, message, provider, sender_credentials)