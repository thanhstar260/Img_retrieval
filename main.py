from fastapi import FastAPI
from app_model import SearchRequest, SearchResult
from models.beit3_model import BEIT3
from models.model import Event_retrieval
from PIL import Image
from io import BytesIO
import torch
import base64
import os
from models.utils import visualize, load_image_path, translate
from typing import Dict


# initialization
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# BEIT3 PARAMETER
beit3_model_path = r".\models\weights\beit3_base_itc_patch16_224.pth"
tokenizer_path = r".\models\weights\beit3.spm"
beit3_fea_path = r".\DATA\beit3_features"
    
# SKETCH PARAMETER
sket_model_path = r".\ZSE_SBIR\checkpoints\sketchy_ext\best_checkpoint.pth"
sket_fea_path = r".\DATA\sketch_features"

retrieval = Event_retrieval()
retrieval.load_feature(type_fea="beit3", beit3_fea_path=beit3_fea_path)
retrieval.load_model(device=device, type_model="beit3", beit3_model_path=beit3_model_path, tokenizer_path=tokenizer_path)

app = FastAPI()
K = 40

print("finish loading")

def checkAndTranslate(lang, str):
    if(lang == "vie"):
        str = translate(str)
    return str

@app.post('/')
def search_image(request: SearchRequest) -> Dict[int, SearchResult]:
    result = {}
    index = 0
    for stage in request.stages:
        stage_result = handle_stage(stage)
        result.update({index: stage_result})
        index += 1
    return result

def handle_stage(stage):
    if(stage.type == "scene"):
        data = checkAndTranslate(stage.lang, stage.data)
        return handle_scene_query(data)
    elif(stage.type == "image"):
        return handle_image_query(stage.lang, stage.data)
    elif(stage.type == "text"):
        data = checkAndTranslate(stage.data)
        print("text")
    elif(stage.type == "speech"):
        data = checkAndTranslate(stage.data)
        print("speech")
    elif(stage.type == "sketch"):
        print("sketch")

def handle_scene_query(data):
    print("text translated: ", data)
    ids_result, distances = retrieval.beit3.Text_retrieval(data, K, device)
    return {"ids": ids_result, "distances": distances}

def handle_image_query(data):
    data = data.split(",")[1]
    image_data = base64.b64decode(data)
    image = Image.open(BytesIO(image_data))
    ids_result, distances = retrieval.beit3.Image_retrieval(image, K, device)
    print(ids_result)
    return {"ids": ids_result, "distances": distances}

