from flask import Flask, render_template, request, send_from_directory, jsonify
from utils.image import img2img as image_retrieval
from utils.text import load_clip_feature, load_image_path, load_model, create_faiss_index
from utils.text import text2img as text_retrieval
from utils.combine_results import combine_2results, combine_3results
from utils.search_ocr import ocr_result
from utils.search_asr import asr_result 
<<<<<<< HEAD
=======
from human_pose.test_result import load_pose_embed, load_image_path, retrieval_pose
from utils.translate import translate
>>>>>>> a57d6cac9e17f42a745a5728eb971db9cad615cf
import os
from torchvision import transforms
import torch
import meilisearch
import json
import numpy as np
import pandas as pd
from PIL import Image
import base64
import subprocess
import sys
sys.path.append('human_pose')

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
sketch_model = Model(args).float() 
if args.load is not None:
    cur = sketch_model.state_dict()
    new = {k: v for k, v in checkpoint['model'].items() if k in cur.keys()}
    cur.update(new)
    sketch_model.load_state_dict(cur)
sketch_model.cpu() 

sketch_model.eval()

# pose
image_path_dict_pose = r".\human_pose\yolov9_pose\data\data.json"
feature_pose_folder_path = r'.\human_pose\poem\output32'
image_paths_pose = load_image_path(image_path_dict_pose)
pose_embed = load_pose_embed(feature_pose_folder_path)
vector_pose_db = create_faiss_index(pose_embed)


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
    # pose_query = request.form['inp_keypoints']
    if img_query_path != '':
        k_value = request.form['k_value']
        K_value = int(k_value) if k_value and k_value.isdigit() else 80
        result = image_retrieval(preprocess, model, img_query_path, K_value, device, vector_db)
        results = [image_paths[str(id)] for id in result]
        return render_template('index1.html', result=results,image_query=img_query_path, sketch_query=sketch_query, k_value=k_value)
    
    # if pose_query != '':
    #     # # Chuyển pose query thành list các số thực
    #     # pose_query = pose_query.split(',')
    #     # pose_query = [float(x) for x in pose_query]
    #     # # Chuyển pose query thành file csv
    #     # header = ["image/width","image/height","image/object/part/Head/center/x","image/object/part/Head/center/y","image/object/part/Head/score","image/object/part/LShoulder/center/x","image/object/part/LShoulder/center/y","image/object/part/LShoulder/score","image/object/part/RShoulder/center/x","image/object/part/RShoulder/center/y","image/object/part/RShoulder/score","image/object/part/LElbow/center/x","image/object/part/LElbow/center/y","image/object/part/LElbow/score","image/object/part/RElbow/center/x","image/object/part/RElbow/center/y","image/object/part/RElbow/score","image/object/part/LWrist/center/x","image/object/part/LWrist/center/y","image/object/part/LWrist/score","image/object/part/RWrist/center/x","image/object/part/RWrist/center/y","image/object/part/RWrist/score","image/object/part/LHip/center/x","image/object/part/LHip/center/y","image/object/part/LHip/score","image/object/part/RHip/center/x","image/object/part/RHip/center/y","image/object/part/RHip/score","image/object/part/LKnee/center/x","image/object/part/LKnee/center/y","image/object/part/LKnee/score","image/object/part/RKnee/center/x","image/object/part/RKnee/center/y","image/object/part/RKnee/score","image/object/part/LFoot/center/x","image/object/part/LFoot/center/y","image/object/part/LFoot/score","image/object/part/RFoot/center/x","image/object/part/RFoot/center/y","image/object/part/RFoot/score"]
    #     # csv_path = ".\static\pose_query/input/data.csv"
    #     # with open(csv_path, 'w') as file:
    #     #     line = ','.join(map(str, header))
    #     #     file.write(line + '\n')
    #     #     line = ','.join(map(str, pose_query))
    #     #     file.write(line + '\n')

    #     # file_path = r"C:\Users\NHAN\UIT_HK5\Truy_van_ttdpt\final_project\Img_retrieval\human_pose\infer_test.py"
    #     # # Chạy infer32.py
    #     # # Thực thi lệnh để chạy file infer.py
    #     # try:
    #     #     subprocess.run(["python", file_path])
    #     # except FileNotFoundError:
    #     #     print("Lỗi: Không tìm thấy file infer.py")
    #     # except Exception as e:
    #     #     print("Lỗi:", e)
        
    #     embed_path = ".\static\pose_query/output"
    #     # pose_query_embed = load_pose_embed(embed_path)
    #     array_list = [5.848838388919830322e-02,-1.744573354721069336e+00,4.045882701873779297e+00,2.022864103317260742e+00,1.193807482719421387e+00,1.224218904972076416e-01,-4.967531859874725342e-01,9.628050327301025391e-01,-1.000905185937881470e-01,1.057646155357360840e+00,3.255387783050537109e+00,3.353397846221923828e-01,-1.785410642623901367e+00,3.120568752288818359e+00,-1.629468560218811035e+00,7.511404156684875488e-01,1.988093376159667969e+00,1.556810259819030762e+00,-1.413368463516235352e+00,2.498430907726287842e-01,-3.488969564437866211e+00,-3.874235868453979492e+00,-6.462529897689819336e-01,-1.724012851715087891e+00,1.588860630989074707e+00,1.525178313255310059e+00,5.877851247787475586e-01,3.747017383575439453e-01,1.109389424324035645e+00,-1.467525243759155273e+00,2.962336301803588867e+00,-1.087930560111999512e+00
    #     ]
    #     pose_query_embed = np.array(array_list).reshape(1,-1)
        
    #     print(pose_query_embed.shape)
    #     pose_query = pose_query_embed[0]
    #     # print(vector_pose_db.shape)
    #     k_value = request.form['k_value']
    #     K_value = int(k_value) if k_value and k_value.isdigit() else 80
    #     result = retrieval_pose(pose_query,vector_pose_db,K_value)
    #     results = [image_paths_pose[str(id)] for id in result]
    #     return render_template('index1.html', result=results, k_value=k_value)

        
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
    language = request.form['language']

    if (language == 'vietnamese'):
        eng_clip_query = translate(clip_query)
    else:
        eng_clip_query = clip_query
    print(eng_clip_query)

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
        result_clip = text_retrieval(model, eng_clip_query, K_value, device, vector_db)
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
