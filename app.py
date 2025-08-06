
from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector as detect_emotion

app = Flask(__name__)

@app.route('/emotionDetector', methods=['GET'])
def emotion_detector_route():
    text_to_analyze = request.args.get("textToAnalyze")
    if not text_to_analyze:
        return jsonify({"error": "No text provided"}), 400

    response = detect_emotion(text_to_analyze)

    if not response.get("dominant_emotion"):
        return jsonify({"error": "Could not detect emotion"}), 400

    return jsonify(response)




@app.route("/")
def render_index_page():
    """
    Render the main index page (HTML interface).
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=5000)
