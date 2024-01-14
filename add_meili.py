import meilisearch
import json
import os


client = meilisearch.Client('https://edge.meilisearch.com', 'bc61b7bb01eb45353ed231d2f88750729ddbbac9')
# An index is where the documents are stored.
# index = client.index('ocr')
path = r"C:\Users\admin\Projects\AIC\DATA\ocr\text1"
save_path = r"C:\Users\admin\Projects\AIC\DATA\ocr\text3"
# save_path2 = r"C:\Users\admin\Projects\AIC\DATA\ocr\text3"


# id = 0

# for key_frame in os.listdir(path):
#     key_frame_path = os.path.join(path, key_frame)
#     key_frame_save = os.path.join(save_path, key_frame)
#     os.makedirs(key_frame_save,exist_ok=True)
#     for file in os.listdir(key_frame_path):
#         new_data = []
#         file_path = os.path.join(key_frame_path,file)
#         file_save = os.path.join(key_frame_save, file)
#         # os.makedirs(key_frame_save,exist_ok=True)

#         with open(file_path, "r") as f:
#             data = json.load(f)

#         for key, value in data.items():
#             new_data.append({"id": id, "value": value})
#             id += 1

#         # Ghi dữ liệu mới vào file JSON
#         with open(file_save, "w") as f:
#             json.dump(new_data, f, indent=4)

# print(id)


print(client.is_healthy())

for key_frame in os.listdir(save_path):
    key_frame_path = os.path.join(save_path, key_frame)
    for file in os.listdir(key_frame_path):
        file_path = os.path.join(key_frame_path,file)
        json_file = open(file_path, encoding='utf-8')
        text = json.load(json_file)
        client.index('test').add_documents(text)
        # print(file_path)

