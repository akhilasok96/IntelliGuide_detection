#Raspberry Pi 4.0 code for interfacing with ultrasonic sensor

import RPi.GPIO as GPIO
import time
import utils


                 
#Activates broadcom chip specific pin numbers.
#GPIO.setmode (GPIO.BOARD) -activates board pin numbers.                          

TRIG_PIN=11 #assign TRIG_PIN variable to GPIO pin 11
ECHO_PIN=6           #assign ECHO_PIN variable to GPIO pin 12


#calculate and display the distance

def getDistance():
	GPIO.setmode (GPIO.BCM)
	GPIO.setup(TRIG_PIN,GPIO.OUT)  #trig pin is output
	GPIO.setup(ECHO_PIN,GPIO.IN)  #echo pin is input
	# set Trigger to HIGH
	GPIO.output(TRIG_PIN, True) 
    # set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(TRIG_PIN, False)
	StartTime = time.time()
	StopTime = time.time()
    # save StartTime
	while GPIO.input(ECHO_PIN) == 0:
		StartTime = time.time() 
		# save time of arrival
	while GPIO.input(ECHO_PIN) == 1:
		StopTime = time.time()
 
    # time difference between start and arrival
	TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
	distance = (TimeElapsed * 34300) / 2
	GPIO.cleanup()
	return distance

def sayDistance() :
	dist=getDistance()
	text="Object is at %.2f cm from the ultrasonic sensor "%(dist)
	print(text)
	utils.speak(text)

