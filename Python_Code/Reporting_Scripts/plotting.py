import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pymongo
import multiprocessing as mp
import pandas
import time
import matplotlib.dates as mdates
import pathlib
import argparse
import numpy as np
import datetime

client = pymongo.MongoClient("mongodb://100.110.90.28/")
db = client['CompostMonitor']
collection = db['Overall']

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sensor')
parser.add_argument('-n', '--number', default = 'All')
parser.add_argument('-c', '--containernumber', default = 'All')
parser.add_argument('-t', '--saveSheet', default = 0)
args = parser.parse_args()

def emptycells(data):                       #Determines whether empty cells exist within the data array passed to the 
    emptycells = data.isnull().any(axis=1)  #function, returns the data array with empty cells removed.
    emptycells = [index for index, value in enumerate(emptycells) if value == True]
    print(emptycells, type(emptycells))
    data = data.drop(emptycells)
    return data

def deleteExtras(data, count):              #Deletes rows from the array that are missing critical data and returns the array.
    print('data len before:', len(data))
    if (count != 0):
        for i in range(count):
            data.pop(len(data)-1)
    print('data len after:', len(data))
    return data

def pull_data(container_no, sensor):        #Pulls data from the MongoDB collection. Takes cointainer number and sensor name 
    if isinstance(args.number, int):        #as arguments, pulls matching documents
        limit = args.number
    else:
        limit = 10**9
    data = collection.find({
                            '$and':[
                                    {'Container_No': str(container_no)},
                                    {sensor: {'$exists': 'True'}},
                                    {'Date_Time': {'$exists': 'True'}},
                                    {'Date_Time': {'$gt': datetime.datetime(2022, 1, 1, 0, 0, 1)}}]
                                                                          }).sort("Date_Time", pymongo.DESCENDING).limit(limit)
    collection_df = pandas.DataFrame(data)

    match sensor:
        case 'TVOC_Con':
            # collection_df                   = emptycells(collection_df)
            TVOC_Data[container_no - 1]     = collection_df.TVOC_Con
            TVOC_Data[container_no - 1]     = [item.replace('loopin""','') for item in TVOC_Data[container_no - 1]]
            TVOC_Data[container_no - 1]     = [value for value in TVOC_Data[container_no - 1] if value != '' and value != None]
            TVOC_Data[container_no - 1]     = [float(value) for value in TVOC_Data[container_no - 1]]
            TVOC_Dates[container_no - 1]    = collection_df.Date_Time
            print(len(TVOC_Dates[container_no - 1]), len(TVOC_Data[container_no - 1]))
            diff = len(TVOC_Dates[container_no - 1]) - len(TVOC_Data[container_no - 1])
            try:
                deleteExtras(TVOC_Dates[container_no - 1], diff)
            except:
                deleteExtras(TVOC_Data[container_no - 1], diff)
        case 'CO2_Con':
            # collection_df                   = emptycells(collection_df)
            CO2_Data[container_no - 1]      = collection_df.CO2_Con
            CO2_Data[container_no - 1]      = [item.replace('U', '').replace('V', '').replace('*','') for item in CO2_Data[container_no - 1]]
            CO2_Data[container_no - 1]      = [value for value in CO2_Data[container_no - 1] if value != '' and value != None]
            CO2_Data[container_no - 1]      = [float(value) for value in CO2_Data[container_no - 1]]
            CO2_Dates[container_no - 1]     = collection_df.Date_Time
            print(container_no, len(CO2_Dates[container_no - 1]) - len(CO2_Data[container_no - 1]))
            diff = len(CO2_Dates[container_no - 1]) - len(CO2_Data[container_no - 1])
            if (diff > 0):
                CO2_Dates[container_no - 1]     = deleteExtras(CO2_Dates[container_no - 1], diff)
            elif (diff < 0):
                CO2_Data[container_no - 1]      = deleteExtras(CO2_Data[container_no - 1], diff)
            if (int(args.saveSheet) == 1):
                collection_df.to_excel('/home/dan/Desktop/CO2_Dataframe.xlsx', index = False)
            
        case 'O2_Con':
            O2_Data[container_no - 1]       = collection_df.O2_Con
            print(O2_Data[container_no - 1])
            O2_Data[container_no - 1]       = [float(value) for value in O2_Data[container_no - 1]]
            O2_Dates[container_no - 1]      = collection_df.Date_Time
            diff = len(O2_Dates[container_no - 1]) - len(O2_Data[container_no - 1])
            deleteExtras(O2_Dates[container_no - 1], diff)
        case 'BME_Humidity':
            Humidity_Data[container_no - 1] = collection_df.BME_Humidity
            Humidity_Data[container_no - 1] = [float(value) for value in Humidity_Data[container_no - 1]]
            BME_Dates[container_no - 1]     = collection_df.Date_Time
            diff = len(BME_Dates[container_no - 1]) - len(Humidity_Data[container_no - 1])
            deleteExtras(BME_Dates[container_no - 1], diff)
        case 'BME_Pressure':
            Pressure_Data[container_no - 1] = collection_df.BME_Pressure
            Pressure_Data[container_no - 1] = [float(value) for value in Pressure_Data[container_no - 1]]
            BME_Dates[container_no - 1]     = collection_df.Date_Time
            diff = len(BME_Dates[container_no - 1]) - len(Pressure_Data[container_no - 1])
            deleteExtras(BME_Dates[container_no - 1], diff)
        case 'BME_Temp':
            Temp_Data[container_no - 1]     = collection_df.BME_Temp
            Temp_Data[container_no - 1]     = [float(value) for value in Temp_Data[container_no - 1]]
            BME_Dates[container_no - 1]     = collection_df.Date_Time
            diff = len(BME_Dates[container_no - 1]) - len(Temp_Data[container_no - 1])
            deleteExtras(BME_Dates[container_no - 1], diff)
        case 'Methane_Con':
            Methane_Data[container_no - 1]  = collection_df.Methane_Con
            Methane_Data[container_no - 1]  = [float(value) for value in Methane_Data[container_no - 1]]
            Methane_Dates[container_no - 1] = collection_df.Date_Time
            diff = len(Methane_Dates[container_no - 1]) - len(Methane_Data[container_no - 1])
            deleteExtras(Methane_Dates[container_no - 1], diff)
            for index, date in enumerate(Methane_Dates[container_no - 1]):
                if '1970' in str(date):
                    print(f'the 1970 date is in index {index} of Methane_Data')
            # print(Methane_Data[container_no - 1])
            # input()
            print('Methane Dates:', Methane_Dates[container_no - 1])
            input()
        case _:
            print(f'{sensor} is not a valid sensor name. Check your sensorNames variable.')

