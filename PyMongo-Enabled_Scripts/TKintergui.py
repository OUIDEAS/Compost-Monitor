import tkinter as tk
import pymongo
import pandas
import datetime

client = pymongo.MongoClient("mongodb://100.110.90.28/")
db = client['CompostMonitor']
collection = db['Overall']

class monitor_output:
    def __init__(self, data):
        self.pandas_df = pandas.DataFrame(data)
        self.lastdate = self.pandas_df.Date_Time[0]
        self.lastdate.to_pydatetime()
        self.timedelta = datetime.datetime.now() - self.lastdate
        if (self.timedelta.total_seconds() >= 5.0):
            self.marker = False
        else:
            self.marker = True

# def pull_data():
C1_TVOC = collection.find({
                    'Container_No': '1', 
                    'TVOC_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)


C1_BME = collection.find({
                    'Container_No': '1', 
                    'BME_Humidity': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C1_CO2 = collection.find({
                    'Container_No': '1', 
                    'CO2_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C1_O2 = collection.find({
                    'Container_No': '1', 
                    'O2_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C1_meth = collection.find({
                    'Container_No': '1', 
                    'Methane_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C2_TVOC = collection.find({
                    'Container_No': '2', 
                    'TVOC_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C2_BME = collection.find({
                    'Container_No': '2', 
                    'BME_Humidity': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C2_CO2 = collection.find({
                    'Container_No': '2', 
                    'CO2_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C2_O2 = collection.find({
                    'Container_No': '2', 
                    'O2_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C2_meth = collection.find({
                    'Container_No': '2', 
                    'Methane_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C3_TVOC = collection.find({
                    'Container_No': '3', 
                    'TVOC_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C3_BME = collection.find({
                    'Container_No': '3', 
                    'BME_Humidity': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C3_CO2 = collection.find({
                    'Container_No': '3', 
                    'CO2_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C3_O2 = collection.find({
                    'Container_No': '3', 
                    'O2_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C3_meth = collection.find({
                    'Container_No': '3', 
                    'Methane_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C4_TVOC = collection.find({
                    'Container_No': '4', 
                    'TVOC_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C4_BME = collection.find({
                    'Container_No': '4', 
                    'BME_Humidity': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C4_CO2 = collection.find({
                    'Container_No': '4', 
                    'CO2_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C4_O2 = collection.find({
                    'Container_No': '4', 
                    'O2_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)

C4_meth = collection.find({
                    'Container_No': '4', 
                    'Methane_Con': {'$exists': 'True'}
                    }).sort("Date_Time", pymongo.DESCENDING).limit(1)
    
    # return C1_TVOC, C1_BME, C1_CO2, C1_O2, C1_meth, C2_TVOC, C2_BME, C2_CO2, C2_O2, C2_meth, C3_TVOC, C3_BME, C3_CO2, C3_O2, C3_meth, C4_TVOC, C4_BME, C4_CO2, C4_O2, C4_meth

# pull_data()

C1_TVOC_marker = monitor_output(C1_TVOC)
C1_BME_marker = monitor_output(C1_BME)
C1_CO2_marker = monitor_output(C1_CO2)
C1_O2_marker = monitor_output(C1_O2)
C1_Meth_marker = monitor_output(C1_meth)
C2_TVOC_marker = monitor_output(C2_TVOC)
C2_BME_marker = monitor_output(C2_BME)
C2_CO2_marker = monitor_output(C2_CO2)
C2_O2_marker = monitor_output(C2_O2)
C2_Meth_marker = monitor_output(C2_meth)
C3_TVOC_marker = monitor_output(C3_TVOC)
C3_BME_marker = monitor_output(C3_BME)
C3_CO2_marker = monitor_output(C3_CO2)
C3_O2_marker = monitor_output(C3_O2)
C3_Meth_marker = monitor_output(C3_meth)
C4_TVOC_marker = monitor_output(C4_TVOC)
C4_BME_marker = monitor_output(C4_BME)
C4_CO2_marker = monitor_output(C4_CO2)
C4_O2_marker = monitor_output(C4_O2)
C4_Meth_marker = monitor_output(C4_meth)

sensorMarkers = [
    [C1_TVOC_marker.marker, C1_BME_marker.marker, C1_CO2_marker.marker, C1_O2_marker.marker, C1_Meth_marker.marker],
    [C2_TVOC_marker.marker, C2_BME_marker.marker, C2_CO2_marker.marker, C2_O2_marker.marker, C2_Meth_marker.marker],
    [C3_TVOC_marker.marker, C3_BME_marker.marker, C3_CO2_marker.marker, C3_O2_marker.marker, C3_Meth_marker.marker],
    [C4_TVOC_marker.marker, C4_BME_marker.marker, C4_CO2_marker.marker, C4_O2_marker.marker, C4_Meth_marker.marker]
]

# Function to update the square color based on the variable value
def update_square_color(section_index, square_index):
    if my_variables[section_index][square_index].get():
        squares[section_index][square_index].config(bg='green')  # Set square background color to green if variable is True
    else:
        squares[section_index][square_index].config(bg='red')  # Set square background color to red if variable is False

# Create a Tkinter window
window = tk.Tk()
window.title("Variable Sections")

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

# Start the Tkinter event loop
window.mainloop()