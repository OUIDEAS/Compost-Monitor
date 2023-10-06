# TODO: add argument for date range.
''' 1. pull data
    2. calculate mean, std. dev?
    3. statistical test w/ 95% confidence
    4. conclusion'''

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
parser.add_argument('-s', '--sensor', required = True)
parser.add_argument('-n', '--number', default = 'All')
parser.add_argument('-c', '--containernumber', default = 'All')
parser.add_argument('-t', '--saveSheet', default = 0)
parser.add_argument('-d', '--dates', nargs = '+', required = True)
args = parser.parse_args()


if __name__ == '__main__':

    dates = args.dates 
    for i, date in enumerate(dates):
        print("Pre-conversion data type:", type(dates[i]))
        dates[i] = datetime.datetime.strptime(date, '%m/%d/%Y')
        print("Post-conversion data type:", type(dates[i]))

    if (len(dates)>4):
        print('Too many date ranges. This script currently only supports 2. No more, no less.')
    num_ranges = len(dates)/2
    print('There are ', num_ranges, ' ranges per your input.')
    daterange_1 = dates[0:1]
    daterange_2 = dates[2:3]
    


def emptycells(data):
    emptycells = data.isnull().any(axis=1)
    emptycells = [index for index, value in enumerate(emptycells) if value == True]
    print(emptycells, type(emptycells))
    data = data.drop(emptycells)
    return data

def deleteExtras(data, count):
    print('data len before:', len(data))
    if (count != 0):
        for i in range(count):
            data.pop(len(data)-1)
    print('data len after:', len(data))
    return data

def pull_data(container_no, sensor, datelist):
    if isinstance(args.number, int):
        limit = args.number
    else:
        limit = 10**9
    data = collection.find({
                            '$and':[
                                    {'Container_No': str(container_no)},
                                    {sensor: {'$exists': 'True'}},
                                    {'Date_Time': {'$exists': 'True'}},
                                    {'Date_Time': {'$gt': datelist[0]}},
                                    {'Date_Time': {'$lt': datelist[1]}}]
                                                                          }).sort("Date_Time", pymongo.DESCENDING).limit(limit)
    collection_df = pandas.DataFrame(data)

    match sensor:
        case 'TVOC_Con':

            TVOC_Data.append(collection_df.Date_Time)
            TVOC_Data.append(collection_df.TVOC_Con)
            TVOC_Data[len(TVOC_Data)]                   = [item.replace('loopin""','') for item in TVOC_Data[container_no - 1]]
            TVOC_Data[len(TVOC_Data)]                   = [value for value in TVOC_Data[len(TVOC_Data)] if value != '' and value != None]
            TVOC_Data[len(TVOC_Data)]                   = [float(value) for value in TVOC_Data[len(TVOC_Data)]]
            # collection_df                   = emptycells(collection_df)
            # TVOC_Data[container_no - 1]     = collection_df.TVOC_Con
            # TVOC_Data[container_no - 1]     = [item.replace('loopin""','') for item in TVOC_Data[container_no - 1]]
            # TVOC_Data[container_no - 1]     = [value for value in TVOC_Data[container_no - 1] if value != '' and value != None]
            # TVOC_Data[container_no - 1]     = [float(value) for value in TVOC_Data[container_no - 1]]
            # TVOC_Dates[container_no - 1]    = collection_df.Date_Time
            # print(len(TVOC_Dates[container_no - 1]), len(TVOC_Data[container_no - 1]))
            # diff = len(TVOC_Dates[container_no - 1]) - len(TVOC_Data[container_no - 1])
            # try:
            #     deleteExtras(TVOC_Dates[container_no - 1], diff)
            # except:
            #     deleteExtras(TVOC_Data[container_no - 1], diff)
        case 'CO2_Con':
            CO2_Data.append(collection_df.Date_Time)
            CO2_Data.append(collection_df.CO2_Con)
            CO2_Data[len(CO2_Data)]                   = [item.replace('U', '').replace('V', '').replace('*','') for item in CO2_Data[container_no - 1]]
            CO2_Data[len(CO2_Data)]                   = [value for value in CO2_Data[len(CO2_Data)] if value != '' and value != None]
            CO2_Data[len(CO2_Data)]                   = [float(value) for value in CO2_Data[len(CO2_Data)]]
            # collection_df                   = emptycells(collection_df)
            # CO2_Data[container_no - 1]      = collection_df.CO2_Con
            # CO2_Data[container_no - 1]      = [item.replace('U', '').replace('V', '').replace('*','') for item in CO2_Data[container_no - 1]]
            # CO2_Data[container_no - 1]      = [value for value in CO2_Data[container_no - 1] if value != '' and value != None]
            # CO2_Data[container_no - 1]      = [float(value) for value in CO2_Data[container_no - 1]]
            # CO2_Dates[container_no - 1]     = collection_df.Date_Time
            # print(container_no, len(CO2_Dates[container_no - 1]) - len(CO2_Data[container_no - 1]))
            # diff = len(CO2_Dates[container_no - 1]) - len(CO2_Data[container_no - 1])
            # if (diff > 0):
            #     CO2_Dates[container_no - 1]     = deleteExtras(CO2_Dates[container_no - 1], diff)
            # elif (diff < 0):
            #     CO2_Data[container_no - 1]      = deleteExtras(CO2_Data[container_no - 1], diff)
            # if (int(args.saveSheet) == 1):
            #     collection_df.to_excel('/home/dan/Desktop/CO2_Dataframe.xlsx', index = False)
            
        case 'O2_Con':
            O2_Data.append(collection_df.Date_Time)
            O2_Data.append(collection_df.O2_Con)
            O2_Data[len(O2_Data)]                     = [float(value) for value in O2_Data[len(O2_Data)]]

            # O2_Data[container_no - 1]       = collection_df.O2_Con
            # print(O2_Data[container_no - 1])
            # O2_Data[container_no - 1]       = [float(value) for value in O2_Data[container_no - 1]]
            # O2_Dates[container_no - 1]      = collection_df.Date_Time
            # diff = len(O2_Dates[container_no - 1]) - len(O2_Data[container_no - 1])
            # deleteExtras(O2_Dates[container_no - 1], diff)
        case 'BME_Humidity':
            Humidity_Data.append(collection_df.Date_Time)
            Humidity_Data.append(collection_df.BME_Humidity)
            Humidity_Data[len(Humidity_Data)] = [float(value) for value in Humidity_Data[len(Humidity_Data)]]
            # Humidity_Data[container_no - 1] = collection_df.BME_Humidity
            # Humidity_Data[container_no - 1] = [float(value) for value in Humidity_Data[container_no - 1]]
            # BME_Dates[container_no - 1]     = collection_df.Date_Time
            # diff = len(BME_Dates[container_no - 1]) - len(Humidity_Data[container_no - 1])
            # deleteExtras(BME_Dates[container_no - 1], diff)
        case 'BME_Pressure':
            Pressure_Data.append(collection_df.Date_Time)
            Pressure_Data.append(collection_df.BME_Pressure)
            Pressure_Data[len(Pressure_Data)] = [float(value) for value in Pressure_Data[len(Pressure_Data)]]
            
            # Pressure_Data[container_no - 1] = collection_df.BME_Pressure
            # Pressure_Data[container_no - 1] = [float(value) for value in Pressure_Data[container_no - 1]]
            # BME_Dates[container_no - 1]     = collection_df.Date_Time
            # diff = len(BME_Dates[container_no - 1]) - len(Pressure_Data[container_no - 1])
            # deleteExtras(BME_Dates[container_no - 1], diff)
        case 'BME_Temp':
            Temp_Data.append(collection_df.Date_Time)
            Temp_Data.append(collection_df.BME_Temp)
            Temp_Data[len(Temp_Data)] = [float(value) for value in Temp_Data[len(Temp_Data)]]
            # Temp_Data[container_no - 1]     = collection_df.BME_Temp
            # Temp_Data[container_no - 1]     = [float(value) for value in Temp_Data[container_no - 1]]
            # BME_Dates[container_no - 1]     = collection_df.Date_Time
            # diff = len(BME_Dates[container_no - 1]) - len(Temp_Data[container_no - 1])
            # deleteExtras(BME_Dates[container_no - 1], diff)
        case 'Methane_Con':
            Methane_Data.append(collection_df.Date_Time)
            Methane_Data.append(collection_df.Methane_Con)
            Methane_Data[len(Methane_Data)] = [float(value) for value in Methane_Data[len(Methane_Data)]]
            # Methane_Data[container_no - 1]  = collection_df.Methane_Con
            # Methane_Data[container_no - 1]  = [float(value) for value in Methane_Data[container_no - 1]]
            # Methane_Dates[container_no - 1] = collection_df.Date_Time
            # diff = len(Methane_Dates[container_no - 1]) - len(Methane_Data[container_no - 1])
            # deleteExtras(Methane_Dates[container_no - 1], diff)
            # for index, date in enumerate(Methane_Dates[container_no - 1]):
            #     if '1970' in str(date):
            #         print(f'the 1970 date is in index {index} of Methane_Data')
            # # print(Methane_Data[container_no - 1])
            # # input()
            # print('Methane Dates:', Methane_Dates[container_no - 1])
            # input()
        case _:
            print(f'{sensor} is not a valid sensor name. Check your sensorNames variable.')

