import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import joblib



def main():
    data = pd.read_csv("emotions.csv", header=None, names=["text", "emotion"])

    data["text"] = data["text"].str.strip()
    data["emotion"] = data["emotion"].str.strip()

    X_train, X_test, y_train, y_test = train_test_split(
        data["text"], data["emotion"], test_size=0.2, random_state=42
    )

    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    clf = MultinomialNB()
    clf.fit(X_train_vec, y_train)

    y_pred = clf.predict(X_test_vec)
        # Save the model
    joblib.dump(clf, 'emotion_model.pkl')

    # Save the vectorizer
    joblib.dump(vectorizer, 'vectorizer.pkl')
    ## print(classification_report(y_test, y_pred))


if __name__ == '__main__':
    ## main()
    clf = joblib.load('emotion_model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')

    # Example prediction
    text = ["I feel bad today"]
    vec = vectorizer.transform(text)
    print(clf.predict(vec))  # Output: ['sadness'] or whatever it learned

