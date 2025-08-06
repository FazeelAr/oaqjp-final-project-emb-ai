import joblib

pipe = joblib.load("rf_emotion_model.pkl")

texts = [
    "I am so angry with what happened.",
    "This is amazing, I love it!",
    "Everything feels meaningless.",
    "I can't believe this happened!"
    "I'm terrified ocf what's going to happen.",
]

for text in texts:
    probs = pipe.predict_proba([text])[0]
    classes = pipe.classes_
    scores = {cls: round(prob, 2) for cls, prob in zip(classes, probs)}
    dominant = max(scores, key=scores.get)
    print(f"{text} → {dominant} 🔥 {scores}")
