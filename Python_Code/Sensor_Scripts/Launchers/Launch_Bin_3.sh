user=$(whoami)
data_filepath=/home/"${user}"/CompostingData/
script_filepath=/home/"${user}"/GitHub_Repositories/Compost-Monitor/Python_Code/Sensor_Scripts
script_filepath2=/home/"${user}"/GitHub_Repositories/Compost-Monitor/Python_Code/SQL
python3 "${script_filepath2}"/CO2_sqlUpload.py  -c /dev/ttyUSB0 -f $data_filepath -n 3 &
python3 "${script_filepath2}"/O2_sqlUpload.py   -c /dev/ttyUSB1  -f $data_filepath -n 3 &
python3 "${script_filepath2}"/RedBoard_sqlUpload.py -c /dev/ttyUSB2 -f $data_filepath -n 3 &
python3 "${script_filepath2}"/CH4_sqlUpload.py  -c /dev/ttyUSB3 -f $data_filepath -n 3 &