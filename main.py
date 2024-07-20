from fastapi import FastAPI
from app_model import SearchRequest
from models.beit3_model import BEIT3
from PIL import Image
from io import BytesIO
import torch
import base64
import tempfile


app = FastAPI()

feature_folder_path = r"D:\Downloads\data\data\beit3_features"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_weight_path = r"D:\Downloads\beit3_base_itc_patch16_224.pth"
    # model_weight_path = r"C:\Users\admin\Downloads\beit3_large_itc_patch16_224_flickr.pth"
tokenizer_path = r"D:\Downloads\beit3.spm"

beit3 = BEIT3()
beit3.load_feature(feature_folder_path)
beit3.load_model(device, model_weight_path, tokenizer_path)
K = 40

print("finish loading")


@app.post('/')
def search_image(request: SearchRequest):
    for stage in request.stages:
        handle_stage(stage)
    return {"hello", "world"}

def handle_stage(stage):
    if(stage.type == "scene"):
        handle_scene_query(stage.data)
    elif(stage.type == "image"):
        handle_image_query(stage.data)
    elif(stage.type == "text"):
        print("text")
    elif(stage.type == "speech"):
        print("speech")
    elif(stage.type == "sketch"):
        print("sketch")

def handle_scene_query(data):
    print("text translated: ", data)
    ids_result, distances = beit3.Text_retrieval(data, K, device)
    return ids_result

def handle_image_query(data):
    data = data.split(",")[1]
    image_data = base64.b64decode(data)
    image = Image.open(BytesIO(image_data))
    ids_result, distances = beit3.Image_retrieval(image, K, device)
    print(ids_result)
    return ids_result

