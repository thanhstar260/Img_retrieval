import numpy as np
import torch
from PIL import Image
import os
import faiss
from torchvision import transforms

import sys
sys.path.append(r"./")
from models.utils import translate, visualize, load_image_path

# sys.path.append(r"./ZSE_SBIR/")
from ZSE_SBIR.options import Option
from ZSE_SBIR.model.model import Model
from ZSE_SBIR.utils.util import setup_seed, load_checkpoint


class SKETCH:
    def __init__(self):
        self.model = None
        # self.faetures = None
        self.faiss_index = None
        
    def load_model(self, device, model_weight_path):
        args = Option().parse()
        setup_seed(args.seed)
        # checkpoint = load_checkpoint(args.load)
        args.load = model_weight_path

        checkpoint = load_checkpoint(args.load)
        # Khởi tạo model
        self.model = Model(args).float() 
        if args.load is not None:
            cur = self.model.state_dict()
            new = {k: v for k, v in checkpoint['model'].items() if k in cur.keys()}
            cur.update(new)
            self.model.load_state_dict(cur)
        self.model.to(device)
        self.model.eval()
        
    def load_feature(self, feature_folder_path = None, distance_metric="cosine"):
        array_list = []

        for file_name in os.listdir(feature_folder_path):
            if file_name.endswith(".npy"):
                file_path = os.path.join(feature_folder_path, file_name)
                array = np.load(file_path, allow_pickle= True)  
                array_list.append(array)

        features = np.concatenate(array_list, axis=0)  # (87306, 768)
        if distance_metric == "cosine":
            self.faiss_index = faiss.IndexFlatIP(features.shape[1])
        elif distance_metric == "L2":
            self.faiss_index = faiss.IndexFlatL2(features.shape[1])
        # Thêm các vector vào index.
        self.faiss_index.add(features)
        
    # def create_faiss_index(self, distance_metric="cosine", feature_folder_path = None):
    #     # Khởi tạo index faiss.
    #     features = self.load_feature(feature_folder_path)
    #     # print(f"vectors shape: {self.faetures.shape[1]}")
    #     if distance_metric == "cosine":
    #         self.faiss_index = faiss.IndexFlatIP(features.shape[1])
    #     elif distance_metric == "L2":
    #         self.faiss_index = faiss.IndexFlatL2(features.shape[1])
            
    #     self.faiss_index.add(features)
            
    def extract_feature_query(self, image, image_size, device):
        # Chuẩn bị transformations
        transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
        ])

        img = image.convert("RGB")
        img_tensor = transform(img).unsqueeze(0).half().to(device)  # Chuyển sang half và đưa lên GPU
        with torch.no_grad():
            img_feature = self.model(img_tensor.float(), None, 'test', only_sa=True)[0]
        
        img_feature = img_feature[:,0,:] # (1, 768)
        img_feature /= img_feature.norm(dim=-1, keepdim=True)
        return img_feature
        
    def find_k_nearest_neighbors(self, input_vector, k):
        if self.faiss_index is None:
            raise ValueError("Features is empty. Please load features first.")

        # Tính khoảng cách giữa input_vector và các vector trong index.
        distances, indices = self.faiss_index.search(input_vector.reshape(1, -1), k)
        return distances[0].tolist(), indices[0].tolist()
    
    def Sket_retrieval(self, image, k, device):
        sket_vector_query = self.extract_feature_query(image, 224, device)
        distances, ids_result = self.find_k_nearest_neighbors(sket_vector_query.cpu().numpy(), k)
        return ids_result, distances
    
    

if __name__ == "__main__":

    sket_query_path = r"D:\Downloads\sketch.png"

    image_path_dict = r"D:\Temporal_search\data\image_path.json"
    sket_feature_path = r'D:\Temporal_search\data\sketch_features'
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_weight_path = r"D:\Downloads\best_checkpoint.pth"
    K = 40

    sketch_model = SKETCH()
    sketch_model.load_model(device, model_weight_path)
    sketch_model.load_feature(sket_feature_path)
    
    
    dis,result = sketch_model.Sket_retrieval(sket_query_path, K, device)
    # print(dis)
    # print(result)


    # image_path = load_image_path(image_path_dict)

    # visualize(image_path, result, K)
    print(result)
