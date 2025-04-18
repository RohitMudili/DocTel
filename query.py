# query.py — Post-Surgery Recovery Assistant Chatbot (Terminal Version)

import pandas as pd
import os
import openai
import difflib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the chatbot dataset
df = pd.read_csv("chatbot_qa_data.csv")

# Clean up missing data
df.dropna(subset=['question_text', 'response_text'], inplace=True)
questions = df['question_text'].str.lower().tolist()

# Search for a matching question in the CSV
def search_local_response(user_input):
    matches = difflib.get_close_matches(user_input.lower(), questions, n=1, cutoff=0.6)
    if matches:
        match = matches[0]
        response = df[df['question_text'].str.lower() == match]['response_text'].values[0]
        return response
    return None

# Use OpenAI API if no match is found locally
def search_openai_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Change to "gpt-4" if needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant for breast cancer patients recovering from surgery."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
            max_tokens=150
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error accessing OpenAI API: {e}"

# Main loop to run chatbot in terminal
def run_chatbot():
    print("🩺 Post-Surgery Recovery Assistant (Type 'exit' to quit)\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'exit':
            print("Bot: Wishing you a smooth recovery! 💖")
            break

        # Try local response first
        response = search_local_response(user_input)
        if response:
            print(f"Bot: {response}")
        else:
            print("Bot: Let me check that for you...")
            response = search_openai_response(user_input)
            print(f"Bot: {response}")

# Run the chatbot
if __name__ == "__main__":
    run_chatbot()
