python3 plotting.py -s TVOC_Con -n 500000 &
python3 plotting.py -s CO2_Con -n 500000 &
python3 plotting.py -s O2_Con -n 500000 &

wait

python3 plotting.py -s BME_Humidity -n 500000 &
python3 plotting.py -s BME_Temp -n 500000 &

wait

python3 plotting.py -s BME_Pressure -n 500000 &
python3 plotting.py -s Methane_Con -n 500000 &

echo "bash_plot.sh has completed its work."