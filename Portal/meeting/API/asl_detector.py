import copy
import itertools
import time
import cv2
import mediapipe as mp
from spellchecker import SpellChecker
from model.keypoint_classifier.keypoint_classifier import KeyPointClassifier


class ASLDetector:
    """
    Detects American Sign Language (ASL) gestures from webcam input using MediaPipe and a custom keypoint classifier.
    Converts recognized gestures into structured, spell-checked sentences.
    """

    def __init__(self):
        # Initialize MediaPipe hand detection
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )

        # Load the custom ASL classifier model
        self.keypoint_classifier = KeyPointClassifier()

        # Spell checker for finalized sentences
        self.spell = SpellChecker()

        # Sentence management
        self.current_sentence = ""
        self.last_finished_sentence = ""
        self.previous_gesture = None
        self.current_gesture = None

        # Gesture state control
        self.in_underscore = False  # If space was triggered
        self.word_started_after_space = False
        self.new_sentence_triggered = False
        self.hold_time_threshold = 1.5  # Hold time to confirm a gesture
        self.space_hold_threshold = 1.4  # Time to hold both hands for space
        self.gesture_start_time = None
        self.gesture_released = True
        self.last_detection_time = time.time()
        self.no_hand_threshold = 4  # Time without hand to end sentence
        self.both_hands_start_time = None

    def calc_landmark_list(self, image, landmarks):
        """
        Convert normalized landmark positions to pixel values.
        """
        image_width, image_height = image.shape[1], image.shape[0]
        return [[min(int(lm.x * image_width), image_width - 1),
                 min(int(lm.y * image_height), image_height - 1)]
                for lm in landmarks.landmark]

    def pre_process_landmark(self, landmark_list):
        """
        Normalize the landmark list to be relative and scaled.
        """
        temp = copy.deepcopy(landmark_list)
        base_x, base_y = temp[0][0], temp[0][1]
        for i, point in enumerate(temp):
            temp[i][0] -= base_x
            temp[i][1] -= base_y
        temp = list(itertools.chain.from_iterable(temp))
        max_val = max(map(abs, temp))
        return [n / max_val for n in temp]

    def save_chat(self, sentence):
        """
        Saves the final sentence to a local log file with timestamp.
        """
        with open("reports/logs/chat_log.txt", "a", encoding="utf-8") as f:
            timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
            f.write(f"{timestamp} {sentence}\n")

    def detect(self, image):
        """
        Run hand detection on the image frame.
        """
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return self.hands.process(rgb_image)

    def display_sentence(self):
        """
        Returns the sentence for display in the UI.
        """
        if self.current_sentence:
            return self.current_sentence + ("_" if self.in_underscore else "")
        elif self.last_finished_sentence:
            return self.last_finished_sentence
        return ""

    def process_gesture(self, hand_sign_text, num_hands):
        """
        Core method to manage gesture timing, state, and sentence building.
        """
        current_time = time.time()
        instant_letters = ["Z", "J"]  # Letters performed dynamically

        # === No hands detected ===
        if num_hands == 0:
            self.gesture_released = True
            if (current_time - self.last_detection_time) >= self.no_hand_threshold:
                if self.current_sentence:
                    final = self.current_sentence.strip("_ ") + "."
                    self.last_finished_sentence = final
                    self.save_chat(final)
                    print("💾 Saved Sentence:", final)
                    self.current_sentence = ""
                    self.in_underscore = False
                    self.word_started_after_space = False
                    self.new_sentence_triggered = True
            self.last_detection_time = current_time
            return self.display_sentence()

        # === Two hands trigger a space ===
        if num_hands == 2:
            self.gesture_released = True
            if self.both_hands_start_time is None:
                self.both_hands_start_time = current_time
            elif (current_time - self.both_hands_start_time) >= self.space_hold_threshold and not self.in_underscore:
                self.in_underscore = True
                print("␣ Space triggered")
            return self.display_sentence()
        else:
            self.both_hands_start_time = None

        # === No valid gesture detected ===
        if hand_sign_text is None:
            self.gesture_released = True
            return self.display_sentence()

        # === New gesture detected ===
        if hand_sign_text != self.current_gesture:
            self.current_gesture = hand_sign_text
            self.gesture_start_time = current_time
            self.gesture_released = True
            return self.display_sentence()

        # === Dynamic gesture (Z/J) detected ===
        if hand_sign_text in instant_letters:
            if self.gesture_released:
                self._append_gesture(hand_sign_text)
                self.gesture_released = False
            return self.display_sentence()

        # === Hold gesture long enough to be valid ===
        if (current_time - self.gesture_start_time) >= self.hold_time_threshold:
            if self.gesture_released:
                self._append_gesture(hand_sign_text)
                self.gesture_released = False
                self.gesture_start_time = current_time

        return self.display_sentence()

    def _append_gesture(self, gesture):
        """
        Appends the current gesture (letter) to the working sentence string.
        """
        if self.new_sentence_triggered:
            self.last_finished_sentence = ""
            self.new_sentence_triggered = False

        if self.in_underscore:
            self.current_sentence += " "
            self.in_underscore = False
            self.word_started_after_space = True

        self.current_sentence += gesture
        self.previous_gesture = gesture
