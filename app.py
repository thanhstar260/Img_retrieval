from flask import Flask, render_template, request, send_from_directory, jsonify
from image import img2img as image_retrieval
from text import load_clip_feature, load_image_path, load_model, create_faiss_index
from text import text2img as text_retrieval
from combine_results import combine_2results, combine_3results
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
    img_query_path = request.form.get('image_query')
    k_value = request.form.get('k_value')
    K_value = int(k_value) if k_value and k_value.isdigit() else 80

    try:
        # Assuming image_retrieval function returns a list of image IDs
        result = image_retrieval(preprocess, model, img_query_path, K_value, device, vector_db)
        results = [(image_paths[str(id)], youtube_path[str(id)]) for id in result]

        return jsonify({'result': results})
    except Exception as e:
        print(f"Error retrieving image: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    

# Route for text retrieval
@app.route('/retrieve_text', methods=['POST'])
def retrieve_text():
    print(request.form)

    img_query_path = request.form['image_query']
    if img_query_path != '':
        k_value = request.form['k_value']
        K_value = int(k_value) if k_value and k_value.isdigit() else 80
        result = image_retrieval(preprocess, model, img_query_path, K_value, device, vector_db)
        results = [(image_paths[str(id)], youtube_path[str(id)]) for id in result]
        return render_template('index.html', result=results)

    clip_query = request.form['text_query']
    ocr_query = request.form['text_query_ocr']
    asr_query = request.form['text_query_asr']
    k_value = request.form['k_value']
    K_value = int(k_value) if k_value and k_value.isdigit() else 80

    result_clip = []
    result_ocr = []
    result_asr = []
    clip=False
    ocr=False
    asr=False

    if clip_query != '':
        result_clip = text_retrieval(model, clip_query, K_value, device, vector_db)
        clip = True

    if ocr_query != '':
        result_ocr = ocr_result(client,text_query=ocr_query,k=K_value)
        ocr = True

    if asr_query != '':
        result_asr = asr_result(client,text_query=asr_query,k=K_value)
        asr = True

    if (clip and ocr and asr):
        result = combine_3results(result_clip, result_asr, result_ocr,  K_value)
    elif (clip):
        if (ocr):
            result = combine_2results(result_clip, result_ocr, K_value)
        elif (asr):
            result = combine_2results(result_clip, result_asr, K_value)
        else:
            result = result_clip
    elif (ocr):
        if (asr):
            result = combine_2results(result_asr, result_ocr, K_value)
        else:
            result = result_ocr
    else:
        result = result_asr
    print(result_clip)
    print(result_ocr)
    print(result_asr)
    print(result)

    # intersect_result = [value for value in result_asr if value in result_ocr and value in result_clip]

    # if (len(intersect_result) < K_value):
    #     if (clip and ocr and asr):
    #         intersect_result.extend(result_asr[:int(K_value/3)])
    #         intersect_result.extend(result_ocr[:int(K_value/3)])
    #         len_result = len(intersect_result)
    #         intersect_result.extend(result_clip[:K_value-len_result])
    #     elif (clip):
    #         if (ocr):
    #             intersect_result.extend(result_ocr[:int(K_value/2)])
    #             len_result = len(intersect_result)
    #             intersect_result.extend(result_clip[:K_value-len_result])
    #         elif (asr):
    #             intersect_result.extend(result_asr[:int(K_value/2)])
    #             len_result = len(intersect_result)
    #             intersect_result.extend(result_clip[:K_value-len_result])   
    #         else:
    #             len_result = len(intersect_result)
    #             intersect_result.extend(result_clip[:K_value-len_result])
    #     elif (ocr):
    #         if (asr):
    #             intersect_result.extend(result_asr[:int(K_value/2)])
    #             len_result = len(intersect_result)
    #             intersect_result.extend(result_ocr[:K_value-len_result])   
    #         else:
    #             len_result = len(intersect_result)
    #             intersect_result.extend(result_ocr[:K_value-len_result])
    #     else:
    #         len_result = len(intersect_result)
    #         intersect_result.extend(result_asr[:K_value-len_result])

    results = [(image_paths[str(id)], youtube_path[str(id)]) for id in result]

    return render_template('index.html', result=results)

if __name__ == '__main__':
    app.run(debug=True)
