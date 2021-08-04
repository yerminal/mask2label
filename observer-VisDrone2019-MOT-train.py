import os
import cv2

classes_dataset = {0: "ignored regions", 1: "pedestrian", 2: "people", 3: "bicycle",
                   4: "car", 5: "van", 6: "truck",
                   7: "tricycle", 8: "awning-tricycle", 9: "bus", 10: "motor", 11: "others"}

colors = {0: (192, 192, 192), 1: (0, 0, 255), 2: (12, 32, 255), 3: (54, 234, 100),
          4: (0, 255, 0), 5: (132, 35, 123), 6: (121, 98, 43),
          7: (34, 67, 123), 8: (43, 134, 213), 9: (244, 242, 12), 10: (101, 110, 10),
          11: (20, 220, 20)}

classes_model = {"car": 0, "van": 0, "truck": 0, "bus": 0, "motor": 0, "pedestrian": 1, "people": 1}

for order, filename in enumerate(os.listdir("VisDrone2019-MOT-train/annotations/")):
    frameDict = dict()
    with open("VisDrone2019-MOT-train/annotations/" + filename, "r") as f:
        lines = f.read().splitlines()
        for i in lines:
            lst = i.split(",")
            try:
                frameDict[lst[0]].append(",".join(lst[1:]))
            except KeyError:
                frameDict[lst[0]] = [",".join(lst[1:])]
    for frameID in frameDict.keys():
        nameIMG = "".join(["0" for _ in range(7 - len(frameID))]) + frameID
        pathIMG = "VisDrone2019-MOT-train/sequences/" + filename[:-4] + "/" + nameIMG + ".jpg"
        img = cv2.imread(pathIMG)
        for obj in frameDict[frameID]:
            lst = list(map(int, obj.split(",")))
            x, y, w, h = lst[1], lst[2], lst[3], lst[4]
            classOBJ = lst[6]
            cv2.rectangle(img, (x, y), (x + w, y + h), colors[classOBJ], 1)
            cv2.putText(img, classes_dataset[classOBJ], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, colors[classOBJ], 2)
        cv2.imshow("test", img)
        cv2.waitKey(17)  # 60 FPS
cv2.destroyAllWindows()
