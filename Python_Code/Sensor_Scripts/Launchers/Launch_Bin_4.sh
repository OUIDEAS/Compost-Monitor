user=$(whoami)
data_filepath=/home/"${user}"/CompostingData/
script_filepath=/home/"${user}"/GitHub_Repositories/Compost-Monitor/Python_Code/Sensor_Scripts
python3 "${script_filepath}"/EZO_CO2_mongoupload.py  -c /dev/ttyUSB13 -f $data_filepath -n 4 -cn Jun28Experiment -e June_2024 &
python3 "${script_filepath}"/EZO_O2_mongoupload.py   -c /dev/ttyUSB14 -f $data_filepath -n 4 -cn Jun28Experiment -e June_2024 &
python3 "${script_filepath}"/RedBoard_mongoupload.py -c /dev/ttyUSB3 -f $data_filepath -n 4 -cn Jun28Experiment -e June_2024 &
python3 "${script_filepath}"/methane_mongoupload.py  -c /dev/ttyUSB15 -f $data_filepath -n 4 -cn Jun28Experiment -e June_2024 &