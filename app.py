from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "JARVIS backend is running!"

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    msg = data.get("message", "").lower()

    if "hello" in msg:
        reply = "Hello sir!"

    elif "who are you" in msg:
        reply = "I am JARVIS."

    elif "time" in msg:
        from datetime import datetime
        reply = datetime.now().strftime("%H:%M")

    else:
        reply = "I am still learning."

    return jsonify({
        "reply": reply
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
