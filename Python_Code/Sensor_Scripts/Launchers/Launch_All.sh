user=$(whoami)
# data_filepath=/home/"${user}"/CompostingData/
# script_filepath=/home/"${user}"/GitHub_Repositories/Compost-Monitor/Python_Code/Sensor_Scripts

# #Bin no.1
# python3 "${script_filepath}"/EZO_CO2_mongoupload.py  -c /dev/ttyUSB0  -f $data_filepath -n 1 -cn Overall -e April_2024 &
# python3 "${script_filepath}"/EZO_O2_mongoupload.py   -c /dev/ttyUSB1  -f $data_filepath -n 1 -cn Overall -e April_2024 &
# python3 "${script_filepath}"/RedBoard_mongoupload.py -c /dev/ttyUSB2  -f $data_filepath -n 1 -cn Overall -e April_2024 &
# python3 "${script_filepath}"/methane_mongoupload.py  -c /dev/ttyUSB3  -f $data_filepath -n 1 -cn Overall -e April_2024 &

# #Bin no.2
# python3 "${script_filepath}"/EZO_CO2_mongoupload.py  -c /dev/ttyUSB4  -f $data_filepath -n 2 -cn Overall -e April_2024 &
# python3 "${script_filepath}"/EZO_O2_mongoupload.py   -c /dev/ttyUSB5  -f $data_filepath -n 2 -cn Overall -e April_2024 &
# python3 "${script_filepath}"/RedBoard_mongoupload.py -c /dev/ttyUSB6  -f $data_filepath -n 2 -cn Overall -e April_2024 &
# python3 "${script_filepath}"/methane_mongoupload.py  -c /dev/ttyUSB7  -f $data_filepath -n 2 -cn Overall -e April_2024 &

# #Bin no.3
# python3 "${script_filepath}"/EZO_CO2_mongoupload.py  -c /dev/ttyUSB8  -f $data_filepath -n 3 -cn Overall -e April_2024 &
# python3 "${script_filepath}"/EZO_O2_mongoupload.py   -c /dev/ttyUSB9  -f $data_filepath -n 3 -cn Overall -e April_2024 &
# python3 "${script_filepath}"/RedBoard_mongoupload.py -c /dev/ttyUSB10 -f $data_filepath -n 3 -cn Overall -e April_2024 &
# python3 "${script_filepath}"/methane_mongoupload.py  -c /dev/ttyUSB11 -f $data_filepath -n 3 -cn Overall -e April_2024 &

# #Bin no.4
# python3 "${script_filepath}"/EZO_CO2_mongoupload.py  -c /dev/ttyUSB12 -f $data_filepath -n 4 -cn Overall -e April_2024 &
# python3 "${script_filepath}"/EZO_O2_mongoupload.py   -c /dev/ttyUSB13 -f $data_filepath -n 4 -cn Overall -e April_2024 &
# python3 "${script_filepath}"/RedBoard_mongoupload.py -c /dev/ttyUSB14 -f $data_filepath -n 4 -cn Overall -e April_2024 &
# python3 "${script_filepath}"/methane_mongoupload.py  -c /dev/ttyUSB15 -f $data_filepath -n 4 -cn Overall -e April_2024 &


#echo /home/"${user}"/test/test_too
/home/compostmonitor/GitHub_Repositories/Compost-Monitor/Python_Code/Sensor_Scripts/Launchers/Launch_Bin_1.sh
/home/compostmonitor/GitHub_Repositories/Compost-Monitor/Python_Code/Sensor_Scripts/Launchers/Launch_Bin_2.sh
/home/compostmonitor/GitHub_Repositories/Compost-Monitor/Python_Code/Sensor_Scripts/Launchers/Launch_Bin_3.sh
/home/compostmonitor/GitHub_Repositories/Compost-Monitor/Python_Code/Sensor_Scripts/Launchers/Launch_Bin_4.sh