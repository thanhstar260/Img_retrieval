from flask import Flask, render_template, request, send_from_directory
from image import img2img as image_retrieval
from text import load_clip_feature, load_image_path, load_model, create_faiss_index
from text import text2img as text_retrieval
from search_ocr import ocr_result
from search_asr import asr_result
import numpy as np
import torch
import clip
import matplotlib.pyplot as plt
import urllib.parse
import meilisearch
import json

app = Flask(__name__, static_folder='static')

feature_folder_path = r'C:\Users\NHAN\AIC\Img_retrival\DATA\clip-features-vit-b32'
image_path_dict = r"C:\Users\NHAN\UIT_HK5\Truy_van_ttdpt\final_project\Img_retrieval\image_path.json"
youtube_path_dict = r'C:\Users\NHAN\UIT_HK5\Truy_van_ttdpt\final_project\Img_retrieval\id2link.json'
client = meilisearch.Client('https://edge.meilisearch.com', 'bc61b7bb01eb45353ed231d2f88750729ddbbac9')

with open(youtube_path_dict, "r") as json_file:
    youtube_path = json.load(json_file)
    
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# LOAD CLIP_FEATURE
clip_feature = load_clip_feature(feature_folder_path)

image_paths = load_image_path(image_path_dict)

# LOAD MODEL
model,preprocess = load_model(device)

# CREATE FAISS INDEX
vector_db = create_faiss_index(clip_feature)

# Your existing routes for serving images
@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory('static/images', filename)


# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for image retrieval
@app.route('/retrieve_image', methods=['POST'])
def retrieve_image():
    img_query_path = request.form['image_query']
    k_value = request.form['k_value']
    K_value = int(k_value) if k_value and k_value.isdigit() else 80
    result = image_retrieval(preprocess, model, img_query_path, K_value, device, vector_db)
    results = [(image_paths[str(id)], youtube_path[str(id)]) for id in result]
    return render_template('index.html', result=results)
    

# Route for text retrieval
@app.route('/retrieve_text', methods=['POST'])
def retrieve_text():
    print(request.form)
    clip_query = request.form['text_query']
    ocr_query = request.form['text_query_ocr']
    asr_query = request.form['text_query_asr']
    k_value = request.form['k_value']
    K_value = int(k_value) if k_value and k_value.isdigit() else 80

    result_clip = []
    result_ocr = []
    result_asr = []

    if clip_query != '':
        result_clip = text_retrieval(model, clip_query, K_value, device, vector_db)

    if ocr_query != '':
        result_ocr = ocr_result(client,text_query=ocr_query,k=K_value)
        

    if asr_query != '':
        result_asr = asr_result(client,text_query=asr_query,k=K_value)

    intersect_result = set(result_asr) & set(result_ocr) & set(result_clip)

    if (len(intersect_result) < K_value):
        intersect_result.update(result_asr[:int(K_value/3)])
        intersect_result.update(result_ocr[:int(K_value/3)])
        len_result = len(intersect_result)
        intersect_result.update(result_clip[:K_value-len_result])

    result = list(intersect_result)
    results = [(image_paths[str(id)], youtube_path[str(id)]) for id in result]

    return render_template('index.html', result=results)

if __name__ == '__main__':
    app.run(debug=True)
