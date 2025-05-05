import os
from django.http import JsonResponse
from django.conf import settings
from transformers import pipeline
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

# Load HuggingFace sentiment analyzer once
sentiment_analyzer = pipeline("sentiment-analysis")

def live_status(request, room_name):
    """
    Returns the latest detected sentence, emotion, and feedback for a given room.
    """
    latest_sentence_file = os.path.join(settings.BASE_DIR, 'meeting', 'API', 'reports', f'latest_sentence_{room_name}.txt')

    if not os.path.exists(latest_sentence_file):
        return JsonResponse({
            "sentence": "Waiting for input...",
            "emotion": "Unknown",
            "feedback": "No feedback yet."
        })

    try:
        with open(latest_sentence_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except Exception as e:
        print(f"[Live Status Error]: {e}")
        content = ""

    if "(" in content and ")" in content:
        sentence_part = content[:content.rfind("(")].strip()
        emotion_part = content[content.rfind("(")+1:content.rfind(")")]
    else:
        sentence_part = content
        emotion_part = "Unknown"

    feedback = "No feedback available"

    try:
        if sentence_part and emotion_part:
            sentiment = sentiment_analyzer(sentence_part)[0]["label"]

            emotion = emotion_part.lower()

            if sentiment == "POSITIVE" and emotion in ["happy", "surprised"]:
                feedback = "✅ Sentiment and emotion align."
            elif sentiment == "NEGATIVE" and emotion in ["angry", "sad"]:
                feedback = "✅ Sentiment and emotion align."
            elif emotion == "neutral":
                feedback = "➖ Neutral detected."
            else:
                feedback = "⚠️ Mismatch: Sentiment (" + sentiment + ") vs Emotion (" + emotion + ")"
    except Exception as e:
        feedback = "Error analyzing sentiment."

    return JsonResponse({
        "sentence": sentence_part,
        "emotion": emotion_part,
        "feedback": feedback
    })

def get_chat_history(request, room_name):
    """
    Return chat history for the given room.
    """
    chat_log_path = os.path.join(settings.BASE_DIR, 'meeting', 'API', 'chatlogs', f'{room_name}.txt')

    messages = []
    if os.path.exists(chat_log_path):
        try:
            with open(chat_log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line:
                        messages.append(line)
        except Exception as e:
            print(f"[Chat History Error]: {e}")

    return JsonResponse({"messages": messages})

@csrf_exempt
def send_message(request, room_name):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            if message:
                chat_log_path = os.path.join(settings.BASE_DIR, 'meeting', 'API', 'chatlogs', f'{room_name}.txt')
                os.makedirs(os.path.dirname(chat_log_path), exist_ok=True)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(chat_log_path, "a", encoding="utf-8") as f:
                    f.write(f"[{timestamp}] Teacher: {message}\n")
            return JsonResponse({"status": "success"})
        except Exception as e:
            print(f"[Send Message Error]: {e}")
            return JsonResponse({"status": "error"}, status=500)
    return JsonResponse({"status": "bad request"}, status=400)
