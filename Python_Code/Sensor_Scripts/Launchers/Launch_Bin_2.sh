user=$(whoami)
data_filepath=/home/"${user}"/CompostingData/
script_filepath=/home/"${user}"/GitHub_Repositories/Compost-Monitor/Python_Code/Sensor_Scripts
python3 "${script_filepath}"/EZO_CO2_mongoupload.py  -c /dev/ttyUSB4  -f $filepath -n 2 -cn Overall -e April_2024
python3 "${script_filepath}"/EZO_O2_mongoupload.py   -c /dev/ttyUSB5  -f $filepath -n 2 -cn Overall -e April_2024
python3 "${script_filepath}"/RedBoard_mongoupload.py -c /dev/ttyUSB6  -f $filepath -n 2 -cn Overall -e April_2024
python3 "${script_filepath}"/methane_mongoupload.py  -c /dev/ttyUSB7  -f $filepath -n 2 -cn Overall -e April_2024