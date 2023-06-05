import tkinter as tk
import pymongo
import pandas
import datetime
import threading

startupTime = datetime.datetime.now()

client = pymongo.MongoClient("mongodb://100.110.90.28/")
db = client['CompostMonitor']
collection = db['Overall']

C1_TVOC = []
C1_BME = []
C1_CO2 = []
C1_O2 = []
C1_Meth = []
C2_TVOC = []
C2_BME = []
C2_CO2 = []
C2_O2 = []
C2_Meth = []
C3_TVOC = []
C3_BME = []
C3_CO2 = []
C3_O2 = []
C3_Meth = []
C4_TVOC = []
C4_BME = []
C4_CO2 = []
C4_O2 = []
C4_Meth = []

C1_TVOC_marker = False
C1_BME_marker = False
C1_CO2_marker = False
C1_O2_marker = False
C1_Meth_marker = False
C2_TVOC_marker = False
C2_BME_marker = False
C2_CO2_marker = False
C2_O2_marker = False
C2_Meth_marker = False
C3_TVOC_marker = False
C3_BME_marker = False
C3_CO2_marker = False
C3_O2_marker = False
C3_Meth_marker = False
C4_TVOC_marker = False
C4_BME_marker = False
C4_CO2_marker = False
C4_O2_marker = False
C4_Meth_marker = False

