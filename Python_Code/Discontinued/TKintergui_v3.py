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

def pull_C1_TVOC_data(*args):

    global C1_TVOC_marker

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

def pull_C2_TVOC_data(*args):

    global C2_TVOC_marker

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

def pull_C3_TVOC_data(*args):

    global C3_TVOC_marker

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

def pull_C4_TVOC_data(*args):

    global C4_TVOC_marker

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

def pull_C1_BME_data(*args):

    global C1_BME_marker

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

def pull_C2_BME_data(*args):
    
    global C2_BME_marker

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

def pull_C3_BME_data(*args):
    
    global C3_BME_marker
    
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

def pull_C4_BME_data(*args):
    
    global C4_BME_marker

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

def pull_C1_CO2_data(*args):
    
    global C1_CO2_marker

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

def pull_C2_CO2_data(*args):

    global C2_CO2_marker

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

def pull_C3_CO2_data(*args):

    global C3_CO2_marker

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

def pull_C4_CO2_data(*args):
    
    global C4_CO2_marker
    
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

def pull_C1_O2_data(*args):

    global C1_O2_marker

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

def pull_C2_O2_data(*args):

    global C2_O2_marker

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

def pull_C3_O2_data(*args):
    
    global C3_O2_marker
    
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

def pull_C4_O2_data(*args):
    
    global C4_O2_marker
    
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

def pull_C1_Meth_data(*args):
    
    global C1_Meth_marker

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

def pull_C2_Meth_data(*args):

    global C2_Meth_marker
    
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

def pull_C3_Meth_data(*args):

    global C3_Meth_marker
    
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

def pull_C4_Meth_data(*args):

    global C4_Meth_marker
    
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


if __name__ == "__main__":
    startTime_main = datetime.datetime.now()
    #create threads
    t1 = threading.Thread(target=pull_C1_TVOC_data, args = ())
    t2 = threading.Thread(target=pull_C1_BME_data, args = ())
    t3 = threading.Thread(target=pull_C1_CO2_data, args = ())
    t4 = threading.Thread(target=pull_C1_O2_data, args = ())
    t5 = threading.Thread(target=pull_C1_Meth_data, args = ())
    t6 = threading.Thread(target=pull_C2_TVOC_data, args = ())
    t7 = threading.Thread(target=pull_C2_BME_data, args = ())
    t8 = threading.Thread(target=pull_C2_CO2_data, args = ())
    t9 = threading.Thread(target=pull_C2_O2_data, args = ())
    t10 = threading.Thread(target=pull_C2_Meth_data, args = ())
    t11 = threading.Thread(target=pull_C3_TVOC_data, args = ())
    t12 = threading.Thread(target=pull_C3_BME_data, args = ())
    t13 = threading.Thread(target=pull_C3_CO2_data, args = ())
    t14 = threading.Thread(target=pull_C3_O2_data, args = ())
    t15 = threading.Thread(target=pull_C3_Meth_data, args = ())
    t16 = threading.Thread(target=pull_C4_TVOC_data, args = ())
    t17 = threading.Thread(target=pull_C4_BME_data, args = ())
    t18 = threading.Thread(target=pull_C4_CO2_data, args = ())
    t19 = threading.Thread(target=pull_C4_O2_data, args = ())
    t20 = threading.Thread(target=pull_C4_Meth_data, args = ())

    #start thread processes
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    t11.start()
    t12.start()
    t13.start()
    t14.start()
    t15.start()
    t16.start()
    t17.start()
    t18.start()
    t19.start()
    t20.start()
    
    #wait for each to finish before continuing
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()
    t10.join()
    t11.join()
    t12.join()
    t13.join()
    t14.join()
    t15.join()
    t16.join()
    t17.join()
    t18.join()
    t19.join()
    t20.join()

    endTime_main = datetime.datetime.now()
    totalTime_main = endTime_main - startTime_main
    print(f'if name = main block executed in {totalTime_main}')

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

print(f'TKintergui.py took {runTime} to open the gui.' )

# Start the Tkinter event loop
window.mainloop()

# class monitor_output:

#     def __init__(self, data):
#         initstarttime = datetime.datetime.now()
#         self.pandas_df = pandas.DataFrame(data)
#         self.lastdate = self.pandas_df.Date_Time[0]
#         self.lastdate.to_pydatetime()
#         self.timedelta = datetime.datetime.now() - self.lastdate
#         if (self.timedelta.total_seconds() >= 5.0):
#             self.marker = False
#         else:
#             self.marker = True
#         initendtime = datetime.datetime.now()
#         inittotaltime = initendtime - initstarttime
#         print(f'init took {inittotaltime} to execute.')

# markers = []

# def getMarker(data):
#     initstarttime = datetime.datetime.now()
#     pandas_df = pandas.DataFrame(data)
#     lastdate = pandas_df.Date_Time[0]
#     lastdate.to_pydatetime()
#     timedelta = datetime.datetime.now() - self.lastdate
#     if (timedelta.total_seconds() >= 5.0):
#         markers.append(False)
#     else:
#         markers.append(True)
#     initendtime = datetime.datetime.now()
#     inittotaltime = initendtime - initstarttime
#     print(f'init took {inittotaltime} to execute.')

# [
#     [C1_TVOC_marker.marker, C1_BME_marker.marker, C1_CO2_marker.marker, C1_O2_marker.marker, C1_Meth_marker.marker],
#     [C2_TVOC_marker.marker, C2_BME_marker.marker, C2_CO2_marker.marker, C2_O2_marker.marker, C2_Meth_marker.marker],
#     [C3_TVOC_marker.marker, C3_BME_marker.marker, C3_CO2_marker.marker, C3_O2_marker.marker, C3_Meth_marker.marker],
#     [C4_TVOC_marker.marker, C4_BME_marker.marker, C4_CO2_marker.marker, C4_O2_marker.marker, C4_Meth_marker.marker]
# ]

# C1_TVOC_marker = monitor_output(C1_TVOC[0])
# C1_BME_marker = monitor_output(C1_BME[0])
# C1_CO2_marker = monitor_output(C1_CO2[0])
# C1_O2_marker = monitor_output(C1_O2[0])
# C1_Meth_marker = monitor_output(C1_Meth[0])
# C2_TVOC_marker = monitor_output(C2_TVOC[0])
# C2_BME_marker = monitor_output(C2_BME[0])
# C2_CO2_marker = monitor_output(C2_CO2[0])
# C2_O2_marker = monitor_output(C2_O2[0])
# C2_Meth_marker = monitor_output(C2_Meth[0])
# C3_TVOC_marker = monitor_output(C3_TVOC[0])
# C3_BME_marker = monitor_output(C3_BME[0])
# C3_CO2_marker = monitor_output(C3_CO2[0])
# C3_O2_marker = monitor_output(C3_O2[0])
# C3_Meth_marker = monitor_output(C3_Meth[0])
# C4_TVOC_marker = monitor_output(C4_TVOC[0])
# C4_BME_marker = monitor_output(C4_BME[0])
# C4_CO2_marker = monitor_output(C4_CO2[0])
# C4_O2_marker = monitor_output(C4_O2[0])
# C4_Meth_marker = monitor_output(C4_Meth[0])