user=$(whoami)
data_filepath=/home/"${user}"/CompostingData/
script_filepath=/home/"${user}"/GitHub_Repositories/Compost-Monitor/Python_Code/Sensor_Scripts
python3 "${script_filepath}"/EZO_CO2_mongoupload.py  -c /dev/ttyUSB10  -f $data_filepath -n 3 -cn Jun28Experiment -e June_2024 &
python3 "${script_filepath}"/EZO_O2_mongoupload.py   -c /dev/ttyUSB11  -f $data_filepath -n 3 -cn Jun28Experiment -e June_2024 &
python3 "${script_filepath}"/RedBoard_mongoupload.py -c /dev/ttyUSB2 -f $data_filepath -n 3 -cn Jun28Experiment -e June_2024 &
python3 "${script_filepath}"/methane_mongoupload.py  -c /dev/ttyUSB12 -f $data_filepath -n 3 -cn Jun28Experiment -e June_2024 &