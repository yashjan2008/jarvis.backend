from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

client = Groq(
    api_key="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"
)

@app.route("/")
def home():
    return "JARVIS backend is running!"

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    msg = data.get("message", "")

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are JARVIS, a smart AI assistant."
            },
            {
                "role": "user",
                "content": msg
            }
        ]
    )

    reply = response.choices[0].message.content

    return jsonify({
        "reply": reply
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
