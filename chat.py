from dotenv import load_dotenv
load_dotenv()

import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

conversation_history = []

def ask(user_message):
    conversation_history.append({"role": "user", "parts": [{"text": user_message}]})

    response = client.models.generate_content(
         model="gemini-3.1-flash-lite",
        contents=conversation_history
    )

    conversation_history.append({"role": "model", "parts": [{"text": response.text}]})

    return response.text

# This is the new part — a loop that keeps asking YOU for input
print("Chat with your AI agent! Type 'quit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    reply = ask(user_input)
    print("Agent:", reply)
    print()