# convert Key from Path to idx(0-80k)
import meilisearch
import json
import os


# An index is where the documents are stored.
# index = client.index('ocr')
path = r"C:\Users\admin\Projects\AIC\DATA\ocr\text1"
save_path = r"C:\Users\admin\Projects\AIC\DATA\ocr\text3"


id = 0

for key_frame in os.listdir(path)[8:]:
    key_frame_path = os.path.join(path, key_frame)
    key_frame_save = os.path.join(save_path, key_frame)
    os.makedirs(key_frame_save,exist_ok=True)
    for file in os.listdir(key_frame_path):
        new_data = []
        file_path = os.path.join(key_frame_path,file)
        file_save = os.path.join(key_frame_save, file)
        # os.makedirs(key_frame_save,exist_ok=True)

        with open(file_path, "r" , encoding= 'utf-8') as f:
            data = json.load(f)

        for key, value in data.items():
            new_data.append({"id": id+70174, "value": value})
            id += 1

        # Ghi dữ liệu mới vào file JSON
        with open(file_save, "w") as f:
            json.dump(new_data, f, indent=4)

# print(id)