"""
This script is deleting unnecessary classes and changing class ids with the intended number.
If you want to edit the directory paths, you have to edit each one of them by hand.
"""
import os

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
wanted_classes = ["bus", "car", "person", "train", "truck", "motorbike"]  #

# forbidden_classes: If the txt file has a class in this list, the txt file and the corresponding image file will be
# deleted.
forbidden_classes = ["apple", "banana", "bed", "bear", "book", "bottle", "bowl", "broccoli", "cake", "carrot",
                     "cell phone", "chair", "clock", "cup", "diningtable", "donut", "elephant", "fork", "giraffe",
                     "hair drier", "horse", "hot dog", "keyboard", "kite", "knife", "laptop", "microwave", "mouse",
                     "orange", "oven", "pizza", "pottedplant", "refrigerator", "remote", "sandwich", "scissors", "sink",
                     "skis", "snowboard", "sofa", "spoon", "sports ball", "surfboard", "teddy bear", "tennis racket",
                     "tie", "toaster", "toilet", "toothbrush", "tvmonitor", "vase", "wine glass", "zebra"]

classes_model_ids = {"car": 0, "van": 0, "truck": 0, "bus": 0, "motor": 0, "motorbike": 0, "train": 0, "pedestrian": 1,
                     "people": 1, "person": 1}
count_classes_model = {"car": 0, "truck": 0, "bus": 0, "motorbike": 0, "train": 0, "person": 0}

path_labels = "train/labels"
path_images = "train/images"

count = 0
count_deleted = 0
label_direc = os.listdir(path_labels)
total_image = len(label_direc)

# Checking the format of paths
if path_labels[-1] == "/":
    path_labels = path_labels[:-1]
if path_images[-1] == "/":
    path_images = path_images[:-1]

for filename in label_direc:
    if count % 100 == 0:
        print("Editing " + filename + " ...")
    count += 1
    wanted_lines = []
    temp = count_classes_model.copy()
    with open(path_labels + "/" + filename, "r+") as f:
        write_file = True
        lines = f.read().splitlines()
        f.truncate(0)
        f.seek(0)
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
            count_classes_model = temp.copy()
            f.write("\n".join(wanted_lines))
    if os.stat(path_labels + "/" + filename).st_size == 0:
        os.remove(path_labels + "/" + filename)
        os.remove(path_images + "/" + filename[:-4] + ".jpg")
        count_deleted += 1

print("\nAll done.\n")
print(f"The number of remaining images is {total_image - count_deleted}.")
print(f"The number of deleted images is {count_deleted}.")
print("The sample number of each classes:")
print(count_classes_model)
