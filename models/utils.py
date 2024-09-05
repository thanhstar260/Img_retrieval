from deep_translator import GoogleTranslator
import matplotlib.pyplot as plt
import json
from PIL import Image
import os
import numpy as np

def translate(string):
    try:
        # print('ita_string: ', string)
        string_translated = GoogleTranslator(
            source='auto', target='en').translate(string)
        # print('string_translated: ', string_translated)
        return string_translated
    except Exception as e:
        string_translated = ''
        print("Errore per ita_string '{}' - caption '{}' - errore: {}".format(string))
        return string_translated
    
    
# def visualize(image_path, result, k=None, figsize=(20, 10), size = 4):
#     if k is None:
#         k = len(result)
#     axes = []
#     grid_size = k // 8 if k % 8 == 0 else (k // 8) + 1
#     fig = plt.figure(figsize=figsize)

#     for id in range(k):
#         draw_image = result[id]
#         axes.append(fig.add_subplot(grid_size, 8, id + 1))
#         axes[-1].set_title(image_path[str(draw_image)][-17:-4])
#         axes[-1].set_xticks([])
#         axes[-1].set_yticks([])
#         plt.imshow(Image.open(image_path[str(draw_image)]))

#     fig.tight_layout()
#     plt.show()

def visualize(image_path, result, k=None, images_per_row=4, figsize=(20, 10)):
    if k is None:
        k = len(result)
    # axes = []
    grid_size = k // images_per_row if k % images_per_row == 0 else (k // images_per_row) + 1
    fig = plt.figure(figsize=figsize)

    for id in range(k):
        draw_image = result[id]
        ax = fig.add_subplot(grid_size, images_per_row, id + 1)
        ax.set_title(image_path[str(draw_image)][-17:-4])
        ax.set_xticks([])
        ax.set_yticks([])
        img = Image.open(image_path[str(draw_image)])
        ax.imshow(img)
        ax.set_aspect('auto')  # Đảm bảo ảnh không bị biến dạng và lớn hơn

    fig.tight_layout()
    plt.show()
    
    
def load_image_path(image_path_dict):
    with open(image_path_dict, "r") as json_file:
        image_path = json.load(json_file)
    return image_path


def calculate_iou(bbox1, bbox2):
    x1, y1, x2, y2 = bbox1
    x1_, y1_, x2_, y2_ = bbox2

    xi1 = max(x1, x1_)
    yi1 = max(y1, y1_)
    xi2 = min(x2, x2_)
    yi2 = min(y2, y2_)

    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)

    bbox1_area = (x2 - x1) * (y2 - y1)
    bbox2_area = (x2_ - x1_) * (y2_ - y1_)

    union_area = bbox1_area + bbox2_area - inter_area

    iou = inter_area / union_area
    return iou


def weighted_average(values):
    if not values:  # Kiểm tra nếu danh sách trống
        return 0
    
    weighted_sum = sum(x ** 2 for x in values)
    sum_of_weights = sum(values)
    
    if sum_of_weights == 0:  # Tránh chia cho 0
        return 0
    
    return weighted_sum / sum_of_weights


def load_features(feature_folder_path):
    array_list = []

    for file_name in os.listdir(feature_folder_path):
        if file_name.endswith(".npy"):
            file_path = os.path.join(feature_folder_path, file_name)
            array = np.load(file_path)
            array_list.append(array)
            
    features = np.concatenate(array_list, axis=0)
    return features


def rrf(ids, k=60):
    print(ids)
    scores = {}
    for i in range(len(ids)):
        for id in ids[i]:
            if id not in scores:
                scores[id] = 0
            rank = ids[i].index(id)
            scores[id] += 1 / (k + rank)
    scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    ids, scores = list(scores.keys()), list(scores.values())
    return ids, scores