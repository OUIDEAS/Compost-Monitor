import matplotlib.pyplot as plt
import numpy
import csv

file_name = open('C:\\Users\\danbr\\Desktop\\IDEAS Lab Work\\Test Data\\Test_All_Sensors_4 reformat.csv', 'r')

data = csv.DictReader(file_name)

dateColumn = []
timeColumn = []
CO2Column = []
O2Column = []
SGP_CO2Column = []
TVOC_Column = []
BME_HumColumn = []
BME_PressColumn = []
BME_TempColumn = []

count = 0
for col in data:
    dateColumn.append(col['Date'])
    timeColumn.append(col['Time'])
    CO2Column.append(col['EZO CO2 Con (ppm)'])
    O2Column.append(col['EZO O2 Con (%)'])
    SGP_CO2Column.append(col['SGP CO2 Con (ppm)'])
    TVOC_Column.append(col['SGP TVOC (ppb)'])
    BME_HumColumn.append(col['BME Humidity (%)'])
    BME_PressColumn.append(col['BME Pressure (Pa)'])
    BME_TempColumn.append(col['BME Temp (Deg C)'])
    count += 1

    if count > 200:
        break

print('date:', len(dateColumn))
print('time:', len(timeColumn))
print("CO2con:", len(CO2Column))
print("temp: ", len(BME_TempColumn))

figure, axis = plt.subplots(3, 3)

axis[0, 0].plot(timeColumn, CO2Column)
axis[0, 0].set_title("EZO CO2 Concentration versus Time")

axis[0, 1].plot(timeColumn, O2Column)
axis[0, 1].set_title("EZO O2 Concentration versus Time")

axis[0, 2].plot(timeColumn, SGP_CO2Column)
axis[0, 2].set_title("SGP30 CO2 Concentration versus Time")

axis[1, 1].plot(timeColumn, TVOC_Column)
axis[1, 1].set_title("SGP30 TVOC versus Time")

axis[2, 0].plot(timeColumn, BME_HumColumn)
axis[2, 0].set_title("BME280 Humidity Reading versus Time")

axis[2, 1].plot(timeColumn, BME_PressColumn)
axis[2, 1].set_title("BME280 Pressure Reading versus Time")

axis[2, 2].plot(timeColumn, BME_TempColumn)
axis[2, 2].set_title("BME280 Temperature Reading versus Time")

plt.show()