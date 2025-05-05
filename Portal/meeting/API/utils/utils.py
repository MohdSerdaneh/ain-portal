import csv
import time
import cv2
import numpy as np


def log_interaction(gesture, emotion, sentence, confidence, feedback=""):
    """
    Logs interaction data (gesture, emotion, sentence, etc.) to a CSV file.
    Used to track user sessions and for generating session reports.

    Params:
    - gesture (str): Recognized ASL gesture
    - emotion (str): Detected facial emotion
    - sentence (str): Constructed sentence from gestures
    - confidence (float): Confidence score of emotion detection
    - feedback (str): Optional system feedback message
    """
    timestamp = int(time.time())
    with open("../interaction_log.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, gesture, emotion, sentence, confidence, feedback])



