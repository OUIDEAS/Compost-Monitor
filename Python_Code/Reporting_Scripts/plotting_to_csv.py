import pandas as pd
import pymongo
import multiprocessing as mp
import datetime
import time
import pathlib

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['CompostMonitor']
collection = db['Overall']
directoryBase = r"home/compostmonitor/SuperSecretTestFolder/Compost-Monitor/Python_Code/Reporting_Scripts/Test_CSVs".format(time.strftime("%m-%d-%Y"))
pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
def pull_data(container_no, sensor):
    data = collection.find({
                            'Container_No': str(container_no),
                            sensor: {'$exists': 'True'}
                            }).sort("_id", pymongo.ASCENDING)
    collection_df = pd.DataFrame(data)
    print(collection_df.columns)

    match sensor:
        case 'TVOC_Con':
            TVOC_df = collection_df[['TVOC_Con']]
            TVOC_df.to_csv(f'/home/dan/SuperSecretTestFolder/Compost-Monitor/Python_Code/Reporting_Scripts/Test_CSVs/{time.strftime("%m-%d-%Y")}/TVOC_{container_no}.csv')
        case 'CO2_Con':
            CO2_df = collection_df[['CO2_Con']]
            CO2_df.to_csv(f'/home/dan/SuperSecretTestFolder/Compost-Monitor/Python_Code/Reporting_Scripts/Test_CSVs/CO2_{container_no}.csv')
        case 'O2_Con':
            O2_df = collection_df[['O2_Con']]
            O2_df.to_csv(f'/home/dan/SuperSecretTestFolder/Compost-Monitor/Python_Code/Reporting_Scripts/Test_CSVs/O2_{container_no}.csv')
        case 'BME_Humidity':
            Hum_df = collection_df[['BME_Humidity']]
            Hum_df.to_csv(f'/home/dan/SuperSecretTestFolder/Compost-Monitor/Python_Code/Reporting_Scripts/Test_CSVs/Humidity_{container_no}.csv')
        case 'BME_Pressure':
            Pressure_df = collection_df[['BME_Pressure']]
            Pressure_df.to_csv(f'/home/dan/SuperSecretTestFolder/Compost-Monitor/Python_Code/Reporting_Scripts/Test_CSVs/Pressure_{container_no}.csv')
        case 'BME_Temp':
            Temp_df = collection_df[['BME_Temp']]
            Temp_df.to_csv(f'/home/dan/SuperSecretTestFolder/Compost-Monitor/Python_Code/Reporting_Scripts/Test_CSVs/Temp_{container_no}.csv')
        case 'Methane_Con':
            Methane_df = collection_df[['Methane_Con']]
            Methane_df.to_csv(f'/home/dan/SuperSecretTestFolder/Compost-Monitor/Python_Code/Reporting_Scripts/Test_CSVs/Methane_{container_no}.csv')            
        case _:
            print(f'{sensor} is not a valid sensor name. Check your sensorNames variable.')

if __name__ == '__main__':

    mainStart = datetime.datetime.now()
    with mp.Manager() as manager:
        
        sensorNames     =  ['TVOC_Con', 'CO2_Con', 'O2_Con', 'BME_Humidity', 'BME_Pressure', 'BME_Temp', 'Methane_Con']

        processes = []

        for index in sensorNames:
            for container_no in range(1, 5):
                process = mp.Process(target = pull_data, args = (container_no, index,))
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