# Upload data to meilisearch
import meilisearch
import json
import os


client = meilisearch.Client('https://ms-cd3d65ab69ae-7424.sgp.meilisearch.io', 'e17ddafe4eea648822355f14d326b3a478bd7141')
# An index is where the documents are stored.
# index = client.index('ocr')
save_path_ocr = r"C:\Users\admin\Projects\AIC\DATA\ocr\final_ocr.json"
save_path_asr = r"C:\Users\admin\Projects\AIC\DATA\asr\final_asr.json"

print(client.is_healthy())

# # ocr
json_file = open(save_path_ocr, encoding='utf-8')
text = json.load(json_file)
client.index('ocr').add_documents(text)

#asr
json_file = open(save_path_asr, encoding='utf-8')
text = json.load(json_file)
client.index('asr').add_documents(text)