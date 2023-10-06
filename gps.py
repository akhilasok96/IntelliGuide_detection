import serial              
from time import sleep
import sys
import pynmea2


ser = serial.Serial ("/dev/ttyAMA0",baudrate=9600, timeout=0.5)
dataout = pynmea2.NMEAStreamReader()
def getCurrentLocation():
	while True:
		received_data = ser.readline()
		if received_data[0:6] == b"$GPRMC":
			newmsg=pynmea2.parse(received_data.decode())
			lat=newmsg.latitude
			lng=newmsg.longitude
			gps = "Latitude= %.6f longitude = %.6f" %(lat,lng)
			print(gps)
			return (lat,lng)
	
