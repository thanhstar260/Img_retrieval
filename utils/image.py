import numpy as np
import torch
from PIL import Image
import clip
import os
import matplotlib.pyplot as plt
import faiss
import json
from PIL import Image
import requests
from io import BytesIO

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


# def img2img(preprocess,model,img_query_path,k,device,vector_db):

#     image_query = Image.open(img_query_path)
#     image_query = preprocess(image_query).to(device)
#     image_query = torch.unsqueeze(image_query, 0)

#     with torch.no_grad():
#         image_features_query = model.encode_image(image_query).float()
#     image_features_query /= image_features_query.norm(dim=-1, keepdim=True)

#     ids_result = find_k_nearest_neighbors(image_features_query.cpu().numpy(),vector_db,k)

#     return ids_result

def img2img(preprocess, model, img_query_path, k, device, vector_db):
    if img_query_path.startswith(('http://', 'https://')):
        # Load image from URL
        response = requests.get(img_query_path)
        image_query = Image.open(BytesIO(response.content))
    else:
        # Load local image
        image_query = Image.open(img_query_path)

    image_query = preprocess(image_query).to(device)
    image_query = torch.unsqueeze(image_query, 0)

    with torch.no_grad():
        image_features_query = model.encode_image(image_query).float()
    image_features_query /= image_features_query.norm(dim=-1, keepdim=True)

    ids_result = find_k_nearest_neighbors(image_features_query.cpu().numpy(), vector_db, k)

    return ids_result


def visualize(result, k, image_path):
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
    img_query_path = r"C:\Users\NHAN\UIT_HK5\Truy_van_ttdpt\final_project\Img_retrieval\static\images\Keyframes_L02\L02_V001\0001.jpg"
    feature_folder_path = r'C:\Users\NHAN\AIC\Img_retrival\DATA\clip-features-vit-b32'
    image_path_dict = r"C:\Users\NHAN\UIT_HK5\Truy_van_ttdpt\final_project\Img_retrieval\image_path.json"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
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
    result = img2img(preprocess,model,img_query_path,K,device,vector_db)
    visualize(result, K)
