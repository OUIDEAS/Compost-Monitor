user=$(whoami)
filepath=/home/"${user}"/CompostingData/
python3 EZO_CO2_mongoupload.py  -c /dev/ttyUSB0  -f $filepath -n 1 -cn Overall -e April_2024
python3 EZO_O2_mongoupload.py   -c /dev/ttyUSB1  -f $filepath -n 1 -cn Overall -e April_2024
python3 RedBoard_mongoupload.py -c /dev/ttyUSB2  -f $filepath -n 1 -cn Overall -e April_2024
python3 methane_mongoupload.py  -c /dev/ttyUSB3  -f $filepath -n 1 -cn Overall -e April_2024