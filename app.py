from flask import Flask, render_template, request, send_from_directory
from image import img2img as image_retrieval
from text import load_clip_feature, load_image_path, load_model, create_faiss_index
from text import text2img as text_retrieval
from search_ocr import result_id
import numpy as np
import torch
import clip
import matplotlib.pyplot as plt
import urllib.parse
import meilisearch

app = Flask(__name__, static_folder='static')

feature_folder_path = r'C:\Users\NHAN\AIC\Img_retrival\DATA\clip-features-vit-b32'
image_path_dict = r"C:\Users\NHAN\UIT_HK5\Truy_van_ttdpt\final_project\Img_retrieval\image_path.json"
client = meilisearch.Client('https://edge.meilisearch.com', 'bc61b7bb01eb45353ed231d2f88750729ddbbac9')
    
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
    results = [image_paths[str(id)] for id in result]
    return render_template('index.html', result=results)

# Route for text retrieval
@app.route('/retrieve_text', methods=['POST'])
def retrieve_text():
    print(request.form)
    clip_query = request.form['text_query']
    ocr_query = request.form['text_query_ocr']
    k_value = request.form['k_value']
    K_value = int(k_value) if k_value and k_value.isdigit() else 80

    if clip_query != '':
        result_clip = text_retrieval(model, clip_query, K_value, device, vector_db)
        results_clip = [image_paths[str(id)] for id in result_clip]
    else:
        results_clip = []

    if ocr_query != '':
        result_ocr = result_id(client,text_query=ocr_query,k=K_value)
        results_ocr = [image_paths[str(id)] for id in result_ocr]
    else:
        results_ocr = []

    if ((len(results_clip)!= 0) and (len(results_ocr)!= 0)):
        results = results_ocr[:int(K_value/2)] + results_clip[:int(K_value/2)]
    elif len(results_clip)!= 0:
        results = results_clip
    else:
        results = results_ocr

    return render_template('index.html', result=results)

if __name__ == '__main__':
    app.run(debug=True)
