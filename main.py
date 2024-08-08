from fastapi import FastAPI, HTTPException
from app_model import SearchRequest, SearchResult, RerankRequest
from models.beit3_model import BEIT3
from models.model import Event_retrieval
from PIL import Image
from io import BytesIO
import torch
import base64
import os
from models.utils import visualize, load_image_path, translate, rrf
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from io import BytesIO

app = FastAPI()

origins = [
    "http://localhost:3000",
]


app.mount("/static", StaticFiles(directory="static"), name="static")

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
sket_model_path = r"D:\THANHSTAR\Projetcs\AIC\ZSE_SBIR\checkpoints\sketchy_ext\best_checkpoint.pth"
# sket_model_path = r".\models\weights\best_checkpoint.pth"
sket_fea_path = r".\DATA\sketch_features"

load_dotenv()
CHECK_SERVER = os.getenv("CHECK_SERVER")
HOST_ELASTIC = os.getenv("HOST_ELASTIC")
PORT_ELASTIC = int(os.getenv("PORT_ELASTIC"))

retrieval = Event_retrieval()
retrieval.load_feature(type_fea="all", beit3_fea_path=beit3_fea_path, sket_fea_path=sket_fea_path)
retrieval.load_model(device=device, type_model="all", beit3_model_path=beit3_model_path, tokenizer_path=tokenizer_path, sket_model_path=sket_model_path)
retrieval.connect_elastic(check_server = CHECK_SERVER, host=HOST_ELASTIC, port=PORT_ELASTIC)


K = 80

print("finish loading")

def checkAndTranslate(lang, str):
    if(lang != "eng"):
        str = translate(str)
    return str

@app.post('/')
def search_image(request: SearchRequest) -> Dict[int, SearchResult]:
    list_ids = []
    list_distances = []
    result = {}
    index = 0
    for stage in request.stages:
        stage_result = handle_stage(stage, request.K)
        if(stage.data.object != None):
            stage_result = handle_object_query(stage_result['ids'], stage_result['distances'], stage.object, K)
        # result.update({index: stage_result})
        list_ids.append(stage_result['ids'])
        list_distances.append(stage_result['distances'])

    # print("list ids: ", list_ids)
    if len(request.stages) > 1:
        # print(list_ids, list_distances)
        ids, dis = retrieval.temporal_search(list_ids, list_distances)
        for index in range(len(ids)):
            result.update({index: {'ids': ids[index], 'distances': dis}})
    else:
        result.update({'0': {'ids': list_ids[0], 'distances': list_distances[0]}})

    return result

def handle_stage(stage, K):
    list_ids = []
    distances = []
    ids = []
    if(stage.data.scene != None):
        data = checkAndTranslate(stage.lang, stage.data.scene)
        stage_result = handle_scene_query(data, K)
        list_ids.append(stage_result['ids'])
        distances = stage_result['distances']
    if(stage.data.image != None):
        stage_result = handle_image_query(stage.data.image, K)
        list_ids.append(stage_result['ids'])
        distances = stage_result['distances']
    if(stage.data.text != None):
        stage_result = handle_text_query(stage.data.text, K)
        list_ids.append(stage_result['ids'])
        distances = stage_result['distances']
    if(stage.data.speech != None):
        stage_result = handle_speech_query(stage.data.speech, K)
        list_ids.append(stage_result['ids'])
        distances = stage_result['distances']
    if(stage.data.sketch != None):
        stage_result = handle_sketch_query(stage.data.sketch, K)
        list_ids.append(stage_result['ids'])
        distances = stage_result['distances']
    
    if(len(list_ids) > 1):
        ids, distances = rrf(list_ids, K)
    else:
        ids = list_ids[0]

    return {'ids': ids, 'distances': distances}

def handle_scene_query(data, K):
    print("text translated: ", data)
    ids_result, distances = retrieval.beit3.Text_retrieval(data, K * 10, device)
    return {"ids": ids_result, "distances": distances}

def handle_image_query(data, K):
    data = data.split(",")[1]
    image_data = base64.b64decode(data)
    image = Image.open(BytesIO(image_data))
    ids_result, distances = retrieval.beit3.Image_retrieval(image, K * 10, device)
    print(ids_result)

    return {"ids": ids_result, "distances": distances}

def handle_sketch_query(data, K):
    data = data.split(",")[1]
    image_data = base64.b64decode(data)
    image = Image.open(BytesIO(image_data))
    ids_result, distances = retrieval.sketch.Sket_retrieval(image, K * 10, device)
    print(ids_result)
    return {"ids": ids_result, "distances": distances}

def handle_text_query(data, K):
    ids_result, distances = retrieval.elastic.Elastic_retrieval(data, K * 10, "ocr")
    return {"ids": ids_result, "distances": distances}

def handle_speech_query(data, K):
    ids_result, distances = retrieval.elastic.Elastic_retrieval(data, K, "asr")
    return {"ids": ids_result, "distances": distances}

def handle_object_query(ids, dis, object_list, K):
    check_list = []
    for key, value in object_list.items():
        for item in value:
            item[0],item[2] = int(item[0]*1280/300), int(item[2]*1280/300)
            item[1],item[3] = int(item[1]*720/150), int(item[3]*720/150)
            check_list.append((key, item))
            
    print("check list: ", check_list)
    ids, dis = retrieval.object_filter(ids, dis, check_list, K)
    print(ids, dis)
    return {"ids": ids, "distances": dis}

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


@app.get("/get_image_url/{id}")
async def get_image_url(id: str):
    image_paths = load_image_path(r".\DATA\image_path.json")
    if id in image_paths:
        image_path = image_paths[id]
        return {"url": f"{image_path[1:]}"}
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    
@app.get("/get_video_url/{id}")
async def get_video_url(id: str):
    video_paths = load_image_path(r".\DATA\id2link.json")
    if id in video_paths:
        video_path = video_paths[id]
        return {"url": f"{video_path}"}
    else:
        raise HTTPException(status_code=404, detail="Video not found")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)