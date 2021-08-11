"""
This script is copying desired classes (and skipping forbidden classes) and changing class ids with the intended number.
"""
import os
import shutil

coco_class_list = ['aeroplane', 'apple', 'backpack', 'banana', 'baseball bat', 'baseball glove', 'bear', 'bed', 'bench',
                   'bicycle', 'bird', 'boat', 'book', 'bottle', 'bowl', 'broccoli', 'bus', 'cake', 'car', 'carrot',
                   'cat', 'cell phone', 'chair', 'clock', 'cow', 'cup', 'diningtable', 'dog', 'donut', 'elephant',
                   'fire hydrant', 'fork', 'frisbee', 'giraffe', 'hair drier', 'handbag', 'horse', 'hot dog',
                   'keyboard', 'kite', 'knife', 'laptop', 'microwave', 'motorbike', 'mouse', 'orange', 'oven',
                   'parking meter', 'person', 'pizza', 'pottedplant', 'refrigerator', 'remote', 'sandwich', 'scissors',
                   'sheep', 'sink', 'skateboard', 'skis', 'snowboard', 'sofa', 'spoon', 'sports ball', 'stop sign',
                   'suitcase', 'surfboard', 'teddy bear', 'tennis racket', 'tie', 'toaster', 'toilet', 'toothbrush',
                   'traffic light', 'train', 'truck', 'tvmonitor', 'umbrella', 'vase', 'wine glass', 'zebra']

# wanted_classes: This is the list of classes that are not going to be deleted.
wanted_classes = ["train"]  #

# forbidden_classes: If the txt file has a class in this list, the txt file and the corresponding image file will be
# deleted.
forbidden_classes = ['aeroplane', 'apple', 'backpack', 'banana', 'baseball bat', 'baseball glove', 'bear', 'bed', 'bench',
                   'bicycle', 'bird', 'boat', 'book', 'bottle', 'bowl', 'broccoli', 'cake', 'carrot',
                   'cat', 'cell phone', 'chair', 'clock', 'cow', 'cup', 'diningtable', 'dog', 'donut', 'elephant',
                   'fire hydrant', 'fork', 'frisbee', 'giraffe', 'hair drier', 'handbag', 'horse', 'hot dog',
                   'keyboard', 'kite', 'knife', 'laptop', 'microwave', 'mouse', 'orange', 'oven',
                   'parking meter', 'person', 'pizza', 'pottedplant', 'refrigerator', 'remote', 'sandwich', 'scissors',
                   'sheep', 'sink', 'skateboard', 'skis', 'snowboard', 'sofa', 'spoon', 'sports ball', 'stop sign',
                   'suitcase', 'surfboard', 'teddy bear', 'tennis racket', 'tie', 'toaster', 'toilet', 'toothbrush',
                   'traffic light', 'tvmonitor', 'umbrella', 'vase', 'wine glass', 'zebra']

classes_model_ids = {"car": 0, "van": 0, "truck": 0, "bus": 0, "motor": 0, "motorbike": 0, "train": 0, "pedestrian": 1,
                     "people": 1, "person": 1}
count_classes_model = {"car": 0, "truck": 0, "bus": 0, "motorbike": 0, "train": 0, "person": 0}

path_labels = r"E:\UlasimDataYarisma\ALLdatasets\COCO\train\labels"
path_images = r"E:\UlasimDataYarisma\ALLdatasets\COCO\train\images"

label_destination = r"E:\UlasimDataYarisma\ALLdatasets\COCO_COPY\labels"
image_destination = r"E:\UlasimDataYarisma\ALLdatasets\COCO_COPY\images"

count = 0
label_direc = os.listdir(path_labels)
total_image = len(label_direc)

# Checking the format of paths
if path_labels[-1] == "/":
    path_labels = path_labels[:-1]
if path_images[-1] == "/":
    path_images = path_images[:-1]
if label_destination[-1] == "/":
    label_destination = label_destination[:-1]

for filename in label_direc:
    wanted_lines = []
    temp = count_classes_model.copy()
    f_coco = open(path_labels + "/" + filename, "r")
    write_file = True
    lines = f_coco.read().splitlines()
    f_coco.close()
    for i in lines:
        lst = i.split(" ")
        if coco_class_list[int(lst[0])] in forbidden_classes:
            write_file = False
            break
        if coco_class_list[int(lst[0])] in wanted_classes:
            temp[coco_class_list[int(lst[0])]] += 1
            line = str(classes_model_ids[coco_class_list[int(lst[0])]]) + " " + " ".join(lst[1:])
            wanted_lines.append(line)
    if write_file:
        if count % 100 == 0:
            print("Creating " + filename + "...")
        count += 1
        count_classes_model = temp.copy()
        f_label = open(label_destination + "/" + filename, "w")
        f_label.write("\n".join(wanted_lines))
        f_label.close()
        shutil.copy(path_images + "/" + filename[:-4] + ".jpg", image_destination)

print("\nAll done.\n")
print(f"The number of total images is {total_image}.")
print(f"The number of copied images is {count}.")
print("The sample number of each classes:")
print(count_classes_model)
