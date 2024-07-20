import numpy as np
import torch
from PIL import Image
import os
import faiss
# import json
from transformers import XLMRobertaTokenizer
# import torch.nn as nn
# import torch.nn.functional as F
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode

import sys
sys.path.append(r"./")
from models.utils import translate, visualize, load_image_path, load_features

sys.path.append(r"./unilm/beit3/")
from unilm.beit3.modeling_finetune import beit3_base_patch16_224_retrieval



class BEIT3:
    def __init__(self):
        self.beit3_model = None
        self.tokenizer = None
        self.faetures = None
        self.faiss_index = None

    def load_model(self, device, model_weight_path, tokenizer_path):
        self.beit3_model = beit3_base_patch16_224_retrieval(pretrained=True)
        checkpoint = torch.load(model_weight_path)
        self.beit3_model.load_state_dict(checkpoint['model'])

        self.tokenizer = XLMRobertaTokenizer(tokenizer_path)
        self.beit3_model.to(device)
        self.beit3_model.eval()

    def load_feature(self, feature_folder_path, distance_metric="cosine"):
        # array_list = []

        # for file_name in os.listdir(feature_folder_path):
        #     if file_name.endswith(".npy"):
        #         file_path = os.path.join(feature_folder_path, file_name)
        #         array = np.load(file_path)
        #         array_list.append(array)

        # self.features = np.concatenate(array_list, axis=0)  # (87306, 768)
        
        self.features = load_features(feature_folder_path)
        print(f"beit3_faetures shape: {self.features.shape}")
        
        if distance_metric == "cosine":
            self.faiss_index = faiss.IndexFlatIP(self.features.shape[1])
        elif distance_metric == "L2":
            self.faiss_index = faiss.IndexFlatL2(self.features.shape[1])
        # Thêm các vector vào index.
        self.faiss_index.add(self.features)

    # def create_faiss_index(self, distance_metric="cosine", feature_folder_path = None):

    #     # print(f"vectors shape: {self.faetures.shape[1]}")
    #     features = self.load_feature(feature_folder_path)
    #     # Khởi tạo index faiss.
    #     if distance_metric == "cosine":
    #         self.faiss_index = faiss.IndexFlatIP(features.shape[1])
    #     elif distance_metric == "L2":
    #         self.faiss_index = faiss.IndexFlatL2(features.shape[1])
    #     # Thêm các vector vào index.
    #     self.faiss_index.add(features)

    def find_k_nearest_neighbors(self, vector_query, k):
        if self.faiss_index is None:
            raise ValueError("Features is empty. Please load features first.")
        # Tính khoảng cách giữa input_vector và các vector trong index.
        distances, indices = self.faiss_index.search(
            vector_query.reshape(1, -1), k)
        return distances[0], indices[0]

    def image_extract(self, image, device, image_size=224):
        # raw_image = Image.open(image_path).convert('RGB')
        raw_image = image.convert('RGB')
        transform = transforms.Compose([
            transforms.Resize((image_size, image_size),
                              interpolation=InterpolationMode.BICUBIC),
            transforms.ToTensor(),
        ])
        image_tensor = transform(raw_image).unsqueeze(0).to(device)

        with torch.no_grad():
            vision_cls, _ = self.beit3_model(image=image_tensor, only_infer=True)

        return vision_cls


    def Image_retrieval(self, image, k, device):
        image_features_query = self.image_extract(image, device)
        print(f"image_features_query: {image_features_query.shape}")
        distances, ids_result = self.find_k_nearest_neighbors(image_features_query.cpu().numpy(), k)

        return ids_result, distances

    def text_extract(self, text_query, device):
        text_tensor = self.tokenizer(text_query, return_tensors='pt')["input_ids"]
        print(f"text_tensor: {text_tensor.shape}")
        text_tensor = text_tensor.to(device)
        with torch.no_grad():
            _, text_cls = self.beit3_model(text_description=text_tensor, only_infer=True)
        return text_cls
    
    def Text_retrieval(self, text_query, k, device):
        text_features_query = self.text_extract(text_query, device)
        print(f"text_features_query: {text_features_query.shape}")
        distances, ids_result = self.find_k_nearest_neighbors(text_features_query.cpu().numpy(), k)

        return ids_result, distances



if __name__ == "__main__":

    # DEFINE PARAMETER
    feature_folder_path = r"D:\Downloads\data\data\beit3_features"
    image_path_dict = r"D:\Downloads\data\data\image_path.json"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_weight_path = r"D:\Downloads\beit3_base_itc_patch16_224.pth"
    # model_weight_path = r"C:\Users\admin\Downloads\beit3_large_itc_patch16_224_flickr.pth"
    tokenizer_path = r"D:\Downloads\beit3.spm"


    # text_query = "a woman feedding dogs in the park"
    text_query = "một người phụ nữ đang cho bầy chó ăn trong công viên"
    # text_query = "bình gốm"
    # text_query = "a dolphin playing with a pink ball"
    img_query_path = r"D:\Downloads\z5482675577503_2688f79cc75b2487cf7e85fd358660f9.jpg"

    K = 40

    beit3 = BEIT3()
    beit3.load_feature(feature_folder_path)
    beit3.load_model(device, model_weight_path, tokenizer_path)
    
    
    
    TEST_TEXT = False
    if TEST_TEXT:
        print()
        print("Text Query")
        text_query = translate(text_query)
        print("text translated: ", text_query)
        ids_result, distances = beit3.Text_retrieval(text_query, K, device)
    else:
        print()
        print("Image Query")
        ids_result, distances = beit3.Image_retrieval(img_query_path, K, device)

    image_path = load_image_path(image_path_dict)
    # visualize(image_path, ids_result, K)
    print(ids_result)
