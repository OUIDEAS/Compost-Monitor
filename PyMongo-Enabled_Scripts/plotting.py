import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pymongo
import multiprocessing as mp
import pandas
import time


client = pymongo.MongoClient("mongodb://100.110.90.28/")
db = client['CompostMonitor']
collection = db['Overall']

def pull_data(container_no, sensor):
    data = collection.find({
                            'Container_No': str(container_no),
                            sensor: {'$exists': 'True'}
                            }).sort("_id", pymongo.ASCENDING).limit(1500)
    collection_df = pandas.DataFrame(data)

    match sensor:
        case 'TVOC_Con':
            TVOC_Data[container_no - 1]     = collection_df.TVOC_Con
            TVOC_Dates[container_no - 1]    = collection_df.Date_Time
        case 'CO2_Con':
            CO2_Data[container_no - 1]      = collection_df.CO2_Con
            CO2_Dates[container_no - 1]     = collection_df.Date_Time
        case 'O2_Con':
            O2_Data[container_no - 1]       = collection_df.O2_Con
            O2_Dates[container_no - 1]      = collection_df.Date_Time
        case 'BME_Humidity':
            Humidity_Data[container_no - 1] = collection_df.BME_Humidity
            BME_Dates[container_no - 1]     = collection_df.Date_Time
        case 'BME_Pressure':
            Pressure_Data[container_no - 1] = collection_df.BME_Pressure
        case 'BME_Temp':
            Temp_Data[container_no - 1]     = collection_df.BME_Temp
        case 'Methane_Con':
            Methane_Data[container_no - 1]  = collection_df.Methane_Con
            Methane_Dates[container_no - 1] = collection_df.Date_Time
        case _:
            print(f'{sensor} is not a valid sensor name. Check your sensorNames variable.')

degree_sign = u'\N{DEGREE SIGN}'

def create_plots(sensorNames):
    for container_no in range(1,5):
        figures = []
        for sensor in sensorNames:
            fig = plt.figure()
            figures.append(fig)
            match sensor:
                case 'TVOC_Con':
                    plt.plot(TVOC_Dates[container_no - 1],    TVOC_Data[container_no - 1])
                    plt.xlabel('Time')
                    plt.ylabel('TVOC Concentration (ppb)')
                    plt.legend()
                    x_locator =ticker.MaxNLocator(10)
                    y_locator =ticker.MaxNLocator(10)
                    plt.gca().xaxis.set_major_locator(x_locator)
                    plt.gca().yaxis.set_major_locator(y_locator)
                    plt.title('TVOC Concentration versus Time')
                case 'CO2_Con':
                    plt.plot(CO2_Dates[container_no - 1],     CO2_Data[container_no - 1])
                    plt.xlabel('Time')
                    plt.ylabel('CO2 Concentration (ppm)')
                    plt.legend()
                    x_locator =ticker.MaxNLocator(10)
                    y_locator =ticker.MaxNLocator(10)
                    plt.gca().xaxis.set_major_locator(x_locator)
                    plt.gca().yaxis.set_major_locator(y_locator)
                    plt.title('CO2 Concentration versus Time')
                case 'O2_Con':
                    plt.plot(O2_Dates[container_no - 1],      O2_Data[container_no - 1])
                    plt.xlabel('Time')
                    plt.ylabel('O2 Concentration (%)')
                    plt.legend()
                    x_locator =ticker.MaxNLocator(10)
                    y_locator =ticker.MaxNLocator(10)
                    plt.gca().xaxis.set_major_locator(x_locator)
                    plt.gca().yaxis.set_major_locator(y_locator)
                    plt.title('O2 Concentration versus Time')
                case 'BME_Humidity':
                    plt.plot(BME_Dates[container_no - 1],     Humidity_Data[container_no - 1])
                    plt.xlabel('Time')
                    plt.ylabel('Relative Humidity')
                    plt.legend()
                    x_locator =ticker.MaxNLocator(10)
                    y_locator =ticker.MaxNLocator(10)
                    plt.gca().xaxis.set_major_locator(x_locator)
                    plt.gca().yaxis.set_major_locator(y_locator)
                    plt.title('Relative Humidity versus Time')
                case 'BME_Temp':
                    plt.plot(BME_Dates[container_no - 1],     Temp_Data[container_no - 1])
                    plt.xlabel('Time')
                    plt.ylabel(f'Temperature ({degree_sign}C)')
                    plt.legend()
                    x_locator =ticker.MaxNLocator(10)
                    y_locator =ticker.MaxNLocator(10)
                    plt.gca().xaxis.set_major_locator(x_locator)
                    plt.gca().yaxis.set_major_locator(y_locator)
                    plt.title('Temperature versus Time')
                case 'BME_Pressure':
                    plt.plot(BME_Dates[container_no - 1],     Pressure_Data[container_no - 1])
                    plt.xlabel('Time')
                    plt.ylabel('Pressure (Pa)')
                    plt.legend()
                    x_locator =ticker.MaxNLocator(10)
                    y_locator =ticker.MaxNLocator(10)
                    plt.gca().xaxis.set_major_locator(x_locator)
                    plt.gca().yaxis.set_major_locator(y_locator)
                    plt.title('Pressure versus Time')
                case 'Methane_Con':
                    plt.plot(Methane_Dates[container_no - 1], Methane_Data[container_no - 1])
                    plt.xlabel('Time')
                    plt.ylabel('Methane Concentration (%)')
                    plt.legend()
                    x_locator =ticker.MaxNLocator(10)
                    y_locator =ticker.MaxNLocator(10)
                    plt.gca().xaxis.set_major_locator(x_locator)
                    plt.gca().yaxis.set_major_locator(y_locator)
                    plt.title('Methane Concentration versus Time')
                case _:
                    print(f'something has gone wrong in function "plot_data" attempting to plot {sensor} in container {container_no}. Check your variables.')
    for figure in figures:
        figure.show()



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
            for sensor_index, sensor in enumerate(sensorNames):
                process = mp.Process(target = pull_data, args = (container_no, sensor,))
                processes.append(process)
        
        for process_index, process in enumerate(processes):
            process.start()
            print(f'Pull_data process {process_index} started...')
        
        for process_index, process in enumerate(processes):
            process.join()
            print(f'Pull_data process {process_index} joined...')
        
        processes = []
        
        for sensor_index, sensor in enumerate(sensorNames):
            process = mp.Process(target = create_plots, args = (sensorNames,))
            processes.append(process)
        
        for process_index, process in enumerate(processes):
            process.start()
            print(f'Create_plots process {process_index} started...')
        
        # for process_index, process in enumerate(processes):
        #     process.join()
        #     print(f'Create_plots process {process_index} joined...')