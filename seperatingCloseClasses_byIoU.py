import os
import cv2
from itertools import product


def bb_iou(boxA, boxB):
    x, y, w, h = boxA[1], boxA[2], boxA[3], boxA[4]
    boxA = [x, y, x + w, y + h]
    x, y, w, h = boxB[1], boxB[2], boxB[3], boxB[4]
    boxB = [x, y, x + w, y + h]
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the intersection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
    # return the intersection over union value
    return iou


classes_dataset = {0: "ignored regions", 1: "pedestrian", 2: "people", 3: "bicycle",
                   4: "car", 5: "van", 6: "truck",
                   7: "tricycle", 8: "awning-tricycle", 9: "bus", 10: "motor", 11: "others", "s": "XXXXXX"}

colors = {0: (192, 192, 192), 1: (0, 0, 255), 2: (12, 32, 255), 3: (54, 234, 100),
          4: (0, 255, 0), 5: (132, 35, 123), 6: (121, 98, 43),
          7: (34, 67, 123), 8: (43, 134, 213), 9: (244, 242, 12), 10: (101, 110, 10),
          11: (20, 220, 20), "s": (0, 255, 0)}

classes_model = {"car": 0, "van": 0, "truck": 0, "bus": 0, "motor": 0, "pedestrian": 1, "people": 1}

delay = 17  # 60 FPS
iou_threshold = 0.3

for order, filename in enumerate(os.listdir("VisDrone2019-MOT-train/annotations/")):
    print("Order =", order)
    print("Folder =", filename[:-4])
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

        person = list()
        motor = list()
        delete_list = set()
        for obj in frameDict[frameID]:
            lst = list(map(int, obj.split(",")))
            if lst[6] == 1 or lst[6] == 2:  # pedestrian and people
                person.append(obj)
            elif lst[6] == 10:  # motor
                motor.append(obj)
        combination = list(product(person, motor))
        for i in combination:
            person_obj = list(map(int, i[0].split(",")))
            motor_obj = list(map(int, i[1].split(",")))
            if bb_iou(person_obj, motor_obj) >= iou_threshold:
                delete_list.add(i[0])

        for obj in frameDict[frameID]:
            lst = list(map(int, obj.split(",")))
            x, y, w, h = lst[1], lst[2], lst[3], lst[4]
            classOBJ = lst[6]
            if obj in delete_list:
                classOBJ = "s"
                delay = 0
                cv2.rectangle(img, (x, y), (x + w, y + h), colors[classOBJ], 1)
                cv2.putText(img, classes_dataset[classOBJ], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, colors[classOBJ], 2)
            else:
                cv2.rectangle(img, (x, y), (x + w, y + h), colors[classOBJ], 1)
                # cv2.putText(img, classes_dataset[classOBJ], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                #             0.4, colors[classOBJ], 2)
        pixel_product = img.shape[1] * img.shape[0]
        if pixel_product > 2000000:
            scale_percent = 90  # percent of original size
            if pixel_product > 4000000:
                scale_percent = 70
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)
            # resize image
            resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
            img = resized
        cv2.namedWindow("Output")
        cv2.moveWindow("Output", 40, 30)
        cv2.imshow("Output", img)
        cv2.waitKey(delay)
        delay = 17 # 60 FPS
cv2.destroyAllWindows()
