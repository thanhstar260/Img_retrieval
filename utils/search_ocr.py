# Test seach by text_ocr + meilisearch 
import meilisearch
import json
from PIL import Image
import os
import matplotlib.pyplot as plt
import json


def visualize(result,k,image_path):
    axes = []
    grid_size = k//8
    fig = plt.figure(figsize=(10,5))

    for id in range(k):
        draw_image = result[id]
        axes.append(fig.add_subplot(grid_size + 1, 8, id+1))
        axes[-1].set_title(image_path[str(draw_image)][-17:-4])
        axes[-1].set_xticks([])
        axes[-1].set_yticks([])
        plt.imshow(Image.open(image_path[str(draw_image)]))


    fig.tight_layout()
    plt.show()


def load_image_path(image_path_dict):
    with open(image_path_dict, "r") as json_file:
        image_path = json.load(json_file)
    return image_path

def ocr_result(client,text_query,k):

    result = client.index("ocr").search(
        text_query,{"limit": k}
    )["hits"]

    ids = [item['id'] for item in result]
    return ids

if __name__ == "__main__":

    # DEFINE PARAMETER

    image_path_dict = r"C:\Users\NHAN\UIT_HK5\Truy_van_ttdpt\final_project\Img_retrieval\image_path.json"
    text_query = "giao hàng thiết bị điện"
    K = 16
    client = meilisearch.Client('https://ms-cd3d65ab69ae-7424.sgp.meilisearch.io', 'e17ddafe4eea648822355f14d326b3a478bd7141')
    image_path = load_image_path(image_path_dict)

    result = ocr_result(client,text_query=text_query,k=K)
    visualize(result, K,image_path=image_path)