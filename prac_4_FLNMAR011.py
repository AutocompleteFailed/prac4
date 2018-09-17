#!/usr/bin/python
# Martin Flanagan FLNMAR011
import RPi.GPIO as GPIO
import time
import spidev
import os
import sys
from datetime import datetime

# setting up switches and interrupts
stop_s = 22
reset_s = 23
freq_s = 24
display_s = 25

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