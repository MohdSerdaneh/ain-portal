from collections import deque
import cv2 as cv


class CvFpsCalc:
    """
    A utility class to calculate frames per second (FPS) using OpenCV's timing functions.

    This class is especially useful for real-time computer vision applications like ASL detection,
    where maintaining and displaying performance metrics such as FPS can help with debugging and tuning.

    Attributes:
        buffer_len (int): Number of recent frame times to average over for smoothing the FPS output.
    """

    def __init__(self, buffer_len=1):
        # Initialize the starting tick count
        self._start_tick = cv.getTickCount()
        # Convert tick frequency to milliseconds
        self._freq = 1000.0 / cv.getTickFrequency()
        # Use a deque to store the most recent frame durations
        self._difftimes = deque(maxlen=buffer_len)

    def get(self):
        """
        Calculates the average FPS based on the stored frame durations.

        Returns:
            float: Rounded FPS value.
        """
        # Get current tick
        current_tick = cv.getTickCount()
        # Calculate time difference in ms since last frame
        different_time = (current_tick - self._start_tick) * self._freq
        self._start_tick = current_tick

        # Store time difference to smooth out FPS
        self._difftimes.append(different_time)

        # Calculate FPS from the average of stored frame durations
        fps = 1000.0 / (sum(self._difftimes) / len(self._difftimes))
        fps_rounded = round(fps, 2)

        return fps_rounded
