import json
from groq import Groq
import os
import sys
sys.path.append('.')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

client = Groq(
    api_key = os.getenv("GROQ_API_KEY"),
)

def translate(text_query):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"""Please answer briefly and do not use punctuation, translate the text delimited by triple backticks into English, 
            only respond with the translated sentence and do not add anything else.
            If the sentence is in English, please respond with that sentence and nothing else.```{text_query}```""",
        }
    ],
    model="llama3-70b-8192",
    temperature=0,
    )
    return chat_completion.choices[0].message.content

# viet_query = "thanh is stupid"
# eng_query = translate(viet_query)
# print(eng_query)