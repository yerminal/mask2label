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

for order, filename in enumerate(os.listdir("ulasimDATA/VisDrone2019-DET-train/annotations/")):
    print(order, "=", filename)
    img = cv2.imread("ulasimDATA/VisDrone2019-DET-train/images/" + filename[:-4] + ".jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h_img, w_img = gray.shape
    with open("ulasimDATA/VisDrone2019-DET-train/annotations/" + filename, "r+") as f:
        lines = f.read().splitlines()
        f.truncate(0)
        f.seek(0)
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
            f.write(f"{object_class} {(x + w / 2) / w_img} {(y + h / 2) / h_img} {w / w_img} {h / h_img}")
            if i != lines[-1]:
                f.write("\n")

# for i in lines:
#     lst = i.split(",")
#     lst.pop(7)
#     lst.pop(6)
#     lst.pop(4)
#     lst = list(map(int, lst))
#     x, y, w, h = lst[0], lst[1], lst[2], lst[3]
#     object_class = classes_dataset[lst[4]]
#     cv2.rectangle(img, (x, y), (x + w, y + h), colors[object_class], 1)
#     cv2.putText(img, classes[object_class], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
#                 0.6, colors[object_class], 2)

# cv2.imshow("test", img)
# cv2.waitKey(0)

# cv2.putText(image, classes[0], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

# img = cv2.imread("ulasimDATA/VisDrone2019-DET-train/images/0000002_00005_d_0000014.jpg")
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# h_img, w_img = gray.shape
# objects = []
# ROI_number = 0
# cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]
# for c in cnts:
#     x, y, w, h = cv2.boundingRect(c)
#     cv2.rectangle(img, (x, y), (x + w, y + h), (26, 245, 55), 1)
#     objects.append([(x + w / 2) / w_img, (y + h / 2) / h_img, w / w_img, h / h_img])
#             # ROI is to take the image inside the box.
#             # ROI = img[y:y+h, x:x+w]  # if you want 1 channel (gray image) - ROI = gray[y:y+h, x:x+w]
#             # cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
#             # ROI_number += 1
#
#
# cv2.imshow("test", img)
# cv2.waitKey(0)
