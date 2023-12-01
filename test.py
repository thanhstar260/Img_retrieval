import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
import json


input_file = r"C:\Users\admin\Projects\AIC\DATA\ocr\coordinate"
save_path = r"C:\Users\admin\Projects\AIC\DATA\ocr\coordinate1"
# old_path = "C:\\Users\\admin\\Projects\\AIC\\DATA\\Keyframes\\Keyframes_L01\\L01_V001\\0001.jpg"
# new_path = ".\\DATA\\Keyframes\\Keyframes_L01\\L01_V001\\0001.jpg"

# path = os.path.join(".",old_path[-46:])
# print(path)
# img = Image.open(path)
# plt.imshow(img)
# plt.show()


index = 0
for path_det in os.listdir(input_file):
    keyframe_path = os.path.join(input_file, path_det)
    save_text_path = os.path.join(save_path,path_det)
    # print(save_text_path)
    os.makedirs(save_text_path, exist_ok=True)
    print("Save path: ",save_text_path)

    for keyframes in os.listdir(keyframe_path):

        path_file = os.path.join(keyframe_path,keyframes)
        # Đọc dữ liệu từ tệp JSON gốc
        with open(path_file, 'r',encoding="utf-8") as f:
            data = json.load(f)
        # print(len(data))
        # Tạo một từ điển mới có khóa được thay thế bằng đường dẫn tương đối
        new_data = {os.path.join(".",key[-46:]): value for key, value in data.items()}
        # print(len(new_data))
        # Đường dẫn đến tệp JSON mới
        output_file = os.path.join(save_text_path,keyframes)

        # Ghi dữ liệu vào tệp JSON mới
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(new_data, f, indent=4)

    print(f"Done {path_det}")