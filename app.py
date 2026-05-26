from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "JARVIS backend is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "")

    response = ollama.chat(
        model="gemma:2b",
        messages=[
            {
                "role": "user",
                "content": msg
            }
        ]
    )

    reply = response["message"]["content"]

    return jsonify({
        "reply": reply
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)