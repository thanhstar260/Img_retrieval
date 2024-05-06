from flask import Flask, render_template, request, send_from_directory, jsonify
from utils.image import img2img as image_retrieval
from utils.text import load_clip_feature, load_image_path, load_model, create_faiss_index
from utils.text import text2img as text_retrieval
from utils.combine_results import combine_2results, combine_3results
from utils.search_ocr import ocr_result
from utils.search_asr import asr_result 
import os
from torchvision import transforms
import torch
import meilisearch
import json
from PIL import Image
import base64
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

import sys
sys.path.append('ZSE_SBIR')
from options import Option
from result import sketch2img
from model.model import Model
from utils.util import setup_seed, load_checkpoint

HTTP = os.getenv("HTTP")
MASTER_KEY = os.getenv("MASTER_KEY")
client = meilisearch.Client(HTTP, MASTER_KEY)

app = Flask(__name__, static_folder='static')

feature_folder_path = r'.\DATA\clip-features-vit-b32'
image_path_dict = r".\utils\image_path.json"
image_paths = load_image_path(image_path_dict)
    
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
clip_feature = load_clip_feature(feature_folder_path)
model,preprocess = load_model(device)
vector_db = create_faiss_index(clip_feature)

#sketch
args = Option().parse()
os.environ["CUDA_VISIBLE_DEVICES"] = args.choose_cuda
setup_seed(args.seed)
args.load = r".\ZSE_SBIR\checkpoints\sketchy_ext\best_checkpoint.pth"

checkpoint = load_checkpoint(args.load)
sket_feature_path = r'.\ZSE_SBIR\features'
# Khởi tạo model
sketch_model = Model(args).float()  # Chuyển model sang half precision
if args.load is not None:
    cur = sketch_model.state_dict()
    new = {k: v for k, v in checkpoint['model'].items() if k in cur.keys()}
    cur.update(new)
    sketch_model.load_state_dict(cur)
sketch_model.cpu()  # Chuyển model lên CPU

if len(args.choose_cuda) > 1:
    sketch_model = torch.nn.parallel.DataParallel(model)

sketch_model.eval()

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory('static/images', filename)

@app.route('/')
def index():
    return render_template('index1.html', clip_query='', ocr_query='', asr_query='', image_query='', sketch_query='', k_value='80')

@app.route('/retrieve_image', methods=['POST'])
def retrieve_image():
    print(request.form)
    img_query_path = request.form['image_query']
    k_value = request.form['k_value']
    K_value = int(k_value) if k_value and k_value.isdigit() else 80
    try:
        result = image_retrieval(preprocess, model, img_query_path, K_value, device, vector_db)
        results = [image_paths[str(id)] for id in result]
        return jsonify({'result': results})
    except Exception as e:
        print(f"Error retrieving image: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/retrieve_text', methods=['POST'])
def retrieve_text():
    print(request.form)
    img_query_path = request.form['image_query']
    sketch_query = request.form['sketch_query']
    if img_query_path != '':
        k_value = request.form['k_value']
        K_value = int(k_value) if k_value and k_value.isdigit() else 80
        result = image_retrieval(preprocess, model, img_query_path, K_value, device, vector_db)
        results = [image_paths[str(id)] for id in result]
        return render_template('index1.html', result=results,image_query=img_query_path, sketch_query=sketch_query, k_value=k_value)
    
    if sketch_query != '':
        # Extract base64 image data from data URL
        _, encoded_data = sketch_query.split(',', 1)
        
        # Decode base64 image data
        decoded_data = base64.b64decode(encoded_data)
        
        # Save decoded data to a file
        save_path = r'.\static\sketch_query\sketch.jpg'
        
        # print(os.path.exists(save_path))
        with open(save_path, 'wb') as f:
            f.write(decoded_data)

        k_value = request.form['k_value']
        K_value = int(k_value) if k_value and k_value.isdigit() else 80
        result = sketch2img(save_path, sket_feature_path, sketch_model, K_value)
        results = [image_paths[str(id)] for id in result]
        return render_template('index1.html', result=results,image_query=img_query_path, sketch_query=sketch_query, k_value=k_value)

    clip_query = request.form['clip_query']
    ocr_query = request.form['ocr_query']
    asr_query = request.form['asr_query']
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

    results = [image_paths[str(id)] for id in result]

    return render_template('index1.html', result=results, clip_query=clip_query, ocr_query=ocr_query, asr_query=asr_query,
                           image_query=img_query_path, sketch_query=sketch_query, k_value=k_value)

if __name__ == '__main__':
    app.run(debug=True)
