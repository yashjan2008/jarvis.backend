from groq import Groq

client = Groq(
    api_key="YOUR_API_KEY"
)

def ai_chat(message):

    response = client.chat.completions.create(
        model="llama3-8b-8192",

        messages=[
            {
                "role": "system",
                "content": "You are JARVIS, a smart AI assistant."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    reply = response.choices[0].message.content

    return reply
