from dotenv import load_dotenv, find_dotenv
import json
import cohere
import os
import sys
sys.path.append('.')

_ = load_dotenv(find_dotenv())  # read local .env file
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def translate(text_query):
    # return chat_completion.choices[0].message.content

    # This is your trial API key
    
    response = co.generate(
        model='command-r-plus',
        prompt=f"""Please answer briefly and do not use punctuation, translate the text delimited by triple backticks into English, only respond with the translated sentence and do not add anything else. If the sentence is in English, please respond with that sentence and nothing else.```{text_query}```""",
        max_tokens=300,
        temperature=0,
        k=0,
        stop_sequences=[],
        return_likelihoods='NONE')
    result = response.generations[0].text
    print('Prediction: {}'.format(result))
    return result

# viet_query = "thanh is stupid"
# eng_query = translate(viet_query)
# print(eng_query)

if __name__ == "__main__":
    text_query = input("Enter the text you want to translate: ")
    translate(text_query)