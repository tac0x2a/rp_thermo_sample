#!/usr/bin/env python3

import time
import datetime as date
import sys
import spidev
import RPi.GPIO as GPIO


# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

V = 3.3

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])

  # 上位10bitを取り出す
  data = ((adc[1]&0x3) << 8) + adc[2]
  return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data, places):
  volts = V * data / float(2**10 - 1)
  volts = round(volts, places)
  return volts

# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def ConvertTemp(data,places):

  # ADC Value
  # (approx)  Temp  Volts
  #    0      -50    0.00
  #   78      -25    0.25
  #  155        0    0.50
  #  233       25    0.75
  #  310       50    1.00
  #  465      100    1.50
  #  775      200    2.50
  # 1023      280    3.30

  temp = ((data * V * 100)/float(2**10 - 1))-50
  temp = round(temp,places)
  return temp

# Define sensor channels
temp_channel  = 1

# Define delay between readings
delay = 10

# LedOutput
pin = 11
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

Samples = 50

delay_par_sample = delay / float(Samples)

try:
    GPIO.output(pin, 1)
    l = 0
    v = 0
    t = 0
    for i in range(Samples):

        # Read the temperature sensor data
        temp_level = ReadChannel(temp_channel)
        l += temp_level
        v += ConvertVolts(temp_level,2)
        t += ConvertTemp(temp_level,2)

        # Wait before repeating loop
        time.sleep(delay_par_sample)

    #print("--------------------------------------------")
    #oprint("Temp : {} ({}V) {} deg C".format( round(l/Samples,2), round(v/Samples,2), round(t/Samples,2) ))

    print("{},{},{},{}".format( date.datetime.now().strftime("%Y/%m/%e %H:%M:%S"), round(l/Samples,2), round(v/Samples,2), round(t/Samples,2) ))
    sys.stdout.flush()

    GPIO.output(pin, 0)
    time.sleep(1)


except KeyboardInterrupt: # Ctrl+C pressed, so…
#    print("\nExit...\n")
    GPIO.output(pin, 0)
    spi.close() # … close the port before exit
