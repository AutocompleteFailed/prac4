#!/usr/bin/python
# Martin Flanagan FLNMAR011
import RPi.GPIO as GPIO
import time
import spidev
import os
import sys
from datetime import datetime

# Opening SPI bus
sp = spidev.SpiDev()
sp.open(0,0)
sp.max_speed_hz = 1000000

# setting up switches and interrupts
stop_s = 22
reset_s = 23
freq_s = 24
display_s = 25

pot_channel = 0
tempsens_channel = 1
ldr_channel = 2

list = [500, 1000, 2000]

frequency = 500
selection = 0

timer = 0
running = False
data_readings = ["0", "0", "0", "0", "0"]
readings = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setup of Pushbuttons
GPIO.setup(stop_s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 	# Stop switch
GPIO.setup(reset_s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 	# Reset switch
GPIO.setup(freq_s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 	# Frequency switch
GPIO.setup(display_s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 	# Display switch

# Events for pushbuttons
GPIO.add_event_detect(stop_s, GPIO.FALLING, callback=stop)
GPIO.add_event_detect(reset_s, GPIO.FALLING, callback=reset)
GPIO.add_event_detect(freq_s, GPIO.FALLING, callback=frequencyChange)
GPIO.add_event_detect(display_s, GPIO.FALLING, callback=display)

# conversion functions
def convertToVolts(data):
	v = (data*3.3) / float(1023)
	v = round(v,1)
	return v

def convertToDegreesCelsius(data):
	t = (((data)*3.3 / float(1023)) - 0.5)/0.01
	t = round(t,0)
	return t

def convertToLight(data):
	t = ((data) / float(1023))*100
	t = round(t,0)
	return t

def ReadData(ch):
	adc = sp.xfer2([1, (8+ch)<<4 ,0])
	data = ((adc[1]&3)<<8) +adc[2]
	return data

#Pushbutton methods
def stop(status):
	global running
	if (running == False):
		global readings
		running = True
		readings = 0
	else:
		running = False

def reset(status):
	global timer
	timer = 0
	# x = os.system("cls")		#Windows
	y = os.system("clear")		#Linux or Mac

def frequencyChange(status):
	global frequency
	global selection
	selection = selection + 1
	if (selection>2):
		selection = 0
	frequency = list[selection]