degree_sign = u'\N{DEGREE SIGN}'

figures = []


def plots(data_sets, title, xaxistitle, yaxistitle, filename):  #Takes data sets, plot title, x- and y-axis titles, and a 
    fig = plt.figure(figsize=(16, 9))                           #filepath. Output is a figure saved in the given path.
    ax = plt.gca()

    if isinstance(data_sets, list):
        for data_set in data_sets:
            x = data_set[0]
            y = data_set[1]
            legend_entry = data_set[2]
            # print(x, y)
            x = [value for value in x if value != None and value != '']
            y = [value for value in y if value != None and value != '']
            
            plt.scatter(x, y, label=legend_entry, alpha = 0.9)
    else:
        x = data_sets[0]
        y = data_sets[1]
        legend_entry = data_sets[2]
        
        plt.scatter(x, y, label=legend_entry)
    
    plt.title(title)
    plt.xlabel(xaxistitle)
    plt.ylabel(yaxistitle)

    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=10))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(10))
    plt.xticks(rotation=45)
    
    plt.legend(loc = 'upper right', bbox_to_anchor = (1.23, 1))
    plt.savefig(filename, bbox_inches = 'tight')

if __name__ == '__main__':


    with mp.Manager() as manager:
        TVOC_Data       =   manager.list([0, 0, 0, 0])
        CO2_Data        =   manager.list([0, 0, 0, 0])
        O2_Data         =   manager.list([0, 0, 0, 0])
        Humidity_Data   =   manager.list([0, 0, 0, 0])
        Temp_Data       =   manager.list([0, 0, 0, 0])
        Pressure_Data   =   manager.list([0, 0, 0, 0])
        Methane_Data    =   manager.list([0, 0, 0, 0])
        TVOC_Dates      =   manager.list([0, 0, 0, 0])
        CO2_Dates       =   manager.list([0, 0, 0, 0])
        O2_Dates        =   manager.list([0, 0, 0, 0])
        BME_Dates       =   manager.list([0, 0, 0, 0])
        Methane_Dates   =   manager.list([0, 0, 0, 0])

        
        sensorNames     =   ['TVOC_Con', 'CO2_Con', 'O2_Con', 'BME_Humidity', 'BME_Pressure', 'BME_Temp', 'Methane_Con']

        processes = []

        for container_no in range(1, 5):
            process = mp.Process(target = pull_data, args = (container_no, args.sensor))
            processes.append(process)
        
        for process_index, process in enumerate(processes):
            process.start()
            print(f'Pull_data process {process_index} started...')
        
        for process_index, process in enumerate(processes):
            process.join()
            print(f'Pull_data process {process_index} joined...')

        directoryBase = f"/home/dan/Desktop/figures/{time.strftime('%m-%d-%Y')}"

        pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)


        if (args.sensor == 'TVOC_Con'):
            data_sets = []
            data_sets.append((TVOC_Dates[0], TVOC_Data[0], 'TVOC - Container 1'))
            data_sets.append((TVOC_Dates[1], TVOC_Data[1], 'TVOC - Container 2'))
            data_sets.append((TVOC_Dates[2], TVOC_Data[2], 'TVOC - Container 3'))
            data_sets.append((TVOC_Dates[3], TVOC_Data[3], 'TVOC - Container 4'))
            # plots(data_sets[0], "TVOC versus Time - Container 1", "Time", "TVOC (ppb)", f"{directoryBase}/TVOC_1.png") 
            # plots(data_sets[1], "TVOC versus Time - Container 2", "Time", "TVOC (ppb)", f"{directoryBase}/TVOC_2.png")
            # plots(data_sets[2], "TVOC versus Time - Container 3", "Time", "TVOC (ppb)", f"{directoryBase}/TVOC_3.png")
            # plots(data_sets[3], "TVOC versus Time - Container 4", "Time", "TVOC (ppb)", f"{directoryBase}/TVOC_4.png")
            plots(data_sets, "TVOC versus Time", "Time", "TVOC (ppb)", f"{directoryBase}/TVOC_{args.number}.png")
        elif(args.sensor == 'CO2_Con'):
            data_sets = []
            data_sets.append((CO2_Dates[0], CO2_Data[0], 'CO2 Con. - Container 1'))
            data_sets.append((CO2_Dates[1], CO2_Data[1], 'CO2 Con. - Container 2'))
            data_sets.append((CO2_Dates[2], CO2_Data[2], 'CO2 Con. - Container 3'))
            data_sets.append((CO2_Dates[3], CO2_Data[3], 'CO2 Con. - Container 4'))
            # plots(data_sets[0], "CO2 Concentration versus Time - Container 1", "Time", "CO2 Concentration (ppm)", f"{directoryBase}/CO2_1.png")
            # plots(data_sets[1], "CO2 Concentration versus Time - Container 2", "Time", "CO2 Concentration (ppm)", f"{directoryBase}/CO2_2.png")
            # plots(data_sets[2], "CO2 Concentration versus Time - Container 3", "Time", "CO2 Concentration (ppm)", f"{directoryBase}/CO2_3.png")
            # plots(data_sets[3], "CO2 Concentration versus Time - Container 4", "Time", "CO2 Concentration (ppm)", f"{directoryBase}/CO2_4.png")
            plots(data_sets, "CO2 Concentration versus Time", 'Time', 'CO2 Concentration (ppm)', f"{directoryBase}/CO2_{args.number}.png")
        elif(args.sensor == 'O2_Con'):
            data_sets = []
            data_sets.append((O2_Dates[0], O2_Data[0], 'O2 Con. - Container 1'))
            data_sets.append((O2_Dates[1], O2_Data[1], 'O2 Con. - Container 2'))
            data_sets.append((O2_Dates[2], O2_Data[2], 'O2 Con. - Container 3'))
            data_sets.append((O2_Dates[3], O2_Data[3], 'O2 Con. - Container 4'))
            # plots(data_sets[0], "O2 Concentration versus Time - Container 1", "Time", "O2 Concentration (%)", f"{directoryBase}/O2_1.png")
            # plots(data_sets[1], "O2 Concentration versus Time - Container 2", "Time", "O2 Concentration (%)", f"{directoryBase}/O2_2.png")
            # plots(data_sets[2], "O2 Concentration versus Time - Container 3", "Time", "O2 Concentration (%)", f"{directoryBase}/O2_3.png")
            # plots(data_sets[3], "O2 Concentration versus Time - Container 4", "Time", "O2 Concentration (%)", f"{directoryBase}/O2_4.png")
            plots(data_sets, "O2 Concentration versus Time", 'Time', 'O2 Concentration (%)', f"{directoryBase}/O2_{args.number}.png")
        elif(args.sensor == 'BME_Humidity'):
            data_sets = []
            data_sets.append((BME_Dates[0], Humidity_Data[0], 'Relative Humidity - Container 1'))
            data_sets.append((BME_Dates[1], Humidity_Data[1], 'Relative Humidity - Container 2'))
            data_sets.append((BME_Dates[2], Humidity_Data[2], 'Relative Humidity - Container 3'))
            data_sets.append((BME_Dates[3], Humidity_Data[3], 'Relative Humidity - Container 4'))
            # plots(data_sets[0], "Relative Humidity versus Time - Container 1", "Time", "Relative Humidity (%)", f"{directoryBase}/Hum_1.png")
            # plots(data_sets[1], "Relative Humidity versus Time - Container 2", "Time", "Relative Humidity (%)", f"{directoryBase}/Hum_2.png")
            # plots(data_sets[2], "Relative Humidity versus Time - Container 3", "Time", "Relative Humidity (%)", f"{directoryBase}/Hum_3.png")
            # plots(data_sets[3], "Relative Humidity versus Time - Container 4", "Time", "Relative Humidity (%)", f"{directoryBase}/Hum_4.png")
            plots(data_sets, "Relative Humidity versus Time", 'Time', 'Relative Humidity (%)', f"{directoryBase}/Hum_{args.number}.png")
        elif(args.sensor == 'BME_Temp'):
            data_sets = []
            data_sets.append((BME_Dates[0], Temp_Data[0], 'Temperature - Container 1'))
            data_sets.append((BME_Dates[1], Temp_Data[1], 'Temperature - Container 2'))
            data_sets.append((BME_Dates[2], Temp_Data[2], 'Temperature - Container 3'))
            data_sets.append((BME_Dates[3], Temp_Data[3], 'Temperature - Container 4'))
            # plots(data_sets[0], "Temperature versus Time - Container 1", "Time", f"Temperature ({degree_sign}C)", f"{directoryBase}/Temp_1.png")
            # plots(data_sets[1], "Temperature versus Time - Container 2", "Time", f"Temperature ({degree_sign}C)", f"{directoryBase}/Temp_2.png")
            # plots(data_sets[2], "Temperature versus Time - Container 3", "Time", f"Temperature ({degree_sign}C)", f"{directoryBase}/Temp_3.png")
            # plots(data_sets[3], "Temperature versus Time - Container 4", "Time", f"Temperature ({degree_sign}C)", f"{directoryBase}/Temp_4.png")
            plots(data_sets, "Temperature versus Time", 'Time', f"Temperature ({degree_sign}C)", f"{directoryBase}/Temp_{args.number}.png")
        elif(args.sensor == 'BME_Pressure'):
            data_sets = []
            data_sets.append((BME_Dates[0], Pressure_Data[0], 'Pressure - Container 1'))
            data_sets.append((BME_Dates[1], Pressure_Data[1], 'Pressure - Container 2'))
            data_sets.append((BME_Dates[2], Pressure_Data[2], 'Pressure - Container 3'))
            data_sets.append((BME_Dates[3], Pressure_Data[3], 'Pressure - Container 4'))
            # plots(data_sets[0], "Pressure versus Time - Container 1", "Time", "Pressure (Pa)", f"{directoryBase}/Pressure_1.png")
            # plots(data_sets[1], "Pressure versus Time - Container 2", "Time", "Pressure (Pa)", f"{directoryBase}/Pressure_2.png")
            # plots(data_sets[2], "Pressure versus Time - Container 3", "Time", "Pressure (Pa)", f"{directoryBase}/Pressure_3.png")
            # plots(data_sets[3], "Pressure versus Time - Container 4", "Time", "Pressure (Pa)", f"{directoryBase}/Pressure_4.png")
            plots(data_sets, "Pressure versus Time", 'Time', "Pressure (Pa)", f"{directoryBase}/Pressure_{args.number}.png")
        elif(args.sensor == 'Methane_Con'):
            data_sets = []
            data_sets.append((Methane_Dates[0], Methane_Data[0], 'Methane Con. - Container 1'))
            data_sets.append((Methane_Dates[1], Methane_Data[1], 'Methane Con. - Container 2'))
            data_sets.append((Methane_Dates[2], Methane_Data[2], 'Methane Con. - Container 3'))
            data_sets.append((Methane_Dates[3], Methane_Data[3], 'Methane Con. - Container 4'))
            # plots(data_sets[0], "Methane Concentration versus Time - Container 1", "Time", "Methane Concentration (% Volume)", f"{directoryBase}/Methane_1.png")
            # plots(data_sets[1], "Methane Concentration versus Time - Container 2", "Time", "Methane Concentration (% Volume)", f"{directoryBase}/Methane_1.png")
            # plots(data_sets[2], "Methane Concentration versus Time - Container 3", "Time", "Methane Concentration (% Volume)", f"{directoryBase}/Methane_1.png")
            # plots(data_sets[3], "Methane Concentration versus Time - Container 4", "Time", "Methane Concentration (% Volume)", f"{directoryBase}/Methane_1.png")
            plots(data_sets, "Methane Concentration versus Time", 'Time', 'Methane Concentration (% Volume)', f"{directoryBase}/Methane_{args.number}.png")
        # plt.show()
