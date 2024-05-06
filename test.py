from PIL import Image
from matplotlib import pyplot as plt
# bounding_boxes = [
#     [
#         1006.1771978021978,
#         662.9163265228271,
#         1077.6720467032967,
#         689.804162979126
#     ],
#     [
#         669.9886675824176,
#         662.109260559082,
#         749.1850103021978,
#         689.9256134033203
#     ],
#     [
#         562.5248111263737,
#         664.2561435699463,
#         586.5352850274726,
#         683.1140041351318
#     ],
#     [
#         942.4935611263737,
#         659.8435020446777,
#         1002.0795844780221,
#         691.807279586792
#     ],
#     [
#         753.6427712912089,
#         661.4723539352417,
#         804.9253949175825,
#         685.7294797897339
#     ],
#     [
#         281.31868131868134,
#         662.34375,
#         311.5604395604396,
#         684.84375
#     ],
#     [
#         594.989010989011,
#         660.234375,
#         663.2087912087912,
#         686.25
#     ],
#     [
#         199.53219436813188,
#         659.196982383728,
#         277.81953983516485,
#         689.0361928939819
#     ],
#     [
#         808.5961538461539,
#         659.3685150146484,
#         856.8083791208792,
#         684.8941326141357
#     ],
#     [
#         316.07891912774727,
#         657.1661424636841,
#         374.25515109890114,
#         686.3444566726685
#     ],
#     [
#         383.20570054945057,
#         657.8083276748657,
#         451.6844093406594,
#         689.0645170211792
#     ],
#     [
#         1129.947029532967,
#         657.7170038223267,
#         1183.2148866758243,
#         684.4212484359741
#     ],
#     [
#         497.2983774038462,
#         656.3876581192017,
#         564.0856370192308,
#         688.386025428772
#     ],
#     [
#         129.87621265453296,
#         654.3928670883179,
#         196.67981627747255,
#         688.9051294326782
#     ],
#     [
#         861.9971668956044,
#         655.8440494537354,
#         938.4521806318683,
#         686.3853549957275
#     ],
#     [
#         23.074546059409343,
#         655.7498502731323,
#         81.86310418097528,
#         687.7765417098999
#     ],
#     [
#         1236.1825206043957,
#         655.2168416976929,
#         1278.3882211538462,
#         683.6666250228882
#     ],
#     [
#         455.4804258241759,
#         653.6556243896484,
#         496.30030906593413,
#         684.3649005889893
#     ],
#     [
#         222.24175824175825,
#         611.71875,
#         263.73626373626377,
#         634.921875
#     ],
#     [
#         592.4749742445056,
#         599.6374797821045,
#         667.0643458104396,
#         623.7820816040039
#     ],
#     [
#         670.2169041895605,
#         598.611888885498,
#         737.7709478021978,
#         625.250301361084
#     ],
#     [
#         773.2152300824176,
#         597.4165678024292,
#         843.7023523351648,
#         624.5967435836792
#     ],
#     [
#         901.6263736263737,
#         597.65625,
#         993.7582417582419,
#         621.5625
#     ],
#     [
#         842.1070570054945,
#         595.5176496505737,
#         898.5624141483518,
#         626.8308305740356
#     ],
#     [
#         1086.6690418956046,
#         595.2319622039795,
#         1142.1015625,
#         627.6222324371338
#     ],
#     [
#         999.2775583791209,
#         596.150393486023,
#         1083.9590487637363,
#         622.3645448684692
#     ],
#     [
#         510.59340659340666,
#         596.25,
#         586.5494505494506,
#         623.671875
#     ],
#     [
#         441.6703296703297,
#         594.84375,
#         494.4175824175825,
#         627.890625
#     ],
#     [
#         360.59619677197804,
#         596.1368322372437,
#         438.2182778159341,
#         623.055911064148
#     ],
#     [
#         741.2747252747254,
#         594.140625,
#         770.1098901098902,
#         623.671875
#     ],
#     [
#         112.52747252747254,
#         203.203125,
#         120.96703296703298,
#         208.828125
#     ],
#     [
#         1046.9478880494507,
#         92.72175550460815,
#         1133.2849416208792,
#         111.88785552978516
#     ],
#     [
#         1158.2424450549452,
#         71.47100508213043,
#         1200.8083791208792,
#         106.49513483047485
#     ],
#     [
#         1056.53125,
#         59.29562151432037,
#         1165.6538461538462,
#         91.93779945373535
#     ]
# ]

