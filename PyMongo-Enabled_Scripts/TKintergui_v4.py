import multiprocessing
import tkinter as tk
import pymongo
import pandas
import datetime

# Define the function to pull data for a specific container and sensor
startupTime = datetime.datetime.now()

def pull_data(container_no, sensor, sensor_markers):

    client = pymongo.MongoClient("mongodb://100.110.90.28/")
    db = client['CompostMonitor']
    collection = db['Overall']
    # print(container_no)
    # print(sensor)
    data = collection.find({
        'Container_No': str(container_no),
        sensor: {'$exists': 'True'}
    }).sort("Date_Time", pymongo.DESCENDING).limit(1)
    # print('data pulled...')
    pandas_df = pandas.DataFrame(data)
    # print(pandas_df)
    # print(datetime.datetime.now())
    lastdate = pandas_df.Date_Time[0]
    lastdate = lastdate.to_pydatetime()
    timedelta = datetime.datetime.now() - lastdate
    # print(timedelta)
    if (timedelta.total_seconds() >= 15.0):
        if sensor == "TVOC_Con":
            sensor_markers[container_no - 1][0] = False
        elif sensor == "BME_Humidity":
            sensor_markers[container_no - 1][1] = False
        elif sensor == "CO2_Con":
            sensor_markers[container_no - 1][2] = False
        elif sensor == "O2_Con":
            sensor_markers[container_no - 1][3] = False
        elif sensor == "Methane":
            sensor_markers[container_no - 1][4] = False
    else:
        if sensor == "TVOC_Con":
            print('TVOC TRUE')
            sensor_markers[container_no - 1][0] = True
            # print(sensor_markers[container_no - 1][0])
        elif sensor == "BME_Humidity":
            print('BME true')
            sensor_markers[container_no - 1][1] = True
            # print(sensor_markers[container_no - 1][0])
        elif sensor == "CO2_Con":
            print('CO2 True')
            sensor_markers[container_no - 1][2] = True
            # print(sensor_markers[container_no - 1][0])
        elif sensor == "O2_Con":
            print('O2 True')
            sensor_markers[container_no - 1][3] = True
            # print(sensor_markers[container_no - 1][0])
        elif sensor == "Methane":
            print('Methane True')
            sensor_markers[container_no - 1][4] = True
            # print(sensor_markers[container_no - 1][0])

        # print('marker for container {} {} True'.format(container_no, sensor))

def update_square_color(section_index, square_index):
    if my_variables[section_index][square_index].get():
        squares[section_index][square_index].config(bg='green')
    else:
        squares[section_index][square_index].config(bg='red')

if __name__ == "__main__":

    startupTime_main = datetime.datetime.now()
    client = pymongo.MongoClient("mongodb://100.110.90.28/")
    db = client['CompostMonitor']
    collection = db['Overall']

    with multiprocessing.Manager() as manager:

        sensor_markers = manager.list([[False, False, False, False, False],
                                       [False, False, False, False, False],
                                       [False, False, False, False, False],
                                       [False, False, False, False, False]
                                       ])


        processes = []

        # Create processes to pull data for each container and sensor
        for container_no in range(1, 5):
            print(container_no)
            for sensor_index, sensor in enumerate(['TVOC_Con', 'BME_Humidity', 'CO2_Con', 'O2_Con', 'Methane_Con']):
                # print(sensor_index, sensor)
                process = multiprocessing.Process(target=pull_data, args=(container_no, sensor, sensor_markers))
                # process = multiprocessing.Process(target=pull_data, args=(container_no, sensor, sensor_markers[container_no - 1]))
                processes.append(process)

        # Start the processes
        for process in processes:
            process.start()

        # Wait for all processes to finish
        for process in processes:
            # print('pre-join...')
            process.join()
        
        sensor_markers = [list(sublist) for sublist in sensor_markers]

    endTime_main = datetime.datetime.now()
    totalTime_main = endTime_main - startupTime_main
    print(f'if __name__ == "__main__" block executed in {totalTime_main}')

    # Continue with the rest of the code (GUI, etc.)
    
    # Create a Tkinter window
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

    for i in range(4):
        section_variables = []
        section_squares = []
        for j in range(5):
            var = tk.BooleanVar()
            # print(sensor_markers[i][j])
            var.set(sensor_markers[i][j])
            section_variables.append(var)
            square = tk.Label(window, text=variable_names[i][j], width=10, height=5)
            square.grid(row=i, column=j, padx=5, pady=5)  # Use grid with appropriate row and column indices
            section_squares.append(square)

        my_variables.append(section_variables)
        print(my_variables)
        squares.append(section_squares)

        # Update square colors after creating the section
        for j in range(5):
            update_square_color(i, j)

    # process = multiprocessing.Process(target=makeWindow, args=(sensor_markers,))
    # process.start()
    # process.join()

    endtime = datetime.datetime.now()

    runTime = endtime - startupTime

    print(f'TKintergui.py took {runTime} to open the gui.' )

    # Start the Tkinter event loop
    window.mainloop()