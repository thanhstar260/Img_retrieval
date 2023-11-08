import numpy as np
import torch
from PIL import Image
import clip
import os
import skimage
import matplotlib.pyplot as plt
import torch.nn.functional as F
import matplotlib.pyplot as plt
import json

# LOAD CLIP_FEATURE

folder_path = r'C:\Users\admin\Projects\AIC\DATA\Keyframes'
image_dict = {}

index = 0
for folder_name in os.listdir(folder_path):
    folder_dir = os.path.join(folder_path, folder_name)
    for sub_folder_name in os.listdir(folder_dir):
        sub_folder_dir = os.path.join(folder_dir, sub_folder_name)
        for file_name in os.listdir(sub_folder_dir):
            file_path = os.path.join(sub_folder_dir, file_name)
            image_dict[index] = file_path
            index += 1

# for key, value in image_dict.items():
#     print(key, ":", value)

with open('feature.json', 'w') as file:
    json.dump(image_dict, file)

print("success!")
