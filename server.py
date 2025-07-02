"""
Flask application for performing emotion detection on user-provided text.

This app exposes a single route (`/emotionDetector`) that accepts a GET request
with a `textToAnalyze` query parameter, sends it to the external Watson NLP 
sentiment API via the `emotion_detector()` function, and returns a formatted
summary of the detected emotions. Handles and reports appropriate HTTP and 
application-level errors.
"""

from flask import Flask, request, render_template
import requests
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/emotionDetector")
def do_emotion_detection():
    """
    Handle GET requests for emotion detection on input text.

    Extracts `textToAnalyze` from the query string, calls the 
    `emotion_detector()` function to analyze emotions using an external service,
    and returns a formatted string summarizing the results.

    Returns:
        str: A natural language summary of emotion analysis if successful.
        tuple: Error message and status code if an error occurs.
    """

    text_to_analyze = request.args.get("textToAnalyze")
    try:
        results = emotion_detector(text_to_analyze)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            results = {'anger': None, 'disgust': None, 'fear': None,
            'joy': None, 'sadness': None, 'dominant_emotion': None}
            if results['dominant_emotion'] is None:
                return "Invalid text! Please try again!", 400
        else:
            return e.response.text, e.response.status_code

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
