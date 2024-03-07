import os
import json
save_path_ocr = r"C:\Users\admin\Projects\AIC\DATA\ocr\text2"
save_path_asr = r"C:\Users\admin\Projects\AIC\DATA\asr\final_asr.json"



# ocr
data = []
for key_frame in os.listdir(save_path_ocr):
    key_frame_path = os.path.join(save_path_ocr, key_frame)
    for file in os.listdir(key_frame_path):
        file_path = os.path.join(key_frame_path,file)
        json_file = open(file_path, encoding='utf-8')
        text = json.load(json_file)
        # print(text)
        data.extend(text)
        # print(file_path)

with open("final_ocr.json", "w") as outfile:
    json.dump(data, outfile)
