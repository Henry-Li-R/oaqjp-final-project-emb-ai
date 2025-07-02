from flask import Flask, request, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/emotionDetector", methods=["GET"])
def do_emotion_detection():
    text_to_analyze = request.args.get("textToAnalyze")
    results = emotion_detector(text_to_analyze)
    formatted_response = (
    f"For the given statement, the system response is "
    f"'anger': {results['anger']}, "
    f"'disgust': {results['disgust']}, "
    f"'fear': {results['fear']}, "
    f"'joy': {results['joy']} and "
    f"'sadness': {results['sadness']}. "
    f"The dominant emotion is {results['dominant_emotion']}."
    )
    return formatted_response

