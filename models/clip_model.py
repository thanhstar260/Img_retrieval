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
import sys
sys.path.append(r"./")
from models.utils import visualize, load_image_path

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
class CLIP:
    def __init__(self):
        self.model = None
        self.preprocess = None
        self.faetures = None
        self.faiss_index = None

    def load_model(self,device):
        self.model, self.preprocess = clip.load("ViT-B/32")
        self.model.to(device).eval()
    
    def load_feature(self, feature_folder_path):
        array_list = []

        for file_name in os.listdir(feature_folder_path):
            if file_name.endswith(".npy"):
                file_path = os.path.join(feature_folder_path, file_name)
                array = np.load(file_path)
                array_list.append(array)

        self.faetures = np.concatenate(array_list, axis=0)  # (87306, 512)
        print(f"faetures shape: {self.faetures.shape}")
        
    def create_faiss_index(self,distance_metric="cosine"):

        print(f"vectors shape: {self.faetures.shape[1]}")
        
        # Khởi tạo index faiss.
        if distance_metric == "cosine":
            self.faiss_index = faiss.IndexFlatIP(self.faetures.shape[1])  
        elif distance_metric == "L2":
            self.faiss_index = faiss.IndexFlatL2(self.faetures.shape[1])
        # Thêm các vector vào index.
        self.faiss_index.add(self.faetures)  
    
    def find_k_nearest_neighbors(self, vector_query, k):
        if self.faiss_index is None:
            self.create_faiss_index()
        # Tính khoảng cách giữa input_vector và các vector trong index.
        distances, indices = self.faiss_index.search(vector_query.reshape(1, -1), k)
        return distances, indices[0]

    def image_extract(self, image_path, device):
        if img_query_path.startswith(('http://', 'https://')):
            # Load image from URL
            response = requests.get(img_query_path)
            image_query = Image.open(BytesIO(response.content))
        else:
            # Load local image
            image_query = Image.open(img_query_path)

        image_query = self.preprocess(image_query).to(device)
        image_query = torch.unsqueeze(image_query, 0)

        with torch.no_grad():
            image_features_query = self.model.encode_image(image_query).float()
        image_features_query /= image_features_query.norm(dim=-1, keepdim=True)
        return image_features_query
    
    # RETRIEVAL BY IMAGE
    def Image_retrieval(self, img_query_path, k, device):
        image_features_query = self.image_extract(img_query_path, device)
        distances, ids_result = self.find_k_nearest_neighbors(image_features_query.cpu().numpy(), k)

        return ids_result, distances


    def extract_text_feature(self, text_query, device):
        text = clip.tokenize([text_query]).to(device)
        with torch.no_grad():
            text_features = self.model.encode_text(text).float()
        text_features /= text_features.norm(dim=-1, keepdim=True)
        return text_features
    # RETRIEVAL BY TEXT
    def Text_retrieval(self, text_query, k, device):
        text_features = self.extract_text_feature(text_query, device)
        distances,ids_result = self.find_k_nearest_neighbors(text_features.cpu().numpy(), k)
        return ids_result, distances



if __name__ == "__main__":
    
    print("RUNNING")
    # DEFINE PARAMETER
    feature_folder_path = r'.\DATA\clip-features-vit-b32'
    image_path_dict = r".\DATA\image_path.json"
    K = 40

    img_query_path = r".\static\images\Keyframes_L02\L02_V001\0001.jpg"
    text_query = "a dolphin play with pink ball"

    # CREATE CLIP OBJECT
    clip_model = CLIP()

    # LOAD MODEL
    clip_model.load_model(DEVICE)
    # LOAD CLIP_FEATURE
    clip_model.load_feature(feature_folder_path=feature_folder_path)


    # TEST Query
    test_text = True
    
    if test_text:
        distances,ids_result = clip_model.Text_retrieval(text_query, K, DEVICE)
    else:
        distances,ids_result = clip_model.Image_retrieval(img_query_path, K, DEVICE)
    
    
    
    # LOAD IMG_PATH
    image_path = load_image_path(image_path_dict)
    visualize(image_path, ids_result, K)
