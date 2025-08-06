import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.utils import resample
from datasets import load_dataset
from sklearn.linear_model import LogisticRegression
import joblib

go_emotions = load_dataset("go_emotions", split="train")
df = go_emotions.to_pandas()

label_map = {
    'admiration': 'joy', 'amusement': 'joy', 'approval': 'joy',
    'gratitude': 'joy', 'joy': 'joy', 'love': 'love',
    'caring': 'love', 'desire': 'love', 'optimism': 'joy',
    'disappointment': 'sadness', 'grief': 'sadness', 'remorse': 'sadness',
    'anger': 'anger', 'annoyance': 'anger', 'disapproval': 'anger',
    'embarrassment': 'sadness', 'nervousness': 'fear', 'fear': 'fear',
    'confusion': 'surprise', 'surprise': 'surprise',
    'realization': 'surprise', 'curiosity': 'surprise',
    'sadness': 'sadness',
    'neutral': 'neutral'  
}

label_names = go_emotions.features['labels'].feature.names

def map_emotions(label_ids):
    emotions = [label_map.get(label_names[i]) for i in label_ids]
    emotions = [e for e in emotions if e is not None and e != 'neutral']
    return emotions[0] if emotions else None

df['emotion'] = df['labels'].apply(map_emotions)
df = df[['text', 'emotion']].dropna()

df = df[df['emotion'].isin(['joy', 'sadness', 'anger', 'fear', 'love', 'surprise'])]

def balance_classes(df):
    max_size = df['emotion'].value_counts().max()
    lst = [df]
    for class_index, group in df.groupby('emotion'):
        lst.append(group.sample(max_size - len(group), replace=True, random_state=42))
    return pd.concat(lst).sample(frac=1, random_state=42)

balanced_data = balance_classes(df)

X_train, X_test, y_train, y_test = train_test_split(
    balanced_data["text"], balanced_data["emotion"], test_size=0.2, random_state=42
)

pipe = Pipeline([
    ("tfidf", TfidfVectorizer(
        stop_words="english",
        max_features=5000,
        ngram_range=(1, 2),
        min_df=3
    )),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

pipe.fit(X_train, y_train)

y_pred = pipe.predict(X_test)
print(classification_report(y_test, y_pred))

joblib.dump(pipe, "rf_emotion_model.pkl")
