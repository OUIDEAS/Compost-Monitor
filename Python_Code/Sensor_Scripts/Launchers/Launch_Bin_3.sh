user=$(whoami)
filepath=/home/"${user}"/CompostingData/
python3 EZO_CO2_mongoupload.py  -c /dev/ttyUSB8  -f $filepath -n 3 -cn Overall -e April_2024
python3 EZO_O2_mongoupload.py   -c /dev/ttyUSB9  -f $filepath -n 3 -cn Overall -e April_2024
python3 RedBoard_mongoupload.py -c /dev/ttyUSB10 -f $filepath -n 3 -cn Overall -e April_2024
python3 methane_mongoupload.py  -c /dev/ttyUSB11 -f $filepath -n 3 -cn Overall -e April_2024