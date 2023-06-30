import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pymongo
import multiprocessing as mp
import pandas
import time
import matplotlib.dates as mdates
import pathlib


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
            TVOC_Data[container_no - 1]     = [float(value) for value in TVOC_Data[container_no - 1]]
            TVOC_Dates[container_no - 1]    = collection_df.Date_Time
        case 'CO2_Con':
            CO2_Data[container_no - 1]      = collection_df.CO2_Con
            CO2_Data[container_no - 1]      = [float(value) for value in CO2_Data[container_no - 1]]
            CO2_Dates[container_no - 1]     = collection_df.Date_Time
        case 'O2_Con':
            O2_Data[container_no - 1]       = collection_df.O2_Con
            O2_Data[container_no - 1]       = [float(value) for value in O2_Data[container_no - 1]]
            O2_Dates[container_no - 1]      = collection_df.Date_Time
        case 'BME_Humidity':
            Humidity_Data[container_no - 1] = collection_df.BME_Humidity
            Humidity_Data[container_no - 1] = [float(value) for value in Humidity_Data[container_no - 1]]
            BME_Dates[container_no - 1]     = collection_df.Date_Time
        case 'BME_Pressure':
            Pressure_Data[container_no - 1] = collection_df.BME_Pressure
            Pressure_Data[container_no - 1] = [float(value) for value in Pressure_Data[container_no - 1]]
        case 'BME_Temp':
            Temp_Data[container_no - 1]     = collection_df.BME_Temp
            Temp_Data[container_no - 1]     = [float(value) for value in Temp_Data[container_no - 1]]
        case 'Methane_Con':
            Methane_Data[container_no - 1]  = collection_df.Methane_Con
            Methane_Data[container_no - 1]  = [float(value) for value in Methane_Data[container_no - 1]]
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

