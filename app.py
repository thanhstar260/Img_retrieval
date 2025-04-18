from flask import Flask, render_template, request, send_from_directory, jsonify
from utils.image import img2img as image_retrieval
from utils.text import load_clip_feature, load_image_path, load_model, create_faiss_index
from utils.text import text2img as text_retrieval
from utils.combine_results import combine_2results, combine_3results
from utils.search_ocr import ocr_result
from utils.search_asr import asr_result 
import torch
import meilisearch
import json


app = Flask(__name__, static_folder='static')

feature_folder_path = r'.\DATA\clip-features-vit-b32'
image_path_dict = r".\utils\image_path.json"
# youtube_path_dict = r'.\utils\id2link.json'
client = meilisearch.Client('https://ms-cd3d65ab69ae-7424.sgp.meilisearch.io', 'e17ddafe4eea648822355f14d326b3a478bd7141')

# with open(youtube_path_dict, "r") as json_file:
#     youtube_path = json.load(json_file)
    
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
        results = [image_paths[str(id)] for id in result]

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
        results = [image_paths[str(id)] for id in result]
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
    # print(result_clip)
    # print(result_ocr)
    # print(result_asr)
    # print(result)

    results = [image_paths[str(id)] for id in result]

    return render_template('index.html', result=results)

if __name__ == '__main__':
    app.run(debug=True)
