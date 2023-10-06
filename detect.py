import cv2
import time
from picamera2 import Picamera2

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils
# import ultrasonic


class ImageDetector:
    def __init__(self, model_name, threads=4):
        self.model = model_name
        self.num_threads = threads
        
    def loadModel(self):
        print("loading yolo model")
        start = time.time()
        base_options = core.BaseOptions(file_name=self.model, 
                                        use_coral=False, num_threads=self.num_threads)
        detection_options = processor.DetectionOptions(max_results=8, score_threshold=.3)
        options = vision.ObjectDetectorOptions(base_options=base_options, 
                                                detection_options=detection_options)
        detector = vision.ObjectDetector.create_from_options(options)
        self.model = detector
        end = time.time()
        print("model lodaing took %d seconds"%(end - start))
    
    def detectFrom(self, image):
        imRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        imTensor = vision.TensorImage.create_from_array(imRGB)
        detections = self.model.detect(imTensor)
        return detections
    
    
    
class Camera:
    
    def __init__(self, width=640, height=480):
        cam = Picamera2()
        cam.preview_configuration.main.size=(width,height)
        cam.preview_configuration.main.format='RGB888'
        cam.preview_configuration.align()
        cam.configure("preview")
        
        self.cam = cam
        self.cam.start()
    
    def getImage(self, debug=False):
        img = self.cam.capture_array()
        if debug:
            cv2.imshow('ImagePreview', img)
            cv2.waitKey(1)
            
        return img
    
