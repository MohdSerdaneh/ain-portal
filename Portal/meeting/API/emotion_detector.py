import cv2
import numpy as np
import csv
import os
from keras.models import load_model
from transformers import pipeline
import json
import pandas as pd
from datetime import datetime


class EmotionDetector:
    """
    Detects emotions from facial expressions using a CNN model,
    logs them, and provides sentiment-emotion mismatch feedback.
    """

    def __init__(self, meeting_name="default_meeting"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.face_cascade = cv2.CascadeClassifier(
            os.path.join(base_dir, "utils", "haarcascade_frontalface_default.xml")
        )
        self.emotion_model = load_model(os.path.join(base_dir, "model", "emotion_detection_model.h5"))

        self.emotion_labels = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']
        self.sentiment_analyzer = pipeline("sentiment-analysis")

        self.meeting_name = meeting_name
        self.csv_path = f"data/{self.meeting_name}.csv"
        self._initialize_csv()

    def _initialize_csv(self):
        """
        Ensures that the session data directory and log file exist.
        """
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["prediction", "time"])

    def _map_to_core_emotion(self, label):
        """
        Maps the 7-model emotion labels to a consistent 5-emotion set.
        """
        if label == "disgusted":
            return "angry"
        elif label == "fearful":
            return "surprised"
        return label

    def get_emotion_confidence(self, image):
        """
        Returns the confidence score for the most likely emotion detected in the frame.
        """
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
            confidences = []
            for (x, y, w, h) in faces:
                face_roi = gray[y:y+h, x:x+w]
                resized = cv2.resize(face_roi, (48, 48))
                reshaped = np.reshape(resized / 255.0, (1, 48, 48, 1))
                prediction = self.emotion_model.predict(reshaped)

                if not isinstance(prediction, np.ndarray) or np.isnan(prediction).any():
                    continue

                confidence = float(np.max(prediction))
                confidences.append(confidence)

            return max(confidences) if confidences else 0.0

        except Exception as e:
            print(f"[get_emotion_confidence ERROR]: {e}")
            return 0.0

    def detect(self, image, log=True):
        """
        Detects emotions from the given image and optionally logs them.
        """
        emotions = []
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)

            for (x, y, w, h) in faces:
                face_roi = gray[y:y+h, x:x+w]
                resized = cv2.resize(face_roi, (48, 48))
                reshaped = np.reshape(resized / 255.0, (1, 48, 48, 1))
                pred = self.emotion_model.predict(reshaped)

                if not isinstance(pred, np.ndarray) or np.isnan(pred).any():
                    continue

                emotion_index = np.argmax(pred)
                label = self.emotion_labels[emotion_index]
                mapped = self._map_to_core_emotion(label)
                emotions.append(mapped)

                if log:
                    self._log_emotion(mapped)

        except Exception as e:
            print(f"[Emotion Detection Error]: {e}")

        return emotions

    def _log_emotion(self, label):
        """
        Logs emotion label with timestamp to CSV.
        """
        if not label or not isinstance(label, str) or label.strip() == "":
            return
        timestamp = int(datetime.now().timestamp())
        with open(self.csv_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([label.strip(), timestamp])

    def check_emotion_context(self, sentence, detected_emotion):
        """
        Compares emotion and sentence sentiment for mismatches.
        """
        try:
            sentiment = self.sentiment_analyzer(sentence)[0]["label"]
        except Exception as e:
            return f"⚠️ Sentiment analysis failed: {e}"

        positive = ["happy", "surprised"]
        negative = ["angry", "sad"]

        if (sentiment == "POSITIVE" and detected_emotion in negative) or \
           (sentiment == "NEGATIVE" and detected_emotion in positive):
            return f"⚠️ Mismatch: Sentiment ({sentiment}) vs Emotion ({detected_emotion})"
        return "✅ Sentiment and emotion align."

    def generate_summary(self):
        """
        Returns a JSON summary of all detected emotions in the session.
        """
        try:
            if not os.path.exists(self.csv_path):
                return json.dumps({"summary": "CSV file not found."})

            df = pd.read_csv(self.csv_path)

            if "prediction" not in df.columns:
                return json.dumps({"summary": "Missing 'prediction' column."})

            # Clean the data before calling value_counts()
            df["prediction"] = df["prediction"].astype(str).str.strip()
            df = df[df["prediction"] != ""]
            df = df.dropna(subset=["prediction"])

            if df.empty:
                return json.dumps({"summary": "No valid predictions yet."})

            summary = df["prediction"].value_counts().to_dict()
            return json.dumps(summary)

        except Exception as e:
            return json.dumps({"error": f"generate_summary() failed: {e}"})

