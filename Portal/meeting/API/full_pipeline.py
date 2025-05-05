import copy
import datetime
import time
import cv2
import csv
import os
import pyttsx3
import requests
from asl_detector import ASLDetector
from emotion_detector import EmotionDetector
from utils.utils import log_interaction
from reports.generate_session_report import SessionReport
from utils.cvfpscalc import CvFpsCalc


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()


def save_to_file(text, room_name):
    reports_dir = os.path.join("meeting", "API", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    with open(os.path.join(reports_dir, f"latest_sentence_{room_name}.txt"), "w", encoding="utf-8") as f:
        f.write(text)


def save_chat_history(sentence, emotion, sender="Student", receiver="Teacher", room_name="default_meeting"):
    chatlogs_dir = os.path.join("meeting", "API", "chatlogs")
    os.makedirs(chatlogs_dir, exist_ok=True)
    chat_log_path = os.path.join(chatlogs_dir, f"{room_name}.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(chat_log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {sender}: {sentence}\n")



def send_to_chat(text):
    try:
        data = {"sender": "ASL_Bot", "receiver": "teacher", "message": text}
        requests.post("http://127.0.0.1:8000/meeting/chat/send/", json=data)
    except Exception as e:
        print(f"[Chat Error]: {e}")


def run_full_pipeline(room_name="default_meeting"):
    asl_detector = ASLDetector()
    emotion_detector = EmotionDetector()
    fps_calc = CvFpsCalc(buffer_len=10)

    print("🔍 Trying to open camera...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("❌ Failed to open camera.")
        return
    print("✅ Camera opened successfully!")

    label_path = os.path.join("model", "keypoint_classifier", "keypoint_classifier_label.csv")
    with open(label_path, encoding="utf-8-sig") as f:
        keypoint_classifier_labels = [row[0] for row in csv.reader(f)]

    last_sentence = ""

    try:
        while True:
            ret, image = cap.read()
            if not ret or image is None:
                print("⚠️ Failed to read frame from camera.")
                break

            image = cv2.flip(image, 1)
            debug_image = copy.deepcopy(image)

            hand_sign_text = None
            num_hands = 0

            hand_results = asl_detector.detect(debug_image)
            if hand_results.multi_hand_landmarks:
                num_hands = len(hand_results.multi_hand_landmarks)
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    landmarks = asl_detector.calc_landmark_list(debug_image, hand_landmarks)
                    processed = asl_detector.pre_process_landmark(landmarks)
                    gesture_index = asl_detector.keypoint_classifier(processed)
                    hand_sign_text = keypoint_classifier_labels[gesture_index]

            sentence = asl_detector.process_gesture(hand_sign_text, num_hands)

            emotions = emotion_detector.detect(debug_image)
            emotion = emotions[0] if emotions else "No face"
            confidence_score = emotion_detector.get_emotion_confidence(debug_image)

            if sentence != last_sentence and sentence.strip().endswith("."):
                speak(sentence.strip())
                save_to_file(f"{sentence.strip()} ({emotion})", room_name)
                save_chat_history(sentence.strip(), emotion, sender="Student", receiver="Teacher", room_name=room_name)
                send_to_chat(sentence.strip())
                last_sentence = sentence

                feedback = emotion_detector.check_emotion_context(sentence.strip(), emotion)
                print("[Feedback]:", feedback)

                log_interaction(
                    hand_sign_text or "None",
                    emotion,
                    sentence,
                    confidence_score,
                    feedback
                )

            fps = fps_calc.get()
            cv2.putText(debug_image, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4)
            cv2.putText(debug_image, f"Gesture: {hand_sign_text or 'No gesture'}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (0, 255, 0), 2)
            cv2.putText(debug_image, f"Emotion: {emotion}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(debug_image, f"Sentence: {sentence}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255),
                        2)

            cv2.imshow("ASL + Emotion Detection", debug_image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        report = SessionReport()
        report.export_pdf()


if __name__ == "__main__":
    try:
        run_full_pipeline()
    except Exception as e:
        print(f"💥 Error occurred: {e}")
