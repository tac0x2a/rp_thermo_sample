#!/bin/sh

cd /home/pi/source/thermo
#python3 ./sample_thermo.py | tee -a `date +%Y%m%e%H%M%S`.txt
python3 ./sample_thermo.py >> thermo.csv
