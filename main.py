from fastapi import FastAPI
from app_model import SearchRequest, SearchResult, RerankRequest
from models.beit3_model import BEIT3
from models.model import Event_retrieval
from PIL import Image
from io import BytesIO
import torch
import base64
import os
from models.utils import visualize, load_image_path, translate
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

app = FastAPI()

origins = [
    "http://localhost:3000",
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialization
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# BEIT3 PARAMETER
beit3_model_path = r".\models\weights\beit3_base_itc_patch16_224.pth"
tokenizer_path = r".\models\weights\beit3.spm"
beit3_fea_path = r".\DATA\beit3_features"
    
# SKETCH PARAMETER
sket_model_path = r".\models\weights\best_checkpoint.pth"
sket_fea_path = r".\DATA\sketch_features"

load_dotenv()
CHECK_SERVER = os.getenv("CHECK_SERVER")
HOST_ELASTIC = os.getenv("HOST_ELASTIC")
PORT_ELASTIC = int(os.getenv("PORT_ELASTIC"))

retrieval = Event_retrieval()
retrieval.load_feature(type_fea="all", beit3_fea_path=beit3_fea_path, sket_fea_path=sket_fea_path)
retrieval.load_model(device=device, type_model="all", beit3_model_path=beit3_model_path, tokenizer_path=tokenizer_path, sket_model_path=sket_model_path)
retrieval.connect_elastic(check_server = CHECK_SERVER, host=HOST_ELASTIC, port=PORT_ELASTIC)


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
        stage_result = handle_stage(stage, request.K)
        result.update({index: stage_result})
        index += 1
    return result

def handle_stage(stage, K):
    if(stage.type == "scene"):
        data = checkAndTranslate(stage.lang, stage.data)
        return handle_scene_query(data, K)
    elif(stage.type == "image"):
        return handle_image_query(stage.data, K)
    elif(stage.type == "text"):
        data = checkAndTranslate(stage.data)
        return handle_text_query(data, K)
    elif(stage.type == "speech"):
        data = checkAndTranslate(stage.data)
        return handle_speech_query(data, K)
    elif(stage.type == "sketch"):
        return handle_sketch_query(stage.data, K)

def handle_scene_query(data, K):
    print("text translated: ", data)
    ids_result, distances = retrieval.beit3.Text_retrieval(data, K * 10, device)
    return {"ids": ids_result[:K], "distances": distances[:K]}

def handle_image_query(data, K):
    data = data.split(",")[1]
    image_data = base64.b64decode(data)
    image = Image.open(BytesIO(image_data))
    ids_result, distances = retrieval.beit3.Image_retrieval(image, K * 10, device)
    print(ids_result)
    return {"ids": ids_result[:K], "distances": distances[:K]}

def handle_sketch_query(data, K):
    data = data.split(",")[1]
    image_data = base64.b64decode(data)
    image = Image.open(BytesIO(image_data))
    ids_result, distances = retrieval.sketch.Sket_retrieval(image, K * 10, device)
    print(ids_result)
    return {"ids": ids_result[:K], "distances": distances[:K]}

def handle_text_query(data, K):
    ids_result, distances = retrieval.elastic.Elastic_retrieval(data, K * 10, "ocr")
    return {"ids": ids_result[:K], "distances": distances[:K]}
def handle_speech_query(data):
    ids_result, distances = retrieval.elastic.Elastic_retrieval(data, K, "asr")
    return {"ids": ids_result[:K], "distances": distances[:K]}



@app.post('/rerank')
def handle_rerank_query(request: RerankRequest) -> Dict[int, SearchResult]:
    result = {}
    index = 0
    for stage in request.stages:
        ids, dis = retrieval.rerank(stage.dis, stage.ids, stage.positive_list, stage.negative_list)
        stage_result = {"ids": ids, "distances": dis}
        result.update({index: stage_result})
        index += 1
    return result

def handle_object_query(ids, dis, object_list, K):
    check_list = []
    for object in object_list:
        for item in object[1]:
            check_list.append((object[0], item))
    ids, dis = retrieval.object_filter(ids, dis, check_list, K)
    return {"ids": ids, "distances": dis}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
