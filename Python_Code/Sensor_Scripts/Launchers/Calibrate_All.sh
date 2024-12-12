user=compostmonitor
data_filepath=/home/"${user}"/CompostingData/
# script_filepath=/home/"${user}"/GitHub_Repositories/Compost-Monitor/Python_Code/Sensor_Scripts
script_filepath=/home/"${user}"/GitHub_Repositories/Compost-Monitor/Python_Code/Sensor_Scripts

device_filepath=/dev/serial/by-path
pci=pci-0000:00:14.0-usb-0:
port=:1.0-port0

# python3 "${script_filepath}"/O2_Cal.py   -c "${device_filepath}"/"${pci}"7.1.1"${port}"  -f $data_filepath -n 1 &
# python3 "${script_filepath}"/CO2_Cal.py  -c "${device_filepath}"/"${pci}"7.1.2"${port}" -f $data_filepath -n 1 &
# python3 "${script_filepath}"/CH4_Cal.py  -c "${device_filepath}"/"${pci}"7.1.4"${port}" -f $data_filepath -n 2 &


# python3 "${script_filepath}"/O2_Cal.py   -c "${device_filepath}"/"${pci}"7.2.1"${port}"  -f $data_filepath -n 2 &
# python3 "${script_filepath}"/CO2_Cal.py  -c "${device_filepath}"/"${pci}"7.2.2"${port}" -f $data_filepath -n 2 &
# python3 "${script_filepath}"/CH4_Cal.py  -c "${device_filepath}"/"${pci}"7.2.4"${port}" -f $data_filepath -n 2 &



python3 "${script_filepath}"/O2_Cal.py   -c "${device_filepath}"/"${pci}"7.3.1"${port}"  -f $data_filepath -n 3 &
# python3 "${script_filepath}"/CO2_Cal.py  -c "${device_filepath}"/"${pci}"7.3.2"${port}" -f $data_filepath -n 3 &
# python3 "${script_filepath}"/CH4_Cal.py  -c "${device_filepath}"/"${pci}"7.3.4"${port}" -f $data_filepath -n 2 &



# python3 "${script_filepath}"/O2_Cal.py   -c "${device_filepath}"/"${pci}"7.4.1"${port}"  -f $data_filepath -n 4 &
# python3 "${script_filepath}"/CO2_Cal.py  -c "${device_filepath}"/"${pci}"7.4.2"${port}" -f $data_filepath -n 4 &
# python3 "${script_filepath}"/CH4_Cal.py  -c "${device_filepath}"/"${pci}"7.4.4"${port}" -f $data_filepath -n 2 &


