import cv2
import csv
import copy
from utils.cvfpscalc import CvFpsCalc
from utils import log_interaction

class UI:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.fps_calc = CvFpsCalc(buffer_len=10)
        self.keypoint_classifier_labels = self.load_keypoint_classifier_labels()
        self.last_sentence = ""

    def load_keypoint_classifier_labels(self):
        with open("model/keypoint_classifier/keypoint_classifier_label.csv", encoding="utf-8-sig") as f:
            keypoint_classifier_labels = csv.reader(f)
            return [row[0] for row in keypoint_classifier_labels]

    def draw_info(self, image, fps, gesture, emotion, sentence):
        cv2.putText(image, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4)
        cv2.putText(image, f"Gesture: {gesture}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(image, f"Emotion: {emotion}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(image, f"Sentence: {sentence}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    def run(self, asl_detector, emotion_detector):
        try:
            while True:
                ret, image = self.cap.read()
                if not ret:
                    break
                image = cv2.flip(image, 1)
                debug_image = copy.deepcopy(image)

                hand_sign_text = None
                num_hands = 0

                hand_results = asl_detector.detect(debug_image)
                if hand_results.multi_hand_landmarks:
                    num_hands = len(hand_results.multi_hand_landmarks)
                    for hand_landmarks in hand_results.multi_hand_landmarks:
                        landmark_list = asl_detector.calc_landmark_list(debug_image, hand_landmarks)
                        pre_processed_landmark_list = asl_detector.pre_process_landmark(landmark_list)
                        gesture_index = asl_detector.keypoint_classifier(pre_processed_landmark_list)
                        hand_sign_text = self.keypoint_classifier_labels[gesture_index]

                sentence = asl_detector.process_gesture(hand_sign_text, num_hands)

                emotions = emotion_detector.detect(debug_image)
                emotion = emotions[0] if emotions else "No face"

                fps = self.fps_calc.get()
                self.draw_info(debug_image, fps, hand_sign_text or "No gesture", emotion, sentence)

                log_interaction(hand_sign_text if hand_sign_text else "None", emotion, sentence, 0)

                cv2.imshow("ASL & Emotion Detection", debug_image)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    print("\n[INFO] 'q' key pressed. Exiting program...")
                    break

        except KeyboardInterrupt:
            print("\n[INFO] Keyboard Interrupt detected. Releasing camera...")
        finally:
            self.cap.release()
            cv2.destroyAllWindows()
            print("[INFO] Camera released successfully.")
