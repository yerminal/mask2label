import json
import os

file_path = "./veriler.json"
count = 0
frames = []
folder_path_list = ["B160519_V1_K1", "T190619_V1_K1", "T190619_V2_K1", "T190619_V3_K1"]
with open(file_path) as json_file:
    data = json.load(json_file)
    for jsn in data['frameler']:
        frames.append(jsn['frame_url'])

for folder_path in folder_path_list:
    for filename in os.listdir(folder_path):
        if folder_path + "/" + filename not in frames:
            count = count + 1
            print(count)
            os.remove(folder_path + "/" + filename)
