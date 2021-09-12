import os
import cv2

def yolo2rect(xc,yc,wn,hn,w_img,h_img):
    w = wn * w_img
    h = hn * h_img
    x1 = xc * w_img - w / 2
    y1 = yc * h_img - h / 2
    x2 = x1 + w
    y2 = y1 + h
    return int(x1), int(y1), int(x2), int(y2)

anno_path = "train"
img_path = "train"

anno_file_list = [x for x in os.listdir(anno_path) if x.endswith("txt")]
img_file_list = [x for x in os.listdir(img_path) if x.endswith("jpg")]

num2str_classes = {0: "vehicle", 1: "person", 2: "uap", 3: "uai"}

colors = {0: (255, 0, 0), 1: (0, 0, 255), 2: (0, 255, 0), 3: (50, 10, 144)}

for anno_filename in anno_file_list:
    img_file = img_path + "/" + anno_filename[:-3] + "jpg"
    img = cv2.imread(img_file)
    h_img, w_img = img.shape[:2]
    with open(anno_path + "/" + anno_filename, "r") as f:
        lines = f.read().splitlines()
        for i in lines:
            lst = i.split(" ")
            classOBJ = int(lst[0])
            xc, yc, wn, hn = float(lst[1]), float(lst[2]), float(lst[3]), float(lst[4])
            x1, y1, x2, y2 = yolo2rect(xc,yc,wn,hn,w_img,h_img)
            cv2.rectangle(img, (x1, y1), (x2, y2), colors[classOBJ], 1)
            cv2.putText(img, num2str_classes[classOBJ], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, colors[classOBJ], 2)
    # scale_percent = 80
    # width = int(w_img * scale_percent / 100)
    # height = int(h_img * scale_percent / 100)
    # resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    # img = resized
    print(f"Current image: {img_file}")
    cv2.namedWindow("Output")
    cv2.moveWindow("Output", 40, 30)
    cv2.imshow("Output", img)
    cv2.waitKey(0)
cv2.destroyAllWindows()
