

import time
import cv2
from firebase import upLoadLocation
from detect import Camera, ImageDetector
from ultrasonic import getDistance
from utils import visualize

debug = False

cam = Camera()
detector = ImageDetector('efficientdet_lite0.tflite', 3)

detector.loadModel()

while True: 
	
	distance = getDistance()
	upLoadLocation()
	if distance > 20:
		cv2.destroyAllWindows()
		# if we don't detect any object's in front 
		# we'll wait for 1 seconds before trying 
		# to detect any other images
		time.sleep(1)
		continue
	
	print("Obect detected %.2f cm from sensor"%(distance))
	image = cam.getImage()
	
	detection_start = time.time()
	objects = detector.detectFrom(image)
	detection_end = time.time()
	
	print("Object detection took %d seconds"%(detection_end - detection_start))
	
	detections = objects.detections
	
	if len(detections) == 0:
		print("No objects detected from image")
		time.sleep(1)
		continue
	
	labelsDetected = [ obj.categories[0].category_name + " (%.2f)"% obj.categories[0].score   for obj in detections ]
	print("objects", labelsDetected)
	
	if debug:
		annotaedImage = visualize(image, objects)
		cv2.imshow('AnnotageImage', annotaedImage)
		cv2.waitKey(1)
	
