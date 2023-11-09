import numpy as np
import torch
from PIL import Image
import clip
import os
import skimage
import matplotlib.pyplot as plt
import json

# LOAD CLIP_FEATURE
feature_folder_path = r'C:\Users\admin\Projects\AIC\DATA\clip-features-vit-b32'

array_list = []

for file_name in os.listdir(feature_folder_path):
    if file_name.endswith(".npy"):
        file_path = os.path.join(feature_folder_path, file_name)
        array = np.load(file_path)
        array_list.append(array)

clip_feature = np.concatenate(array_list, axis=0)
print(clip_feature.shape)

# LOAD IMG_PATH
image_path_dict = r"C:\Users\admin\Projects\AIC\new_features.json"

# Đọc nội dung từ tệp tin JSON và chuyển đổi thành từ điển
with open(image_path_dict, "r") as json_file:
    image_path = json.load(json_file)
print(len(image_path))


# LOAD MODEL

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)

model, preprocess = clip.load("ViT-B/32")
model.to(device).eval()

text = "a dolphin and pink ball" 
# Keyframe = "L01_V001/0147.jpg"
text_tokens = clip.tokenize([text]).to(device)# (1,77)

with torch.no_grad():
    text_features = model.encode_text(text_tokens).float() #(1,512)


text_features /= text_features.norm(dim=-1, keepdim=True)
print("clip_feature: ",clip_feature.shape) # SHAPE(246,512)
print("image_feature: ",text_features.shape) 


# CALCULATE DISTANCE
distance = np.linalg.norm(clip_feature - text_features.cpu().numpy(),axis = 1 )
print(distance.shape)


# SHOW RESULT
k = 40
ids = np.argsort(distance)[:k]
# print(ids)

result = [(image_path[str(id)],distance[id]) for id in ids]


axes = []
grid_size = k//8
fig = plt.figure(figsize=(10,5))

for id in range(k):
    draw_image = result[id]
    axes.append(fig.add_subplot(grid_size + 1, 8, id+1))
    axes[-1].set_title(draw_image[0][-17:-4])
    axes[-1].set_xticks([])
    axes[-1].set_yticks([])
    plt.imshow(Image.open(draw_image[0]))


fig.tight_layout()
plt.show()