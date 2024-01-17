<<<<<<< HEAD
import pandas as pd
import json

# Định nghĩa biến path và đuôi file mới
path_json = r"C:\Users\admin\Projects\AIC\image_path.json"
path_csv = r"C:\Users\admin\Projects\AIC\data.csv"

df = pd.read_csv(path_csv)
values = df['new_idx'].tolist()
with open(path_json) as json_file:
    json_data = json.load(json_file)
# keys = list(json_data.values())
keys = df['link'].tolist()
data = {}

print(len(keys))
print(len(values))

for i in range(len(keys)):
    key = values[i]
    value = keys[i]
    data[key] = value
    # data.append[result]

print(len(data))
with open("id2link.json", "w") as f:
    json.dump(data, f)

# print(value[:10])
# print(key[:10])
=======

from text import load_clip_feature, load_image_path, load_model, create_faiss_index, text2img, visualize
# from image import load_clip_feature, load_image_path, load_model, create_faiss_index, img2img, visualize
import torch
import meilisearch
import json
client = meilisearch.Client('https://edge.meilisearch.com', 'masterKey')
from PIL import Image
import os
import matplotlib.pyplot as plt
import json

# DEFINE PARAMETER

feature_folder_path = r'C:\Users\admin\Projects\AIC\DATA\clip-features-vit-b32'
image_path_dict = r"C:\Users\admin\Projects\AIC\image_path.json"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
K = 40

img_query_path = r"C:\Users\admin\Projects\AIC\DATA\Keyframes\Keyframes_L01\L01_V002\0019.jpg"
text_query = "a dolphin and a pink ball"

# LOAD CLIP_FEATURE
clip_feature = load_clip_feature(feature_folder_path)

# LOAD IMG_PATH
image_path = load_image_path(image_path_dict)

# LOAD MODEL
model,preprocess = load_model(device)

# CREATE FAISS INDEX
vector_db = create_faiss_index(clip_feature)

# TEST Query

result = text2img(model, text_query, K, device,vector_db)
# result = img2img(preprocess,model,img_query_path,K,device,vector_db)
visualize(result, K, image_path)
# json_file = open('new_file.json', encoding='utf-8')
# movies = json.load(json_file)
# client.index('test').add_documents(movies)

result = client.index("test").search(
    "Khai mạc lễ hội tết việt quý mão 2023",{"limit": 3}
)["hits"]
print(result)
>>>>>>> 1d06e5ac145c9c50d220484eef52b2db322204ff
