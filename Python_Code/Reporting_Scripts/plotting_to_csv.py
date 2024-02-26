import pandas as pd
import pymongo
import multiprocessing as mp
import datetime
import time
import pathlib

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['CompostMonitor']
collection = db['Overall']
directoryBase = r"home/dan/SuperSecretTestFolder/Compost-Monitor/Python_Code/Reporting_Scripts/Test_CSVs".format(time.strftime("%m-%d-%Y"))
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
def pull_data(container_no, sensor):
    data = collection.find({
                            'Container_No': str(container_no),
                            sensor: {'$exists': 'True'}
                            }).sort("_id", pymongo.ASCENDING)
    collection_df = pd.DataFrame(data)

    match sensor:
        case 'TVOC_Con':
            TVOC_df = collection_df[['Date_Time', 'TVOC_Con']]
            TVOC_df.to_csv(f'/home/dan/Desktop/CSVs/{time.strftime("%m-%d-%Y")}/TVOC_{container_no}.csv')
        case 'CO2_Con':
            CO2_df = collection_df[['Date_Time', 'CO2_Con']]
            CO2_df.to_csv(f'/home/dan/CompostMonitor_git/Compost-Monitor/PyMongo-Enabled_Scripts/temp_csvs/CO2_{container_no}.csv')
        case 'O2_Con':
            O2_df = collection_df[['Date_Time', 'O2_Con']]
            O2_df.to_csv(f'/home/dan/CompostMonitor_git/Compost-Monitor/PyMongo-Enabled_Scripts/temp_csvs/O2_{container_no}.csv')
        case 'BME_Humidity':
            Hum_df = collection_df[['Date_Time', 'BME_Humidity']]
            Hum_df.to_csv(f'/home/dan/CompostMonitor_git/Compost-Monitor/PyMongo-Enabled_Scripts/temp_csvs/Humidity_{container_no}.csv')
        case 'BME_Pressure':
            Pressure_df = collection_df[['Date_Time', 'BME_Pressure']]
            Pressure_df.to_csv(f'/home/dan/CompostMonitor_git/Compost-Monitor/PyMongo-Enabled_Scripts/temp_csvs/Pressure_{container_no}.csv')
        case 'BME_Temp':
            Temp_df = collection_df[['Date_Time', 'BME_Temp']]
            Temp_df.to_csv(f'/home/dan/CompostMonitor_git/Compost-Monitor/PyMongo-Enabled_Scripts/temp_csvs/Temp_{container_no}.csv')
        case 'Methane_Con':
            Methane_df = collection_df[['Date_Time', 'Methane_Con']]
            Methane_df.to_csv(f'/home/dan/CompostMonitor_git/Compost-Monitor/PyMongo-Enabled_Scripts/temp_csvs/Methane_{container_no}.csv')            
        case _:
            print(f'{sensor} is not a valid sensor name. Check your sensorNames variable.')

if __name__ == '__main__':

    mainStart = datetime.datetime.now()
    with mp.Manager() as manager:
        
        sensorNames     =  'Methane_Con' #['TVOC_Con', 'CO2_Con', 'O2_Con', 'BME_Humidity', 'BME_Pressure', 'BME_Temp', 'Methane_Con']

        processes = []

        # for container_no in range(1, 2):
        for sensor_index, sensor in enumerate(sensorNames):
            process = mp.Process(target = pull_data, args = (1, sensor,))
            processes.append(process)
        
        for process_index, process in enumerate(processes):
            process.start()
            print(f'Pull_data process {process_index} started...')
        
        for process_index, process in enumerate(processes):
            process.join()
            print(f'Pull_data process {process_index} joined...')

    mainEnd = datetime.datetime.now()
    mainTotalTime = (mainEnd - mainStart).total_seconds()
    print(f'if __name__ == "__main__" block executed in {mainTotalTime} seconds.\n')