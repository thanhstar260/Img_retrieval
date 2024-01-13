from flask import Flask, render_template, request, send_from_directory
from image import img2img as image_retrieval
from text import text2img as text_retrieval
import numpy as np
import torch
import clip
import matplotlib.pyplot as plt
import urllib.parse

app = Flask(__name__, static_folder='static')

# LOAD MODEL

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print("Device:", device)

model, preprocess = clip.load("ViT-B/32")
model.to(device).eval()

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
    K_value = int(k_value) if k_value and k_value.isdigit() else 40
    result = image_retrieval(preprocess, model, img_query_path, K_value, device)
    return render_template('index.html', result=result)

# Route for text retrieval
@app.route('/retrieve_text', methods=['POST'])
def retrieve_text():
    print(request.form)
    text_query = request.form['text_query']
    k_value = request.form['k_value']
    K_value = int(k_value) if k_value and k_value.isdigit() else 40
    result = text_retrieval(model, text_query, K_value, device)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