def pull_data(Sensor):
    global C1_TVOC_marker, C1_BME_marker, C1_CO2_marker, C1_O2_marker, C1_Meth_marker
    global C2_TVOC_marker, C2_BME_marker, C2_CO2_marker, C2_O2_marker, C2_Meth_marker
    global C3_TVOC_marker, C3_BME_marker, C3_CO2_marker, C3_O2_marker, C3_Meth_marker
    global C4_TVOC_marker, C4_BME_marker, C4_CO2_marker, C4_O2_marker, C4_Meth_marker

    match Sensor:
        case "TVOC":
            C1_TVOC.append(collection.find({
                            'Container_No': '1', 
                            'TVOC_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C1_TVOC[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C1_TVOC_marker = False
            else:
                C1_TVOC_marker = True
            C2_TVOC.append(collection.find({
                            'Container_No': '2', 
                            'TVOC_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C2_TVOC[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C2_TVOC_marker = False
            else:
                C2_TVOC_marker = True
            C3_TVOC.append(collection.find({
                            'Container_No': '3', 
                            'TVOC_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C3_TVOC[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C3_TVOC_marker = False
            else:
                C3_TVOC_marker = True
            C4_TVOC.append(collection.find({
                            'Container_No': '4', 
                            'TVOC_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C4_TVOC[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C4_TVOC_marker = False
            else:
                C4_TVOC_marker = True
        case "BME":
            C1_BME.append(collection.find({
                            'Container_No': '1', 
                            'BME_Humidity': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C1_BME[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C1_BME_marker = False
            else:
                C1_BME_marker = True
            C2_BME.append(collection.find({
                            'Container_No': '2', 
                            'BME_Humidity': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C2_BME[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C2_BME_marker = False
            else:
                C2_BME_marker = True
            C3_BME.append(collection.find({
                            'Container_No': '3', 
                            'BME_Humidity': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C3_BME[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C3_BME_marker = False
            else:
                C3_BME_marker = True
            C4_BME.append(collection.find({
                            'Container_No': '4', 
                            'BME_Humidity': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C4_BME[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C4_BME_marker = False
            else:
                C4_BME_marker = True
        case "CO2":
            C1_CO2.append(collection.find({
                            'Container_No': '1', 
                            'CO2_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C1_CO2[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C1_CO2_marker = False
            else:
                C1_CO2_marker = True
            C2_CO2.append(collection.find({
                            'Container_No': '2', 
                            'CO2_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C2_CO2[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C2_CO2_marker = False
            else:
                C2_CO2_marker = True
            C3_CO2.append(collection.find({
                            'Container_No': '3', 
                            'CO2_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C3_CO2[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C3_CO2_marker = False
            else:
                C3_CO2_marker = True
            C4_CO2.append(collection.find({
                            'Container_No': '4', 
                            'CO2_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C4_CO2[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C4_CO2_marker = False
            else:
                C4_CO2_marker = True
        case "O2":
            C1_O2.append(collection.find({
                            'Container_No': '1', 
                            'O2_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C1_O2[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C1_O2_marker = False
            else:
                C1_O2_marker = True
            C2_O2.append(collection.find({
                            'Container_No': '2', 
                            'O2_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C2_O2[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C2_O2_marker = False
            else:
                C2_O2_marker = True
            C3_O2.append(collection.find({
                            'Container_No': '3', 
                            'O2_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C3_O2[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C3_O2_marker = False
            else:
                C3_O2_marker = True
            C4_O2.append(collection.find({
                            'Container_No': '4', 
                            'O2_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C4_O2[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C4_O2_marker = False
            else:
                C4_O2_marker = True
        case "Methane":
            C1_Meth.append(collection.find({
                            'Container_No': '1', 
                            'Methane_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C1_Meth[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C1_Meth_marker = False
            else:
                C1_Meth_marker = True
            C2_Meth.append(collection.find({
                            'Container_No': '2', 
                            'Methane_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C2_Meth[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C2_Meth_marker = False
            else:
                C2_Meth_marker = True
            C3_Meth.append(collection.find({
                            'Container_No': '3', 
                            'Methane_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C3_Meth[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C3_Meth_marker = False
            else:
                C3_Meth_marker = True
            C4_Meth.append(collection.find({
                            'Container_No': '4', 
                            'Methane_Con': {'$exists': 'True'}
                            }).sort("Date_Time", pymongo.DESCENDING).limit(1))
            pandas_df = pandas.DataFrame(C4_Meth[0])
            lastdate = pandas_df.Date_Time[0]
            lastdate.to_pydatetime()
            timedelta = datetime.datetime.now() - lastdate
            if (timedelta.total_seconds() >= 5.0):
                C4_Meth_marker = False
            else:
                C4_Meth_marker = True
        case _:
            print('Invalid Sensor Name; valid names are TVOC, BME, CO2, O2, and Methane.')



if __name__ == "__main__":
    startTime_main = datetime.datetime.now()
    #create thread
    t1 = threading.Thread(target=pull_data, args = ('TVOC',))
    t2 = threading.Thread(target=pull_data, args = ('BME',))
    t3 = threading.Thread(target=pull_data, args = ('CO2',))
    t4 = threading.Thread(target=pull_data, args = ('O2',))
    t5 = threading.Thread(target=pull_data, args = ('Methane',))

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()

    endTime_main = datetime.datetime.now()
    totalTime_main = endTime_main - startTime_main
    print(f'if name = main block executed in {totalTime_main}')

startTime_main = datetime.datetime.now()

endTime_main = datetime.datetime.now()
totalTime_main = endTime_main - startTime_main
print(f'markers block executed in {totalTime_main}')

sensorMarkers = [
    [C1_TVOC_marker, C1_BME_marker, C1_CO2_marker, C1_O2_marker, C1_Meth_marker],
    [C2_TVOC_marker, C2_BME_marker, C2_CO2_marker, C2_O2_marker, C2_Meth_marker],
    [C3_TVOC_marker, C3_BME_marker, C3_CO2_marker, C3_O2_marker, C3_Meth_marker],
    [C4_TVOC_marker, C4_BME_marker, C4_CO2_marker, C4_O2_marker, C4_Meth_marker]
    ]

# Function to update the square color based on the variable value
def update_square_color(section_index, square_index):
    if my_variables[section_index][square_index].get():
        squares[section_index][square_index].config(bg='green')  # Set square background color to green if variable is True
    else:
        squares[section_index][square_index].config(bg='red')  # Set square background color to red if variable is False

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
        var.set(sensorMarkers[i][j])
        section_variables.append(var)
        square = tk.Label(window, text=variable_names[i][j], width=10, height=5)
        square.grid(row=i, column=j, padx=5, pady=5)  # Use grid with appropriate row and column indices
        section_squares.append(square)

    my_variables.append(section_variables)
    squares.append(section_squares)

    # Update square colors after creating the section
    for j in range(5):
        update_square_color(i, j)

endtime = datetime.datetime.now()

runTime = endtime - startupTime

print(f'TKintergui.py took {runTime} to open the gui.')

# Start the Tkinter event loop
window.mainloop()