figures = []
def plots(x, y, title, xaxistitle, yaxistitle, filename):
    fig = plt.figure(figsize= (8,8))  # Create a new figure object
    plt.scatter(x, y)
    plt.title(title)
    plt.xlabel(xaxistitle)  # Set x-axis title
    plt.ylabel(yaxistitle)  # Set y-axis title

    # Set the number of tick marks on each axis
    # plt.xticks(ticks=numticks)
    # plt.yticks(ticks=numticks)
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=10))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(10))
    plt.xticks(rotation=45)

    plt.savefig(filename)

    # plt.show()


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

        directoryBase = "/home/dan/Desktop/figures/06-30-2023"

        pathlib.Path(directoryBase).mkdir(parents=True, exist_ok=True)

        plots(TVOC_Dates[0], TVOC_Data[0], "TVOC versus Time - Container 1", "Time", "TVOC (ppb)", "/home/dan/Desktop/figures/06-30-2023/TVOC_1.png") 
        plots(TVOC_Dates[1], TVOC_Data[1], "TVOC versus Time - Container 2", "Time", "TVOC (ppb)", "/home/dan/Desktop/figures/06-30-2023/TVOC_2.png")
        plots(TVOC_Dates[2], TVOC_Data[2], "TVOC versus Time - Container 3", "Time", "TVOC (ppb)", "/home/dan/Desktop/figures/06-30-2023/TVOC_3.png")
        plots(TVOC_Dates[3], TVOC_Data[3], "TVOC versus Time - Container 4", "Time", "TVOC (ppb)", "/home/dan/Desktop/figures/06-30-2023/TVOC_4.png")
        plots(CO2_Dates[0], CO2_Data[0], "CO2 Concentration versus Time - Container 1", "Time", "CO2 Concentration (ppm)", "/home/dan/Desktop/figures/06-30-2023/CO2_1.png")
        plots(CO2_Dates[1], CO2_Data[1], "CO2 Concentration versus Time - Container 2", "Time", "CO2 Concentration (ppm)", "/home/dan/Desktop/figures/06-30-2023/CO2_2.png")
        plots(CO2_Dates[2], CO2_Data[2], "CO2 Concentration versus Time - Container 3", "Time", "CO2 Concentration (ppm)", "/home/dan/Desktop/figures/06-30-2023/CO2_3.png")
        plots(CO2_Dates[3], CO2_Data[3], "CO2 Concentration versus Time - Container 4", "Time", "CO2 Concentration (ppm)", "/home/dan/Desktop/figures/06-30-2023/CO2_4.png")
        plots(O2_Dates[0], O2_Data[0], "O2 Concentration versus Time - Container 1", "Time", "O2 Concentration (%)", "/home/dan/Desktop/figures/06-30-2023/O2_1.png")
        plots(O2_Dates[1], O2_Data[1], "O2 Concentration versus Time - Container 2", "Time", "O2 Concentration (%)", "/home/dan/Desktop/figures/06-30-2023/O2_2.png")
        plots(O2_Dates[2], O2_Data[2], "O2 Concentration versus Time - Container 3", "Time", "O2 Concentration (%)", "/home/dan/Desktop/figures/06-30-2023/O2_3.png")
        plots(O2_Dates[3], O2_Data[3], "O2 Concentration versus Time - Container 4", "Time", "O2 Concentration (%)", "/home/dan/Desktop/figures/06-30-2023/O2_4.png")
        plots(BME_Dates[0], Humidity_Data[0], "Relative Humidity versus Time - Container 1", "Time", "Relative Humidity (%)", "/home/dan/Desktop/figures/06-30-2023/Hum_1.png")
        plots(BME_Dates[1], Humidity_Data[1], "Relative Humidity versus Time - Container 2", "Time", "Relative Humidity (%)", "/home/dan/Desktop/figures/06-30-2023/Hum_2.png")
        plots(BME_Dates[2], Humidity_Data[2], "Relative Humidity versus Time - Container 3", "Time", "Relative Humidity (%)", "/home/dan/Desktop/figures/06-30-2023/Hum_3.png")
        plots(BME_Dates[3], Humidity_Data[3], "Relative Humidity versus Time - Container 4", "Time", "Relative Humidity (%)", "/home/dan/Desktop/figures/06-30-2023/Hum_4.png")
        plots(BME_Dates[0], Temp_Data[0], "Temperature versus Time - Container 1", "Time", f"Temperature ({degree_sign}C)", "/home/dan/Desktop/figures/06-30-2023/Temp_1.png")
        plots(BME_Dates[1], Temp_Data[1], "Temperature versus Time - Container 2", "Time", f"Temperature ({degree_sign}C)", "/home/dan/Desktop/figures/06-30-2023/Temp_2.png")
        plots(BME_Dates[2], Temp_Data[2], "Temperature versus Time - Container 3", "Time", f"Temperature ({degree_sign}C)", "/home/dan/Desktop/figures/06-30-2023/Temp_3.png")
        plots(BME_Dates[3], Temp_Data[3], "Temperature versus Time - Container 4", "Time", f"Temperature ({degree_sign}C)", "/home/dan/Desktop/figures/06-30-2023/Temp_4.png")
        plots(BME_Dates[0], Pressure_Data[0], "Pressure versus Time - Container 1", "Time", "Pressure (Pa)", "/home/dan/Desktop/figures/06-30-2023/Pressure_1.png")
        plots(BME_Dates[1], Pressure_Data[1], "Pressure versus Time - Container 2", "Time", "Pressure (Pa)", "/home/dan/Desktop/figures/06-30-2023/Pressure_2.png")
        plots(BME_Dates[2], Pressure_Data[2], "Pressure versus Time - Container 3", "Time", "Pressure (Pa)", "/home/dan/Desktop/figures/06-30-2023/Pressure_3.png")
        plots(BME_Dates[3], Pressure_Data[3], "Pressure versus Time - Container 4", "Time", "Pressure (Pa)", "/home/dan/Desktop/figures/06-30-2023/Pressure_4.png")
        plots(Methane_Dates[0], Methane_Data[0], "Methane Concentration versus Time - Container 1", "Time", "Methane Concentration (% Volume)", "/home/dan/Desktop/figures/06-30-2023/Methane_1.png")
        plots(Methane_Dates[1], Methane_Data[1], "Methane Concentration versus Time - Container 2", "Time", "Methane Concentration (% Volume)", "/home/dan/Desktop/figures/06-30-2023/Methane_1.png")
        plots(Methane_Dates[2], Methane_Data[2], "Methane Concentration versus Time - Container 3", "Time", "Methane Concentration (% Volume)", "/home/dan/Desktop/figures/06-30-2023/Methane_1.png")
        plots(Methane_Dates[3], Methane_Data[3], "Methane Concentration versus Time - Container 4", "Time", "Methane Concentration (% Volume)", "/home/dan/Desktop/figures/06-30-2023/Methane_1.png")

        plt.show()

        "/home/dan/Desktop/figures/06-30-2023/TVOC_1.png"

        # processes = []
        
        # for sensor_index, sensor in enumerate(sensorNames):
        #     process = mp.Process(target = create_plots, args = (sensorNames,))
        #     processes.append(process)
        
        # for process_index, process in enumerate(processes):
        #     process.start()
        #     print(f'Create_plots process {process_index} started...')
        
        # for process_index, process in enumerate(processes):
        #     process.join()
        #     print(f'Create_plots process {process_index} joined...')


