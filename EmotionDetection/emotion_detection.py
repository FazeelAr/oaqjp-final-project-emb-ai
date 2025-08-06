# EmotionDetection/emotion_detection.py
import joblib
import os

# Load your trained pipeline once
model_path = os.path.join(os.path.dirname(__file__), "rf_emotion_model.pkl")
model = joblib.load(model_path)

def emotion_detector(text):
    try:
        # Predict emotion probabilities
        probs = model.predict_proba([text])[0]
        classes = model.classes_

        # Format into Watson-style response
        scores = {cls: round(prob, 2) for cls, prob in zip(classes, probs)}

        # Fill in missing Watson emotions
        all_emotions = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'love']
        result = {emotion: scores.get(emotion, 0.0) for emotion in all_emotions}

        # Determine dominant emotion
        dominant = max(result, key=result.get)
        result['dominant_emotion'] = dominant

        return result

    except Exception as e:
        print("Emotion detection error:", e)
        return {
            'anger': 0, 'disgust': 0, 'fear': 0,
            'joy': 0, 'sadness': 0, 'surprise': 0,
            'love': 0, 'dominant_emotion': None
        }
