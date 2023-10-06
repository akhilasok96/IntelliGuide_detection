from tflite_support.task import processor
import cv2
import numpy as np
from gtts import gTTS
import tempfile
import pygame

_MARGIN = 10
_ROW_SIZE = 10
_FONT_SIZE = 1
_FONT_THICKNESS = 1
_TEXT_COLOR = (0, 0, 255)

def speak(text):
    # Create a temporary WAV file to store the speech
    with tempfile.NamedTemporaryFile(delete=True) as temp_wav:
        tts = gTTS(text=text, lang='en')
        tts.save(temp_wav.name)

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(temp_wav.name)
        pygame.mixer.music.play()

        # Wait for speech to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

def CountFreq(li):
    freq = {}
    for items in li:
        freq[items] = li.count(items)
    a = str(freq)
    speak(a)

def visualize(
    image: np.ndarray,
    detection_result: processor.DetectionResult,
) -> np.ndarray:

    category_list = []
    for detection in detection_result.detections:

        bbox = detection.bounding_box
        start_point = bbox.origin_x, bbox.origin_y
        end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
        cv2.rectangle(image, start_point, end_point, _TEXT_COLOR, 3)

        category = detection.categories[0]
        category_name = category.category_name
        category_list.append(category_name)
        probability = round(category.score, 2)
        result_text = category_name + ' (' + str(probability) + ')'
        text_location = (_MARGIN + bbox.origin_x, _MARGIN + _ROW_SIZE + bbox.origin_y)
        cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)

    CountFreq(category_list)
    return image
