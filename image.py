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
image_paths_dict = r"C:\Users\admin\Projects\AIC\feature.json"

# Đọc nội dung từ tệp tin JSON và chuyển đổi thành từ điển
with open(image_paths_dict, "r") as json_file:
    image_paths = json.load(json_file)
print(len(image_paths))


# LOAD MODEL

model, preprocess = clip.load("ViT-B/32")
model.cuda().eval()

image_paths_query = r"C:\Users\admin\Projects\AIC\DATA\Keyframes\Keyframes_L01\L01_V002\0019.jpg"
image_query = Image.open(image_paths_query)

image_query = preprocess(image_query) # SHAPE(3,224,224)
print(image_query.shape)

image_query = torch.unsqueeze(image_query, 0).cuda() # SHAPE(1,3,224,224)
# print(image.shape)

# image_input = torch.tensor(np.stack(image)).cuda()
print(image_query.shape)
with torch.no_grad():
    image_features_query = model.encode_image(image_query).float()
image_features_query /= image_features_query.norm(dim=-1, keepdim=True)
# SHAPE(1,512)

print("clip_feature: ",clip_feature.shape) # SHAPE(25032,512)
print("image_feature: ",image_features_query.shape) 


# CALCULATE DISTANCE
distance = np.linalg.norm(clip_feature - image_features_query.cpu().numpy(),axis = 1 )
print(distance.shape)


# SHOW RESULT
k = 50
ids = np.argsort(distance)[:k]



result = [(image_paths[str(id)],distance[id]) for id in ids]

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




