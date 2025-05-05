import pandas as pd
import matplotlib.pyplot as plt

def generate_emotion_trend():
    """
    Reads logged user interactions and generates a bar chart showing emotion frequency.
    """
    df = pd.read_csv("../interaction_log.csv", names=["Timestamp", "Gesture", "Emotion", "Sentence", "Confidence"])

    # Convert timestamp to readable format
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit='s')

    # Count occurrences of each emotion
    emotion_counts = df["Emotion"].value_counts()

    # Plot Emotion Trend
    plt.figure(figsize=(10, 5))
    emotion_counts.plot(kind="bar", color=['blue', 'red', 'green', 'yellow', 'purple', 'orange', 'cyan'])
    plt.xlabel("Emotion")
    plt.ylabel("Frequency")
    plt.title("User Emotion Trend Throughout Conversation")
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

generate_emotion_trend()
