user=$(whoami)
filepath=/home/"${user}"/CompostingData/
python3 EZO_CO2_mongoupload.py  -c /dev/ttyUSB4  -f $filepath -n 2 -cn Overall -e April_2024
python3 EZO_O2_mongoupload.py   -c /dev/ttyUSB5  -f $filepath -n 2 -cn Overall -e April_2024
python3 RedBoard_mongoupload.py -c /dev/ttyUSB6  -f $filepath -n 2 -cn Overall -e April_2024
python3 methane_mongoupload.py  -c /dev/ttyUSB7  -f $filepath -n 2 -cn Overall -e April_2024