import os
import cv2

classes_dataset = {0: "ignored regions", 1: "pedestrian", 2: "people", 3: "bicycle", 4: "car", 5: "van", 6: "truck",
                   7: "tricycle", 8: "awning-tricycle", 9: "bus", 10: "motor", 11: "others"}

colors = {0: (192, 192, 192), 1: (0, 0, 255), 2: (12, 32, 255), 3: (54, 234, 100), 4: (0, 255, 0), 5: (132, 35, 123),
          6: (121, 98, 43), 7: (34, 67, 123), 8: (43, 134, 213), 9: (244, 242, 12), 10: (101, 110, 10),
          11: (20, 220, 20)}

classes_model = {"car": 0, "van": 0, "truck": 0, "bus": 0, "motor": 0, "pedestrian": 1, "people": 1}

path_annotations = "VisDrone2019-MOT-train/annotations"
path_images = "VisDrone2019-MOT-train/sequences"
prefix = "_"
# Checking the format of paths
if path_annotations[-1] == "/":
    path_labels = path_annotations[:-1]
if path_images[-1] == "/":
    path_images = path_images[:-1]

for order, filename in enumerate(os.listdir(path_annotations)):
    print("Order =", order)
    print("Folder =", filename[:-4] + "\n")
    frameDict = dict()
    with open(path_annotations + "/" + filename, "r") as f:
        lines = f.read().splitlines()
        for i in lines:
            lst = i.split(",")
            try:
                frameDict[lst[0]].append(",".join(lst[1:]))
            except KeyError:
                frameDict[lst[0]] = [",".join(lst[1:])]
    for frameID in frameDict.keys():
        pathIMG = path_images + "/" + filename[:-4] + "/" + filename[:-4] + prefix + frameID + ".jpg"
        img = cv2.imread(pathIMG)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h_img, w_img = gray.shape
        with open(pathIMG[:-4] + ".txt", "w") as f:
            for obj in frameDict[frameID]:
                lst = list(map(int, obj.split(",")))
                if classes_dataset[int(lst[6])] not in classes_model.keys():
                    continue
                x, y, w, h = lst[1], lst[2], lst[3], lst[4]
                classOBJ = classes_model[classes_dataset[int(lst[6])]]
                f.write(f"{classOBJ} {(x + w / 2) / w_img} {(y + h / 2) / h_img} {w / w_img} {h / h_img}")
                if obj != frameDict[frameID][-1]:
                    f.write("\n")
print("\nAll done.\n")
