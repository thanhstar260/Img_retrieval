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

def result_id(client,text_query,k):

    results = client.index("asr").search(
        text_query,{"limit": k}
    )["hits"]
    ids = []
    for result in results:
        id = list(range(int(result["start"]),int(result["end"])))
        ids.extend(id)
    print(ids)
    return ids

if __name__ == "__main__":

    # DEFINE PARAMETER

    image_path_dict = r"C:\Users\admin\Projects\AIC\image_path.json"
    text_query = "chạm tay trong vòng cấm"
    K = 40
    client = meilisearch.Client('https://edge.meilisearch.com', 'bc61b7bb01eb45353ed231d2f88750729ddbbac9')
    image_path = load_image_path(image_path_dict)

    result = result_id(client,text_query=text_query,k=K)
    visualize(result, K,image_path=image_path)