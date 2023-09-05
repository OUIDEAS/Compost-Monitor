python3 plotting.py -s TVOC_Con &
python3 plotting.py -s CO2_Con &

wait

python3 plotting.py -s BME_Humidity &
python3 plotting.py -s BME_Temp &

wait

python3 plotting.py -s BME_Pressure &
python3 plotting.py -s Methane_Con &

wait

python3 plotting.py -s O2_Con &

echo "bash_plot.sh has completed its work."