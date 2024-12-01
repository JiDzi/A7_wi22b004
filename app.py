from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/analyze-sentiment", methods=["POST"])
def analyze_sentiment():
    text = request.json.get("text", "")
    if not text:
        return jsonify({"error": "Text is required"}), 400

    endpoint = os.getenv("AZ_ENDPOINT")
    key = os.getenv("AZ_KEY")
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    body = {"documents": [{"id": "1", "language": "en", "text": text}]}
    
    try:
        response = requests.post(f"{endpoint}/text/analytics/v3.1/sentiment", headers=headers, json=body)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)