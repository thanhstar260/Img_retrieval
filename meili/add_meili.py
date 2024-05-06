# Upload data to meilisearch
import meilisearch
import json
import os


client = meilisearch.Client('https://edge.meilisearch.com', 'bc61b7bb01eb45353ed231d2f88750729ddbbac9')
# An index is where the documents are stored.
# index = client.index('ocr')
# path = r"C:\Users\admin\Projects\AIC\DATA\ocr\text1"
save_path = r"C:\Users\admin\Projects\AIC\DATA\ocr\text2"
# save_path2 = r"C:\Users\admin\Projects\AIC\DATA\ocr\text3"


print(client.is_healthy())

for key_frame in os.listdir(save_path):
    key_frame_path = os.path.join(save_path, key_frame)
    for file in os.listdir(key_frame_path):
        file_path = os.path.join(key_frame_path,file)
        json_file = open(file_path, encoding='utf-8')
        text = json.load(json_file)
        client.index('ocr2').add_documents(text)
        # print(file_path)

