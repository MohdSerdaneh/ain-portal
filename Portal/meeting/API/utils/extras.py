import cv2 as cv
import mediapipe as mp


def main():
    """
    Starts a live webcam stream and uses MediaPipe to detect and display hand landmarks in real-time.
    Useful for visual debugging or verifying hand detection.
    """

    # Initialize MediaPipe's Hands module
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    mp_draw = mp.solutions.drawing_utils

    # Set up webcam input (camera 0)
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 540)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB as required by MediaPipe
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # If hand landmarks are detected, draw them on the original frame
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
                )

        # Show the frame in a window
        cv.imshow("Hand Landmarks", frame)

        # Exit if ESC is pressed
        if cv.waitKey(1) & 0xFF == 27:
            break

    # Release resources
    cap.release()
    cv.destroyAllWindows()


# Entry point
if __name__ == "__main__":
    main()
