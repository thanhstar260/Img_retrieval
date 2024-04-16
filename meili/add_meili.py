# Upload data to meilisearch
import meilisearch
import json
import os


client = meilisearch.Client('https://ms-771a4545fc1a-8932.sgp.meilisearch.io', 'a7aa95f4dd64d9a82a0c56e60955f01db6145cfc')
# An index is where the documents are stored.
# index = client.index('ocr')
save_path_ocr = r"C:\Users\admin\Projects\AIC\DATA\ocr\final_ocr.json"
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