def group_boxes(boxes):
    groups = []
    current_group = [boxes[0]]

    for box in boxes[1:]:
        prev_box = current_group[-1]
        if abs(box[1] - prev_box[1]) < 10:  # Nếu y chênh lệch nhỏ hơn 10px
            current_group.append(box)
        else:
            groups.append(current_group)
            current_group = [box]

    groups.append(current_group)
    return groups

# Hàm tính toán bounding box mới cho mỗi nhóm

def compute_group_bbox(group, image_width= 1280, image_height = 720):
    x_min = max(min([box[0] for box in group]) - 10, 0)
    y_min = max(group[0][1] - 10, 0)
    x_max = min(max([box[2] for box in group]) + 10, image_width)
    y_max = min(group[-1][3] + 10, image_height)
    return [x_min, y_min, x_max, y_max]


def result_boxes(bounding_boxes):
    # Sắp xếp các bounding box theo giá trị y
    sorted_boxes = sorted(bounding_boxes, key=lambda x: x[1])

    # Hàm gom nhóm các bounding box

    # Gom nhóm các bounding box
    grouped_boxes = group_boxes(sorted_boxes)

    # Tính toán bounding box mới cho mỗi nhóm
    new_boxes = [compute_group_bbox(group) for group in grouped_boxes]
    
    return new_boxes

bounding_boxes = []
# print(result_boxes(bounding_boxes))

def filter_data(data:list):
    filtered_data = []

    # Lặp qua từng phần tử trong danh sách ban đầu
    for item in data:
        # Kiểm tra xem chuỗi "0000" có tồn tại trong phần tử không
        if "0000" not in item:
            # Nếu không tồn tại, thêm phần tử vào danh sách mới
            filtered_data.append(item)
    return filtered_data


# bỏ bớt "0000"
# import json
# import os
# stop = False
# index = 0
# coordinate = r"C:\Users\admin\Projects\AIC\keyframe_convert"
# for filename in os.listdir(coordinate):
#     json_contents = []
#     with open(os.path.join(coordinate, filename), 'r', encoding='utf-8') as json_file:
#         datas = json.load(json_file)
#         for data in datas:
#             dict_new = {}
#             key,value = list(data.items())[0]
#             value = filter_data(value)
#             dict_new["id"] = key
#             dict_new["text"] = value
            
#             json_contents.append(dict_new)
#     output_file_path = f"keyframe_clean/{filename}"
#     with open(output_file_path, 'w', encoding='utf-8') as output_file:
#         json.dump(json_contents, output_file, ensure_ascii=False, indent=4)


import json

# Upload data to meilisearch
import meilisearch
import json
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
HTTP = os.getenv("HTTP")
MASTER_KEY = os.getenv("MASTER_KEY")


client = meilisearch.Client(HTTP, MASTER_KEY)
# An index is where the documents are stored.
# index = client.index('ocr')
save_path_ocr = r"C:\Users\admin\Projects\AIC\final_ocr_clean.json"

print(client.is_healthy())


# ADD OCR
with open(save_path_ocr, 'r', encoding='utf-8') as f:
    data_ocr = json.load(f)

# Define batch size
batch_size = 1000

# Split data into batches and add them to MeiliSearch
for i in range(0, len(data_ocr), batch_size):
    batch = data_ocr[i:i + batch_size]
    try:
        client.index('ocr2').add_documents(batch)
        print(f"Added batch {i//batch_size + 1} to MeiliSearch")
    except Exception as e:
        print(f"Error adding batch {i//batch_size + 1}: {e}")




# # nối thành 1 file
# import json
# import os

# path = r"C:\Users\admin\Projects\AIC\keyframe_clean"

# datas = []
# for filename in os.listdir(path):
#     with open(os.path.join(path, filename), 'r', encoding='utf-8') as json_file:
#         data = json.load(json_file)
    
#     datas.extend(data)

# print(len(datas))
# with open("final_ocr_clean.json", 'w', encoding='utf-8') as output_file:
#     json.dump(datas, output_file, ensure_ascii=False, indent=4)
