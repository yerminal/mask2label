import cv2
import json

images_path = './'
file_path = "./veriler.json"
countForTxt = 0
countForImage = 0
counter = {"B160519_V1_K1": 0, "T190619_V1_K1": 0, "T190619_V2_K1": 0, "T190619_V3_K1": 0}
obj_class = {"arac": 0, "yaya": 1}

with open(file_path) as json_file:
    data = json.load(json_file)
    for order, jsn in enumerate(data['frameler']):
        url = images_path + jsn['frame_url']
        counter[str(jsn['frame_url'])[:13]] += 1
        countForImage += 1
        objs = jsn['objeler']
        image = cv2.imread(url, cv2.IMREAD_UNCHANGED)
        h_img, w_img, _ = image.shape
        if len(objs) != 0:
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
        if order % 50 == 0:
            print(url + "...")

print(f"\nThe number of created txt files: {countForTxt}")
print(f"The number of total images: {countForImage}")
print(f"The number of total background images: {countForImage-countForTxt}\n")
print(counter)
