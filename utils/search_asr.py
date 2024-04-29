# Test seach by text_asr + meilisearch 
import meilisearch
import json
from PIL import Image
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

def asr_result(client,text_query,k):

    results = client.index("asr").search(
        text_query,{"limit": k}
    )["hits"]
    ids = []
    for result in results:
        id = list(range(int(result["start"]),int(result["end"])+1))
        ids.extend(id)
    return ids[:k]

if __name__ == "__main__":

    # DEFINE PARAMETER

    image_path_dict = r"C:\Users\admin\Projects\AIC\image_path.json"
    text_query = "chạm tay trong vòng cấm"
    K = 40
    client = meilisearch.Client('https://ms-771a4545fc1a-8932.sgp.meilisearch.io', 'a7aa95f4dd64d9a82a0c56e60955f01db6145cfc')
    image_path = load_image_path(image_path_dict)

    result = asr_result(client,text_query=text_query,k=K)
    visualize(result, K,image_path=image_path)