import pandas as pd
import json

# Định nghĩa biến path và đuôi file mới
path_json = r"C:\Users\admin\Projects\AIC\image_path.json"
path_csv = r"C:\Users\admin\Projects\AIC\data.csv"

df = pd.read_csv(path_csv)
values = df['new_idx'].tolist()
with open(path_json) as json_file:
    json_data = json.load(json_file)
# keys = list(json_data.values())
keys = df['link'].tolist()
data = {}

print(len(keys))
print(len(values))

for i in range(len(keys)):
    key = values[i]
    value = keys[i]
    data[key] = value
    # data.append[result]

print(len(data))
with open("id2link.json", "w") as f:
    json.dump(data, f)

# print(value[:10])
# print(key[:10])
