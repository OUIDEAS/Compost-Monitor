import multiprocessing
import pandas
import datetime
import tkinter as tk
import pymongo
import numpy as np

startupTime = datetime.datetime.now()

client = pymongo.MongoClient("mongodb://100.110.90.28/")
db = client['CompostMonitor']
collection = db['Overall']

def pull_data(container_no, sensor):
    data = collection.find({
                            'Container_No': str(container_no),
                            sensor: {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1)
    collection_df = pandas.DataFrame(data)
    coll_datetime = collection_df.Date_Time[0]
    lastdate = coll_datetime.to_pydatetime()
    timedelta = datetime.datetime.now() - lastdate

    if (timedelta.total_seconds() < 5.0):
        match sensor:
            case 'TVOC_Con':
                TVOC_markers[container_no - 1]      =   True
                print(f'TVOC_markers changed at index {container_no - 1}\n')
            case 'BME_Humidity':
                BME_markers[container_no - 1]       =   True
                print(f'BME_markers changed at index {container_no - 1}\n')
            case 'CO2_Con':
                CO2_markers[container_no - 1]       =   True
                print(f'CO2_markers changed at index {container_no - 1}\n')
            case 'O2_Con':
                O2_markers[container_no - 1]        =   True
                print(f'O2_markers changed at index {container_no - 1}\n')
            case 'Methane_Con':
                Methane_markers[container_no - 1]   =   True
                print(f'Methane_markers changed at index {container_no - 1}\n')
            case _:
                print(f'{sensor} is not a valid sensor. Check your sensor_names variable.')
    else:
        print(f'{sensor} in {container_no} lastdate: {lastdate}')

def update_square_color(section_index, square_index):
    if my_variables[section_index][square_index].get():
        squares[section_index][square_index].config(bg='green')
    else:
        squares[section_index][square_index].config(bg='red')


if __name__ == '__main__':
    ifStart = datetime.datetime.now()
    processes = []
    joined_processes = []

    with multiprocessing.Manager() as manager:
        TVOC_markers    =   manager.list([False, False, False, False])
        BME_markers     =   manager.list([False, False, False, False])
        CO2_markers     =   manager.list([False, False, False, False])
        O2_markers      =   manager.list([False, False, False, False])
        Methane_markers =   manager.list([False, False, False, False])

        sensor_names    =   ['TVOC_Con', 'BME_Humidity', 'CO2_Con', 'O2_Con', 'Methane_Con']

        for container_no in range(1, 5):
            for sensor_index, sensor in enumerate(sensor_names):
                process = multiprocessing.Process(target=pull_data, args = (container_no, sensor))
                processes.append(process)
        
        for process_index, process in enumerate(processes):
            print(f'Process {process_index} starting...\n')
            process.start()

        for process_index, process in enumerate(processes):
            process.join()
            joined_processes.append(process_index)
            print(f'Process {process_index} joined.\n')

        sensor_markers = manager.list([TVOC_markers, BME_markers, CO2_markers, O2_markers, Methane_markers])
        sensor_markers = [list(sublist) for sublist in sensor_markers]
        print(f'Here are the sensor markers:\n {sensor_markers}\n')
        print(f'Processes in order of joining:\n{joined_processes}\n')
        ifEnd = datetime.datetime.now()
        ifTime = (ifEnd - ifStart).total_seconds()
        print(f"if __name__ = '__main__' block executed in {ifTime} seconds.\n")

    window = tk.Tk()
    window.title("CM Sensor Status")

    # Create variables and squares for each section
    my_variables = []
    squares = []
    variable_names = [
                     ["Con.1 TVOC", "Con.1 BME", "Con.1 CO2", "Con.1 O2", "Con.1 Methane"],
                     ["Con.2 TVOC", "Con.2 BME", "Con.2 CO2", "Con.2 O2", "Con.2 Methane"],
                     ["Con.3 TVOC", "Con.3 BME", "Con.3 CO2", "Con.3 O2", "Con.3 Methane"],
                     ["Con.4 TVOC", "Con.4 BME", "Con.4 CO2", "Con.4 O2", "Con.4 Methane"]
                     ]
    variable_names = np.transpose(variable_names)

    for i in range(5):
        section_variables = []
        section_squares = []
        for j in range(4):
            var = tk.BooleanVar()
            var.set(sensor_markers[i][j])
            section_variables.append(var)
            square = tk.Label(window, text=variable_names[i][j], width=20, height=10)
            square.grid(row=i, column=j, padx=5, pady=5)  # Use grid with appropriate row and column indices
            section_squares.append(square)

        my_variables.append(section_variables)
        squares.append(section_squares)

        # Update square colors after creating the section
        for j in range(4):
            update_square_color(i, j)

    endtime = datetime.datetime.now()

    runTime = endtime - startupTime

    print(f'TKintergui.py took {runTime} to open the gui.')

    # Start the Tkinter event loop
    window.mainloop()