user=$(whoami)
filepath=/home/"${user}"/CompostingData/
python3 EZO_CO2_mongoupload.py  -c /dev/ttyUSB12 -f $filepath -n 4 -cn Overall -e April_2024
python3 EZO_O2_mongoupload.py   -c /dev/ttyUSB13 -f $filepath -n 4 -cn Overall -e April_2024
python3 RedBoard_mongoupload.py -c /dev/ttyUSB14 -f $filepath -n 4 -cn Overall -e April_2024
python3 methane_mongoupload.py  -c /dev/ttyUSB15 -f $filepath -n 4 -cn Overall -e April_2024