import csv
import matplotlib as mpl
import matplotlib.pyplot as p
import numpy as np
import os
import glob
from datetime import datetime

degree_sign = u'\N{DEGREE SIGN}'
mpl.use('TkAgg')

O2_datelist: list = []
O2_con: list = []
CO2_datelist: list = []
CO2_con: list = []
RB_datelist: list = []
RB_CO2_con: list = []
RB_TVOC_con: list = []
RB_Hum: list = []
RB_P: list = []
RB_T: list = []

path_O2 = r'C:\Users\danbr\Desktop\IDEAS Lab Work\Test Data\Bucket 1 (Control)\Test 1\O2'
for filename in glob.glob(os.path.join(path_O2, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            O2_datelist.append(datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S'))
            O2_con.append(row[1])
print('O2 works')
path_CO2 = r'C:\Users\danbr\Desktop\IDEAS Lab Work\Test Data\Bucket 1 (Control)\Test 1\CO2'
for filename in glob.glob(os.path.join(path_CO2, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            CO2_datelist.append(datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S'))
            CO2_con.append(row[1])
print('CO2 works')
path_RB = r'C:\Users\danbr\Desktop\IDEAS Lab Work\Test Data\Bucket 1 (Control)\Test 1\RB'
for filename in glob.glob(os.path.join(path_RB, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            RB_datelist.append(datetime.strptime(row[0], '%m-%d-%Y %H:%M:%S'))
            RB_CO2_con.append(row[1])
            RB_TVOC_con.append(row[2])
            RB_Hum.append(row[3])
            RB_P.append(row[4])
            RB_T.append(row[5])
print('RB works')

RB_P_Float = [float(x) for x in RB_P]
RB_P_Float_min = min(RB_P_Float)
RB_P_Float_max = max(RB_P_Float)

O2_Con_Float = [float(x) for x in O2_con]
CO2_Con_Float = [float(x) for x in CO2_con]
RB_Hum_Float = [float(x) for x in RB_Hum]
RB_CO2_Con_Float = [float(x) for x in RB_CO2_con]
RB_TVOC_Con_Float = [float(x) for x in RB_TVOC_con]
RB_T_Float = [float(x) for x in RB_T]

fig1 = p.figure(1, figsize = (11,8))
ax1 = fig1.add_subplot()
ax1.scatter(O2_datelist, O2_Con_Float, s= 10, marker = 's', label = 'AS EZO-O2 O2 Con')
p.legend(loc = 'upper right')
p.savefig(r'C:\Users\danbr\Desktop\IDEAS Lab Work\Test Data\Bucket 1 (Control)\Figures\9-29-2022\AS_O2_Con.png')

fig2 = p.figure(2, figsize = (11,8))
ax2 = fig2.add_subplot()
ax2.scatter(CO2_datelist, CO2_Con_Float, s= 10, marker = 's', label = 'AS EZO-CO2 CO2 Con')
p.legend(loc = 'upper right')
p.savefig(r'C:\Users\danbr\Desktop\IDEAS Lab Work\Test Data\Bucket 1 (Control)\Figures\9-29-2022\AS_CO2_Con.png')

fig3 = p.figure(3, figsize = (11,8))
ax3 = fig3.add_subplot()
ax3.scatter(RB_datelist, RB_Hum_Float, s= 10, marker = 's', label = 'RedBoard Relative Humidity')
p.legend(loc = 'upper right')
p.savefig(r'C:\Users\danbr\Desktop\IDEAS Lab Work\Test Data\Bucket 1 (Control)\Figures\9-29-2022\RB_Hum.png')

fig4 = p.figure(4, figsize = (11,8))
ax4 = fig4.add_subplot()
ax4.scatter(RB_datelist, RB_CO2_Con_Float, s= 10, marker = 's', label = 'RedBoard CO2 Con')
p.legend(loc = 'upper right')
p.savefig(r'C:\Users\danbr\Desktop\IDEAS Lab Work\Test Data\Bucket 1 (Control)\Figures\9-29-2022\RB_CO2_Con.png')

fig5 = p.figure(5, figsize = (11,8))
ax5 = fig5.add_subplot()
ax5.scatter(RB_datelist, RB_TVOC_Con_Float, s= 10, marker = 's', label = 'RedBoard TVOC Con')
p.legend(loc = 'upper right')
p.savefig(r'C:\Users\danbr\Desktop\IDEAS Lab Work\Test Data\Bucket 1 (Control)\Figures\9-29-2022\RB_TVOC_Con.png')

fig6 = p.figure(6, figsize = (11,8))
ax6 = fig6.add_subplot()
ax6.scatter(RB_datelist[1:-1],RB_P_Float[1:-1], s= 10, marker = 's', label = 'RedBoard Pressure (Pa)')
p.legend(loc = 'upper right')
p.savefig(r'C:\Users\danbr\Desktop\IDEAS Lab Work\Test Data\Bucket 1 (Control)\Figures\9-29-2022\RB_P.png')

fig7 = p.figure(7, figsize = (11,8))
ax7 = fig7.add_subplot()
ax7.scatter(RB_datelist, RB_T_Float, s= 10, marker = 's', label = 'RedBoard Temperature ({}C)'.format(degree_sign))
p.legend(loc = 'upper right')
p.savefig(r'C:\Users\danbr\Desktop\IDEAS Lab Work\Test Data\Bucket 1 (Control)\Figures\9-29-2022\RB_T.png')

fig8 = p.figure(8, figsize = (14, 8))
ax8 = fig8.add_subplot()
ax8.scatter(CO2_datelist, CO2_Con_Float, s = 10, c = 'b', marker = 's', label = 'AS EZO-CO2 CO2 Con')
ax8.scatter(RB_datelist, RB_CO2_Con_Float, s= 10, c = 'r', marker = 's', label = 'RedBoard CO2 Con')
p.legend(loc = 'upper right')
p.savefig(r'C:\Users\danbr\Desktop\IDEAS Lab Work\Test Data\Bucket 1 (Control)\Figures\9-29-2022\AS_RB_CO2_Con.png')
p.show()