# Upload data to meilisearch
import meilisearch
import json
import os
import sys
sys.path.append('..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
HTTP = os.getenv("HTTP")
MASTER_KEY = os.getenv("MASTER_KEY")

client = meilisearch.Client(HTTP, MASTER_KEY)
# An index is where the documents are stored.
# index = client.index('ocr')
save_path_ocr = r"C:\Users\admin\Projects\AIC\DATA\ocr\final_ocr_clean.json"
save_path_asr = r"C:\Users\admin\Projects\AIC\DATA\asr\final_asr.json"

print(client.is_healthy())


# ADD OCR
with open(save_path_ocr, 'r', encoding='utf-8') as f:
    data_ocr = json.load(f)

# Define batch size
batch_size = 1000

# Split data into batches and add them to MeiliSearch
for i in range(0, len(data_ocr), batch_size):
    batch = data_ocr[i:i + batch_size]
    try:
        client.index('ocr').add_documents(batch)
        print(f"Added batch {i//batch_size + 1} to MeiliSearch")
    except Exception as e:
        print(f"Error adding batch {i//batch_size + 1}: {e}")


# ADD ASR
with open(save_path_asr, 'r', encoding='utf-8') as f:
    data_asr = json.load(f)

for i in range(0, len(data_asr), batch_size):
    batch = data_asr[i:i + batch_size]
    try:
        client.index('asr').add_documents(batch)
        print(f"Added batch {i//batch_size + 1} to MeiliSearch")
    except Exception as e:
        print(f"Error adding batch {i//batch_size + 1}: {e}")