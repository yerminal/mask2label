import os
import cv2
import shutil

classes_dataset = {0: "ignored regions", 1: "pedestrian", 2: "people", 3: "bicycle",
                   4: "car", 5: "van", 6: "truck",
                   7: "tricycle", 8: "awning-tricycle", 9: "bus", 10: "motor", 11: "others"}

colors = {0: (192, 192, 192), 1: (0, 0, 255), 2: (12, 32, 255), 3: (54, 234, 100),
          4: (0, 255, 0), 5: (132, 35, 123), 6: (121, 98, 43),
          7: (34, 67, 123), 8: (43, 134, 213), 9: (244, 242, 12), 10: (101, 110, 10),
          11: (20, 220, 20)}

classes_model = {"car": 0, "van": 0, "truck": 0, "bus": 0, "motor": 0, "pedestrian": 1, "people": 1}

prefix = "det_train"
for order, filename in enumerate(os.listdir("VisDrone2019-DET-val/annotations/")):
    img = cv2.imread("VisDrone2019-DET-val/images/" + filename[:-4] + ".jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h_img, w_img = gray.shape
    data = []
    vehicle_sum = 0
    person_sum = 0
    classes_count = {"car": 0, "van": 0, "truck": 0, "bus": 0, "motor": 0, "pedestrian": 0, "people": 0}
    with open("VisDrone2019-DET-val/annotations/" + filename, "r") as f:
        lines = f.read().splitlines()
        for i in lines:
            lst = i.split(",")
            if lst[-1] == '':
                del lst[-1]
            lst.pop(7)
            lst.pop(6)
            lst.pop(4)
            lst = list(map(int, lst))
            x, y, w, h = lst[0], lst[1], lst[2], lst[3]
            if classes_dataset[lst[4]] not in classes_model.keys():
                continue
            object_class = classes_model[classes_dataset[lst[4]]]
            classes_count[classes_dataset[lst[4]]] += 1
            data.append(f"{object_class} {(x + w / 2) / w_img} {(y + h / 2) / h_img} {w / w_img} {h / h_img}")

    vehicle_sum += classes_count["car"]
    vehicle_sum += classes_count["van"]
    vehicle_sum += classes_count["truck"]
    vehicle_sum += classes_count["bus"]
    vehicle_sum += classes_count["motor"]
    person_sum += classes_count["pedestrian"]
    person_sum += classes_count["people"]

    if person_sum / (vehicle_sum + person_sum) >= 0.2:
        continue
    else:
        with open("VisDrone2019-DET-val/all/" + prefix + "_" + str(order) + ".txt", "w") as f:
            f.write("\n".join(data))
        shutil.copy("VisDrone2019-DET-val/images/" + filename[:-4] + ".jpg", "VisDrone2019-DET-val/all/" + prefix + "_" + str(order) + ".jpg")
        