degree_sign = u'\N{DEGREE SIGN}'

figures = []


def plots(data_sets, title, xaxistitle, yaxistitle, filename):
    fig = plt.figure(figsize=(16, 9))
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
        TVOC_Data       =   manager.list([])
        CO2_Data        =   manager.list([])
        O2_Data         =   manager.list([])
        Humidity_Data   =   manager.list([])
        Temp_Data       =   manager.list([])
        Pressure_Data   =   manager.list([])
        Methane_Data    =   manager.list([])
        # TVOC_Dates      =   manager.list([0, 0, 0, 0])
        # CO2_Dates       =   manager.list([0, 0, 0, 0])
        # O2_Dates        =   manager.list([0, 0, 0, 0])
        # BME_Dates       =   manager.list([0, 0, 0, 0])
        # Methane_Dates   =   manager.list([0, 0, 0, 0])
        

        
        sensorNames     =   ['TVOC_Con', 'CO2_Con', 'O2_Con', 'BME_Humidity', 'BME_Pressure', 'BME_Temp', 'Methane_Con']

        processes = []

        for i in range(num_ranges):
            process = mp.Process(target = pull_data, args = (args.containernumber, args.sensor, dates[i*2:i*2+1]))
            process.start()
            print(f'Pull_data process {i} started...')
            process.join()
            print(f'Pull_data process {i} joined...')

        # for process_index, process in enumerate(processes):
            # process.start()
            # print(f'Pull_data process {process_index} started...')
        # 
        # for process_index, process in enumerate(processes):
            # process.join()
            # print(f'Pull_data process {process_index} joined...')

        directoryBase = f"/home/dan/Desktop/figures/{time.strftime('%m-%d-%Y')}"

        pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)
