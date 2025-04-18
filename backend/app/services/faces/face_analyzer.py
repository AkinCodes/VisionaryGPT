import cv2
import dlib
import face_recognition
import os
from typing import List, Dict

class FaceAnalyzer:
    def __init__(self):
        # Load the OpenCV pre-trained Haar Cascade model for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Initialize dlib face detector (optional, can be used for better face detection)
        self.face_detector = dlib.get_frontal_face_detector()

    def detect_faces(self, filepath: str) -> List[Dict]:
        """
        Detect faces in an image and return bounding boxes and confidence.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Image not found at {filepath}")

        # Load the image
        image = face_recognition.load_image_file(filepath)
        
        # Detect faces
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        # If no faces are detected, return an empty list
        if len(face_locations) == 0:
            return []

        results = []
        for (top, right, bottom, left), _ in zip(face_locations, face_encodings):
            face_info = {
                "box": [left, top, right, bottom], 
                "confidence": 1.0,  
                "name": "Unknown"  
            }
            results.append(face_info)

        return results
