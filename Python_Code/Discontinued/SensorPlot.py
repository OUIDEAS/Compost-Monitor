import csv
import matplotlib as mpl
import matplotlib.pyplot as p
import numpy as np
import os
import glob
from datetime import datetime
import pathlib

degree_sign = u'\N{DEGREE SIGN}'
mpl.use('TkAgg')

O2_datelist_1: list = []
O2_con_1: list = []
CO2_datelist_1: list = []
CO2_con_1: list = []
RB_datelist_1: list = []
RB_TVOC_con_1: list = []
RB_Hum_1: list = []
RB_P_1: list = []
RB_T_1: list = []

O2_datelist_2: list = []
O2_con_2: list = []
CO2_datelist_2: list = []
CO2_con_2: list = []
PMQ_datelist_2: list = []
PMQ_TVOC_con_2: list = []
PMQ_Hum_2: list = []
PMQ_P_2: list = []
PMQ_T_2: list = []

O2_datelist_3: list = []
O2_con_3: list = []
CO2_datelist_3: list = []
CO2_con_3: list = []
PMQ_datelist_3: list = []
PMQ_TVOC_con_3: list = []
PMQ_Hum_3: list = []
PMQ_P_3: list = []
PMQ_T_3: list = []

O2_datelist_4: list = []
O2_con_4: list = []
CO2_datelist_4: list = []
CO2_con_4: list = []
RB_datelist_4: list = []
RB_TVOC_con_4: list = []
RB_Hum_4: list = []
RB_P_4: list = []
RB_T_4: list = []

## Make figure save path ##
figSavePath = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\11-18-2022\Figures"
pathlib.Path(figSavePath).mkdir(parents=True, exist_ok=True)

