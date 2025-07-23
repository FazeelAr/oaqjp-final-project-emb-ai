import requests
import json

def emotion_detector(text_to_analyze):
    try:
        URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
        HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
        obj = { "raw_document": { "text": text_to_analyze } }

        response = requests.post(URL, headers=HEADERS, json=obj)
        data = json.loads(response.text)
        emo_scores = data['emotionPredictions'][0]['emotion']

        # 🏆 Find the dominant vibe
        dominant_emotion = max(emo_scores, key=emo_scores.get)

        # 🎁 Assemble the final dictionary
        result = {
            'anger':   emo_scores['anger'],
            'disgust': emo_scores['disgust'],
            'fear':    emo_scores['fear'],
            'joy':     emo_scores['joy'],
            'sadness': emo_scores['sadness'],
            'dominant_emotion': dominant_emotion
        }
        return result
    except Exception as e:
        print("Exception occurred", e)
        return {
            'anger':   0,
            'disgust': 0,
            'fear':    0,
            'joy':     0,
            'sadness': 0,
            'dominant_emotion': 0
        }
