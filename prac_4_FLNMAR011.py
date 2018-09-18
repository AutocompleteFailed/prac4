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

units = ['', '', 'V', 'C','%']

data_readings = [['00:00:00','00:00:00.0',0.0,'00.0',0], ['00:00:00','00:00:00.0',0.0,'00.0',0], ['00:00:00','00:00:00.0',0.0,'00.0',0], ['00:00:00','00:00:00.0',0.0,'00.0',0], ['00:00:00','00:00:00.0',0.0,'00.0',0]]
lines = [0,0,0,0,0]
readings = 0




GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setup of Pushbuttons
GPIO.setup(stop_s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 	# Stop switch
GPIO.setup(reset_s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 	# Reset switch
GPIO.setup(freq_s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 	# Frequency switch
GPIO.setup(display_s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 	# Display switch



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

def display(status):
    	#print("Display fxn")
        if running == False:
            Heading = "Time         Timer          Pot      Temp      Light"
            #units = ['', '', 'V', 'C','%']
            for i in range(len(lines)):
                lines[i] = linemaker(data_readings[i])
            print('{0}\n{1}\n{2}\n{3}\n{4}\n{5}'.format(Heading, lines[0], lines[1], lines[2], lines[3], lines[4]))
    

# Events for pushbuttons
GPIO.add_event_detect(stop_s, GPIO.FALLING, callback=stop)
GPIO.add_event_detect(reset_s, GPIO.FALLING, callback=reset)
GPIO.add_event_detect(freq_s, GPIO.FALLING, callback=frequencyChange)
GPIO.add_event_detect(display_s, GPIO.FALLING, callback=display)

    
def linemaker(arrayofstuff):
        global units
        line = str()
        for i in range(len(arrayofstuff)):
            line = line + str(arrayofstuff[i])+units[i] + "     "
        return(line)



def addReading(p, t, l):
	global timer
	global data_readings
	#str_x = print("%d\t%.1f V\t %d C\t %d%%" % (timer, p, t, l))
	hours, rem = divmod(timer,3600000000)
	mins, seconds = divmod(rem, 60000)
	seconds = float(seconds)/1000
	#print(seconds)
	#print(timer)
	timer_str = '{0:0>2}:{1:0>2}:{2:0>4}'.format(hours, mins, seconds)

	#print( '{:%H:%M:%S}'.format(datetime.now().time()) )
	#data = '{:%H:%M:%S} {:f} {:.1f}V {:f}C {:f}%'.format(datetime.now().time()), timer, p, t, l)
	data = ['{:%H:%M:%S}'.format(datetime.now().time()), timer_str, '{0:0>3}'.format(p), '{0:0>4}'.format(t), l]
	print (linemaker(data))
	#print("New reading..........")
	#print(datetime.now().time())
	#print("%d" % frequency)
	#print("%.1f V" % p)
	#print("%d C" % t)
	#print("%d%%" % l)
	del data_readings[4]  # remove oldest reading
	data_readings = [data] + data_readings # add newest to start of array
	
	
Heading = "Time         Timer          Pot      Temp      Light"
print (Heading)

while True:
	if(running):
		pot = ReadData(pot_channel)
		temp = ReadData(tempsens_channel)
		ldr = ReadData(ldr_channel)
		
		potV = convertToVolts(pot)
		tempC = convertToDegreesCelsius(temp)
		lightM = convertToLight(ldr)

		addReading(potV, tempC, lightM)
	timer = timer + frequency
	scnd = float(frequency)/1000
	time.sleep(scnd)

GPIO.cleanup()