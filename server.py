"""Flask app for emotion detection using IBM Watson NLP service."""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector as detect_emotion

app = Flask(__name__)

@app.route('/emotionDetector', methods=['GET', 'POST'])
def emotion_detector_route():
    """
    Handle emotion detection requests via GET or POST.
    Returns a formatted string with emotion scores and dominant emotion.
    """
    text_to_analyze = request.args.get('textToAnalyze') or (
        request.get_json().get('textToAnalyze') if request.is_json else None
    )

    if not text_to_analyze:
        return "Invalid text! Please try again!", 400

    response = detect_emotion(text_to_analyze)

    if response['dominant_emotion'] is None:
        return "Invalid text! Please try again!", 400

    anger = response['anger']
    disgust = response['disgust']
    fear = response['fear']
    joy = response['joy']
    sadness = response['sadness']
    dominant = response['dominant_emotion']

    result = (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant}."
    )

    return result

@app.route("/")
def render_index_page():
    """
    Render the main index page (HTML interface).
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=8080)
