import os
import numpy as np
import tensorflow as tf


class KeyPointClassifier(object):
    """
    This class handles classification of hand keypoints using a pre-trained TensorFlow Lite (TFLite) model.
    It is a key component in the ASL (American Sign Language) recognition pipeline.
    """

    def __init__(self, model_path=None, num_threads=1):
        """
        Initializes the classifier by loading a TFLite model.

        Parameters:
        - model_path (str): Path to the TFLite model file. If None, uses the default file in the same directory.
        - num_threads (int): Number of threads to use for inference.
        """
        if model_path is None:
            model_path = os.path.join(
                os.path.dirname(__file__),
                "keypoint_classifier.tflite"
            )

        # Ensure the model file exists to prevent silent errors
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"❌ Model not found at: {model_path}")

        # Load the TFLite interpreter
        self.interpreter = tf.lite.Interpreter(
            model_path=model_path,
            num_threads=num_threads
        )
        self.interpreter.allocate_tensors()

        # Store tensor I/O details for later use
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def __call__(self, landmark_list):
        """
        Performs prediction on a given list of hand keypoints.

        Parameters:
        - landmark_list (list): A list of 2D normalized hand keypoints.

        Returns:
        - int: The predicted class index (gesture/ASL sign).
        """
        input_index = self.input_details[0]["index"]
        self.interpreter.set_tensor(
            input_index,
            np.array([landmark_list], dtype=np.float32)
        )
        self.interpreter.invoke()

        output_index = self.output_details[0]["index"]
        result = self.interpreter.get_tensor(output_index)

        # Return the index of the class with the highest probability
        return np.argmax(np.squeeze(result))