## Read each sensor type, bucket by bucket ##
path_O2_1 = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\11-18-2022\Bucket 1\O2"
for filename in glob.glob(os.path.join(path_O2_1, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        for row in reader:
            O2_datelist_1.append(datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S'))
            O2_con_1.append(row[1])
path_O2_2 = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\11-18-2022\Bucket 2\O2"
for filename in glob.glob(os.path.join(path_O2_2, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        for row in reader:
            O2_datelist_2.append(datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S'))
            O2_con_2.append(row[1])
path_O2_3 = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\11-18-2022\Bucket 3\O2"
for filename in glob.glob(os.path.join(path_O2_3, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        for row in reader:
            O2_datelist_3.append(datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S'))
            O2_con_3.append(row[1])
path_O2_4 = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\11-18-2022\Bucket 4\O2"
for filename in glob.glob(os.path.join(path_O2_4, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        for row in reader:
            O2_datelist_4.append(datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S'))
            O2_con_4.append(row[1])

print('O2 works')
path_CO2 = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\11-18-2022\Bucket 1\CO2"
for filename in glob.glob(os.path.join(path_CO2, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        for row in reader:
            CO2_datelist_1.append(datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S'))
            CO2_con_1.append(row[1])
path_CO2 = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\11-18-2022\Bucket 2\CO2"
for filename in glob.glob(os.path.join(path_CO2, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        for row in reader:
            CO2_datelist_2.append(datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S'))
            CO2_con_2.append(row[1])
path_CO2 = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\11-18-2022\Bucket 3\CO2"
for filename in glob.glob(os.path.join(path_CO2, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        for row in reader:
            CO2_datelist_3.append(datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S'))
            CO2_con_3.append(row[1])
path_CO2 = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\11-18-2022\Bucket 4\CO2"
for filename in glob.glob(os.path.join(path_CO2, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        for row in reader:
            CO2_datelist_4.append(datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S'))
            CO2_con_4.append(row[1])
print('CO2 works')
path_RB_1 = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\11-18-2022\Bucket 1\RB"
for filename in glob.glob(os.path.join(path_RB_1, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        for row in reader:
            RB_datelist_1.append(datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S'))
            RB_TVOC_con_1.append(row[1])
            RB_Hum_1.append(row[2])
            RB_P_1.append(row[3])
            RB_T_1.append(row[4])
path_RB_4 = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\11-18-2022\Bucket 4\RB"
for filename in glob.glob(os.path.join(path_RB_4, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        for row in reader:
            RB_datelist_4.append(datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S'))
            RB_TVOC_con_4.append(row[1])
            RB_Hum_4.append(row[2])
            RB_P_4.append(row[3])
            RB_T_4.append(row[4])
path_PMQ_2 = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\11-18-2022\Bucket 2\PMQ"
for filename in glob.glob(os.path.join(path_PMQ_2, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        for row in reader:
            PMQ_datelist_2.append(datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S'))
            PMQ_TVOC_con_2.append(row[1])
            PMQ_Hum_2.append(row[2])
            PMQ_P_2.append(row[3])
            PMQ_T_2.append(row[4])
path_PMQ_3 = r"C:\Users\Dan's Loaner\Documents\Compost Monitor\Test Data\11-18-2022\Bucket 3\PMQ"
for filename in glob.glob(os.path.join(path_PMQ_3, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        for row in reader:
            PMQ_datelist_3.append(datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S'))
            PMQ_TVOC_con_3.append(row[1])
            PMQ_Hum_3.append(row[2])
            PMQ_P_3.append(row[3])
            PMQ_T_3.append(row[4])
print('RB works')


## Convert strings to floating point numbers ##
RB_P_Float_1 = [float(x) for x in RB_P_1]
RB_Hum_Float_1 = [float(x) for x in RB_Hum_1]
RB_TVOC_Con_Float_1 = [float(x) for x in RB_TVOC_con_1]
RB_T_Float_1 = [float(x) for x in RB_T_1]

RB_P_Float_4 = [float(x) for x in RB_P_4]
RB_Hum_Float_4 = [float(x) for x in RB_Hum_4]
RB_TVOC_Con_Float_4 = [float(x) for x in RB_TVOC_con_4]
RB_T_Float_4 = [float(x) for x in RB_T_4]

PMQ_P_Float_2 = [float(x) for x in PMQ_P_2]
PMQ_Hum_Float_2 = [float(x) for x in PMQ_Hum_2]
PMQ_TVOC_Con_Float_2 = [float(x) for x in PMQ_TVOC_con_2]
PMQ_T_Float_2 = [float(x) for x in PMQ_T_2]

PMQ_P_Float_3 = [float(x) for x in PMQ_P_3]
PMQ_Hum_Float_3 = [float(x) for x in PMQ_Hum_3]
PMQ_TVOC_Con_Float_3 = [float(x) for x in PMQ_TVOC_con_3]
PMQ_T_Float_3 = [float(x) for x in PMQ_T_3]

O2_Con_Float_1 = [float(x) for x in O2_con_1]
O2_Con_Float_2 = [float(x) for x in O2_con_2]
O2_Con_Float_3 = [float(x) for x in O2_con_3]
O2_Con_Float_4 = [float(x) for x in O2_con_4]

CO2_Con_Float_1 = [float(x) for x in CO2_con_1]
CO2_Con_Float_2 = [float(x) for x in CO2_con_2]
CO2_Con_Float_3 = [float(x) for x in CO2_con_3]
CO2_Con_Float_4 = [float(x) for x in CO2_con_4]

RB_TVOC_MAvg_1 = []
RB_TVOC_MAvg_4 = []
PMQ_TVOC_MAvg_2 = []
PMQ_TVOC_MAvg_3 = []
i = 0


## Calculate basic moving averages ##
while i<len(RB_TVOC_Con_Float_1):
    if i<=30:
        RB_TVOC_MAvg_1.append(RB_TVOC_Con_Float_1[i])
    else:
        RB_TVOC_MAvg_1.append((np.sum(RB_TVOC_Con_Float_1[i-29:i])/30))
    i+=1
i = 0
while i<len(RB_TVOC_Con_Float_4):
    if i<=30:
        RB_TVOC_MAvg_4.append(RB_TVOC_Con_Float_4[i])
    else:
        RB_TVOC_MAvg_4.append((np.sum(RB_TVOC_Con_Float_4[i-29:i])/30))
    i+=1
i = 0
while i<len(PMQ_TVOC_Con_Float_2):
    if i<=30:
        PMQ_TVOC_MAvg_2.append(PMQ_TVOC_Con_Float_2[i])
    else:
        PMQ_TVOC_MAvg_2.append((np.sum(PMQ_TVOC_Con_Float_2[i-29:i])/30))
    i+=1
i = 0
while i<len(PMQ_TVOC_Con_Float_3):
    if i<=30:
        PMQ_TVOC_MAvg_3.append(PMQ_TVOC_Con_Float_3[i])
    else:
        PMQ_TVOC_MAvg_3.append((np.sum(PMQ_TVOC_Con_Float_3[i-29:i])/30))
    i+=1

## Make plots ##
p.rcParams.update({'font.size': 16})
fig1 = p.figure(1, figsize = (11,8))
ax1 = fig1.add_subplot()
ax1.set_title('O2 Concentration versus Time')
ax1.set_xlabel('Time (MM-DD HH)')
ax1.set_ylabel('O2 Concentration (%)')
ax1.scatter(O2_datelist_1, O2_Con_Float_1, s= 10, marker = 's', label = 'O2 Con - Bucket 1')
ax1.scatter(O2_datelist_2, O2_Con_Float_2, s=10, marker = '+', label = 'O2 Con - Bucket 2')
ax1.scatter(O2_datelist_3, O2_Con_Float_3, s=10, marker = 'x', label = 'O2 Con - Bucket 3')
ax1.scatter(O2_datelist_4, O2_Con_Float_4, s=10, marker = 'd', label = 'O2 Con - Bucket 4')
p.legend(loc = 'upper right')
p.savefig(r"{}\O2_Con.png".format(figSavePath))

fig2 = p.figure(2, figsize = (11,8))
ax2 = fig2.add_subplot()
ax2.set_title('CO2 Concentration versus Time')
ax2.set_xlabel('Time (MM-DD HH)')
ax2.set_ylabel('CO2 Concentration (ppm)')
ax2.scatter(CO2_datelist_1, CO2_Con_Float_1, s= 10, marker = 's', label = 'CO2 Con - Bucket 1')
ax2.scatter(CO2_datelist_2, CO2_Con_Float_2, s= 10, marker = '+', label = 'CO2 Con - Bucket 2')
ax2.scatter(CO2_datelist_3, CO2_Con_Float_3, s= 10, marker = 'x', label = 'CO2 Con - Bucket 3')
ax2.scatter(CO2_datelist_4, CO2_Con_Float_4, s= 10, marker = 'd', label = 'CO2 Con - Bucket 4')
p.legend(loc = 'upper right')
p.savefig(r"{}\CO2_Con.png".format(figSavePath))

fig3 = p.figure(3, figsize = (11,8))
ax3 = fig3.add_subplot()
ax3.set_title('Relative Humidity versus Time')
ax3.set_xlabel('Time (MM-DD HH)')
ax3.set_ylabel('Relative Humidity (%)')
ax3.scatter(RB_datelist_1, RB_Hum_Float_1, s= 10, marker = 's', label = 'Bucket 1 Relative Humidity')
ax3.scatter(PMQ_datelist_2, PMQ_Hum_Float_2, s= 10, marker = '+', label = 'Bucket 2 Relative Humidity')
ax3.scatter(PMQ_datelist_3, PMQ_Hum_Float_3, s= 10, marker = 'x', label = 'Bucket 3 Relative Humidity')
ax3.scatter(RB_datelist_4, RB_Hum_Float_4, s= 10, marker = 'd', label = 'Bucket 4 Relative Humidity')
p.legend(loc = 'upper right')
p.savefig(r"{}\Humidity.png".format(figSavePath))


fig4 = p.figure(4, figsize = (11,8))
ax4 = fig4.add_subplot()
ax4.set_title('TVOC Concentration versus Time')
ax4.set_xlabel('Time (MM-DD HH)')
ax4.set_ylabel('TVOC Concentration (ppb)')
ax4.scatter(RB_datelist_1, RB_TVOC_Con_Float_1, s= 10, marker = 's', label = 'Bucket 1 TVOC Con')
ax4.scatter(PMQ_datelist_2, PMQ_TVOC_Con_Float_2, s= 10, marker = '+', label = 'Bucket 2 TVOC Con')
ax4.scatter(PMQ_datelist_3, PMQ_TVOC_Con_Float_3, s= 10, marker = 'x', label = 'Bucket 3 TVOC Con')
ax4.scatter(RB_datelist_4, RB_TVOC_Con_Float_4, s= 10, marker = 'd', label = 'Bucket 4 TVOC Con')
p.legend(loc = 'upper right')
p.savefig(r"{}\TVOC_Con.png".format(figSavePath))

fig5 = p.figure(5, figsize = (11,8))
ax5 = fig5.add_subplot()
ax5.set_title('Pressure versus Time')
ax5.set_xlabel('Time (MM-DD HH)')
ax5.set_ylabel('Pressure (Pa)')
ax5.scatter(RB_datelist_1[1:-1],RB_P_Float_1[1:-1], s= 10, marker = 's', label = 'Bucket 1 Pressure (Pa)')
ax5.scatter(PMQ_datelist_2[1:-1],PMQ_P_Float_2[1:-1], s= 10, marker = '+', label = 'Bucket 2 Pressure (Pa)')
ax5.scatter(PMQ_datelist_3[1:-1],PMQ_P_Float_3[1:-1], s= 10, marker = 'x', label = 'Bucket 3 Pressure (Pa)')
ax5.scatter(RB_datelist_4[1:-1],RB_P_Float_4[1:-1], s= 10, marker = 'd', label = 'Bucket 4 Pressure (Pa)')
p.legend(loc = 'upper right')
p.savefig(r"{}\Pressure.png".format(figSavePath))

fig6 = p.figure(6, figsize = (11,8))
ax6 = fig6.add_subplot()
ax6.set_title('Temperature versus Time')
ax6.set_xlabel('Time (MM-DD HH)')
ax6.set_ylabel('Temperature (deg C)')
ax6.scatter(RB_datelist_1, RB_T_Float_1, s= 10, marker = 's', label = 'Bucket 1 Temperature ({}C)'.format(degree_sign))
ax6.scatter(PMQ_datelist_2, PMQ_T_Float_2, s= 10, marker = '+', label = 'Bucket 2 Temperature ({}C)'.format(degree_sign))
ax6.scatter(PMQ_datelist_3, PMQ_T_Float_3, s= 10, marker = 'x', label = 'Bucket 3 Temperature ({}C)'.format(degree_sign))
ax6.scatter(RB_datelist_4, RB_T_Float_4, s= 10, marker = 'd', label = 'Bucket 4 Temperature ({}C)'.format(degree_sign))
p.legend(loc = 'upper right')
p.savefig(r"{}\Temperature.png".format(figSavePath))


fig7 = p.figure(7, figsize = (14, 8))
ax7 = fig7.add_subplot()
ax7.set_title('TVOC Concentration versus Time - Moving Average')
ax7.set_xlabel('Time (MM-DD HH)')
ax7.set_ylabel('TVOC Concentration (ppb)')
ax7.scatter(RB_datelist_1, RB_TVOC_MAvg_1, s = 10, marker = 's', label = 'Bucket 1 TVOC Moving Average')
ax7.scatter(PMQ_datelist_2, PMQ_TVOC_MAvg_2, s = 10, marker = '+', label = 'Bucket 2 TVOC Moving Average')
ax7.scatter(PMQ_datelist_3, PMQ_TVOC_MAvg_3, s = 10, marker = 'x', label = 'Bucket 3 TVOC Moving Average')
ax7.scatter(RB_datelist_4, RB_TVOC_MAvg_4, s = 10, marker = 'd', label = 'Bucket 4 TVOC Moving Average')
p.legend(loc = 'upper right')
p.savefig(r"{}\TVOC_MovingAvg_30.png".format(figSavePath))


p.show()