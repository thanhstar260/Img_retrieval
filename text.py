import numpy as np
import torch
from PIL import Image
import clip
import os
import matplotlib.pyplot as plt
import faiss
import json


def create_faiss_index(vectors_db):
    # Khởi tạo index faiss.
    index = faiss.IndexFlatL2(vectors_db.shape[1])
    # Thêm các vector vào index.
    index.add(vectors_db)  
    return index
 
def find_k_nearest_neighbors(input_vector, vectors_db, k):
  # Tính khoảng cách giữa input_vector và các vector trong index.
  distances, indices = vectors_db.search(input_vector.reshape(1, -1), k)
  return indices[0]


def text2img(model,text_query,k,device,vector_db):

    text_tokens = clip.tokenize([text_query]).to(device)# (1,77)

    with torch.no_grad():
        text_features = model.encode_text(text_tokens).float() #(1,512)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    ids_result = find_k_nearest_neighbors(text_features.cpu().numpy(),vector_db,k)

    return ids_result

def visualize(result,k,image_path):
    axes = []
    grid_size = k//8
    fig = plt.figure(figsize=(10,5))

    for id in range(k):
        draw_image = result[id]
        axes.append(fig.add_subplot(grid_size + 1, 8, id+1))
        axes[-1].set_title(image_path[str(draw_image)][-17:-4])
        axes[-1].set_xticks([])
        axes[-1].set_yticks([])
        plt.imshow(Image.open(image_path[str(draw_image)]))


    fig.tight_layout()
    plt.show()

def load_clip_feature(feature_folder_path):
    array_list = []

    for file_name in os.listdir(feature_folder_path):
        if file_name.endswith(".npy"):
            file_path = os.path.join(feature_folder_path, file_name)
            array = np.load(file_path)
            array_list.append(array)

    clip_feature = np.concatenate(array_list, axis=0)

    return clip_feature


def load_image_path(image_path_dict):
    with open(image_path_dict, "r") as json_file:
        image_path = json.load(json_file)
    return image_path

def load_model(device):
    model, preprocess = clip.load("ViT-B/32")
    model.to(device).eval()
    return model,preprocess

if __name__ == "__main__":

    # DEFINE PARAMETER
    feature_folder_path = r'C:\Users\admin\Projects\AIC\DATA\clip-features-vit-b32'
    image_path_dict = r"C:\Users\admin\Projects\AIC\image_path.json"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    text_query = "a dog and a pink ball"
    K = 40
    
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
    visualize(result, K,image_path=image_path)