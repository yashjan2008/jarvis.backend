from flask import Flask, request, jsonify
from flask_cors import CORS

import ollama
import webbrowser
import os
from ddgs import DDGS

app = Flask(__name__)

CORS(app)

# ---------------- MEMORY ---------------- #

chat_history = [
    {
        "role": "system",
        "content":
        (
            "You are Jarvis, a futuristic AI assistant. "
            "You can speak English, Hindi and Hinglish naturally."
        )
    }
]

# ---------------- INTERNET SEARCH ---------------- #

def internet_search(query):

    results = DDGS().text(
        query,
        max_results=3
    )

    output = ""

    for result in results:

        output += (
            f"{result['title']}\n"
            f"{result['body']}\n\n"
        )

    return output

# ---------------- COMMANDS ---------------- #

def handle_command(prompt):

    prompt = prompt.lower()

    if "open google" in prompt:

        webbrowser.open("https://google.com")

        return "Opening Google"

    elif "open youtube" in prompt:

        webbrowser.open("https://youtube.com")

        return "Opening YouTube"

    elif "open notepad" in prompt:

        os.system("notepad")

        return "Opening Notepad"

    elif "open calculator" in prompt:

        os.system("calc")

        return "Opening Calculator"

    return None

# ---------------- AI CHAT ---------------- #

def ai_chat(prompt):

    global chat_history

    # COMMANDS
    command_reply = handle_command(prompt)

    if command_reply:
        return command_reply

    # REALTIME SEARCH
    realtime_keywords = [
        "latest",
        "current",
        "today",
        "news",
        "won",
        "weather",
        "score",
        "live"
    ]

    if any(
        word in prompt.lower()
        for word in realtime_keywords
    ):

        web_info = internet_search(prompt)

        prompt = (
            f"Using this real-time information:\n\n"
            f"{web_info}\n\n"
            f"Answer this question:\n{prompt}"
        )

    # MEMORY LIMIT
    chat_history = chat_history[-10:]

    chat_history.append({
        "role": "user",
        "content": prompt
    })

    response = ollama.chat(
        model="phi3",
        messages=chat_history
    )

    reply = response["message"]["content"]

    chat_history.append({
        "role": "assistant",
        "content": reply
    })

    return reply

# ---------------- API ROUTE ---------------- #

@app.route("/chat", methods=["POST"])

def chat():

    data = request.json

    user_message = data["message"]

    reply = ai_chat(user_message)

    return jsonify({
        "reply": reply
    })

# ---------------- RUN SERVER ---------------- #

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )