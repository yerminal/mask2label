# This script creates txt files from labels and put all files into one main folder.
# PART 1
# Creating txt files
import cv2
import json
import os

images_path = './'
file_path = "./veriler.json"
countForTxt = 0
countForImage = 0
counter = {"B160519_V1_K1": 0, "T190619_V1_K1": 0, "T190619_V2_K1": 0, "T190619_V3_K1": 0}
obj_class = {"arac": 0, "yaya": 1}
background_images = []

with open(file_path) as json_file:
    data = json.load(json_file)
    for order, jsn in enumerate(data['frameler']):
        url = images_path + jsn['frame_url']
        counter[str(jsn['frame_url'])[:13]] += 1
        countForImage += 1
        objs = jsn['objeler']
        if len(objs) != 0:
            image = cv2.imread(url, cv2.IMREAD_UNCHANGED)
            h_img, w_img, _ = image.shape
            with open(url[:-4] + ".txt", "w") as f:
                for o in objs:
                    try:
                        x, y, w, h = int(o['x0']), int(o['y0']), int(o['x1']) - int(o['x0']), int(o['y1']) - int(o['y0'])
                        object_class = obj_class[o['tur']]
                        f.write(f"{object_class} {(x + w / 2) / w_img} {(y + h / 2) / h_img} {w / w_img} {h / h_img}")
                        if o != objs[-1]:
                            f.write("\n")
                    except KeyError:
                        continue
            countForTxt = countForTxt + 1
        else:
            background_images.append(jsn['frame_url'])
        if order % 50 == 0:
            print(url + "...")

print(f"\nThe number of created txt files: {countForTxt}")
print(f"The number of total images: {countForImage}")
print(f"The number of total background images: {countForImage-countForTxt}\n")
print(counter)

print("Creating txt files done...\n")

# PART 2
# Uniting and Renaming

folder_path_list = ["B160519_V1_K1", "T190619_V1_K1", "T190619_V2_K1", "T190619_V3_K1"]
prefix = "frame"
unite_folders = True
united_folder_path = "YarismaData"
number = 0  # initial number of renaming

if unite_folders:
    try:
        os.mkdir(united_folder_path)
        print("Directory ", united_folder_path, " Created ")
    except FileExistsError:
        print("Directory ", united_folder_path, " already exists")

    for folder_path in folder_path_list:
        files = [i for i in os.listdir(folder_path) if i[-4:] == ".jpg"]
        for filename in files:
            os.rename(folder_path + "/" + filename,
                      united_folder_path + "/" + prefix + str(number) + filename[-4:])
            if folder_path + "/" + filename not in background_images:
                os.rename(folder_path + "/" + filename[:-4] + ".txt",
                          united_folder_path + "/" + prefix + str(number) + ".txt")
            number = number + 1
    for folder_path in folder_path_list:
        os.rmdir(folder_path)
else:
    for folder_path in folder_path_list:
        files = [i for i in os.listdir(folder_path) if i[-4:] == ".jpg"]
        for filename in files:
            os.rename(folder_path + "/" + filename,
                      folder_path + "/" + prefix + str(number) + filename[-4:])
            if folder_path + "/" + filename not in background_images:
                os.rename(folder_path + "/" + filename[:-4] + ".txt",
                          folder_path + "/" + prefix + str(number) + ".txt")
            number = number + 1
        number = 0
print("Uniting and Renaming done...")
print("All done...")
