import numpy as np
import PyDAQmx as nidaq
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import time
import datetime
import schedule

class TemperatureReader:
    def __init__(self, device_name):
        self.device_name = device_name
        self.task_handle = nidaq.TaskHandle()

    def create_task(self):
        nidaq.DAQmxCreateTask("", nidaq.byref(self.task_handle))
        nidaq.DAQmxCreateAIThrmcplChan(
            self.task_handle,
            f"{self.device_name}/ai0",
            "",
            -200.0,
            1260.0,
            nidaq.DAQmx_Val_DegC,
            nidaq.DAQmx_Val_K_Type_TC,
            nidaq.DAQmx_Val_BuiltIn,
            0.0,
            ""
        )

    def read_temperature(self):
        self.create_task()
        data = np.zeros((1,), dtype=np.float64)
        read = nidaq.int32()

        nidaq.DAQmxStartTask(self.task_handle)
        nidaq.DAQmxReadAnalogF64(
            self.task_handle,
            1,
            10.0,
            nidaq.DAQmx_Val_GroupByChannel,
            data,
            len(data),
            nidaq.byref(read),
            None
        )
        nidaq.DAQmxStopTask(self.task_handle)
        nidaq.DAQmxClearTask(self.task_handle)
        
        return data[0]
    
def MongoUpload(data):
    client = MongoClient("mongodb://100.114.38.109:27017/")
    db = client['Testing_DB']
    collection = db['Thermocouple_Test']
    try:
        collection.insert_one(data)
        print('Thermocouple temp saved to MongoDB @ {}.'.format(time.strftime("%H:%M:%S")))
    except PyMongoError as e:
        print('Error saving thermocouple data to MongoDB @ {}.'.format(time.strftime("%H:%M:%S")))
        print(e)

def theWholeSongAndDance():
    device_name = "Dev1"  # Replace with your device name
    reader = TemperatureReader(device_name)
    temperature = reader.read_temperature()
    print(f"Temperature: {temperature:.2f} °C")
    temperature_dict = {'Date_Time': datetime.datetime.now(), 'Temperature': temperature, 'Sensor': 'USB-TC01', 'Container_No': 'Environment'}
    MongoUpload(temperature_dict)

if __name__ == "__main__":

    theWholeSongAndDance() ## do the whole song and dance when the script launches
    
    schedule.every().hour.at(":00").do(theWholeSongAndDance) # repeat at the top of every hour

    while True:
        schedule.run_pending()
        time.sleep(1)