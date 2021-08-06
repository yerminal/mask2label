"""
This script is deleting unnecessary classes and changing class ids with the intended number.
If you want to edit the directory paths, you have to edit each one of them by hand.
"""
import os

coco_class_list = ['aeroplane', 'apple', 'backpack', 'banana', 'baseball bat', 'baseball glove', 'bear', 'bed', 'bench',
                   'bicycle', 'bird', 'boat', 'book', 'bottle', 'bowl', 'broccoli', 'bus', 'cake', 'car', 'carrot', 'cat',
                   'cell phone', 'chair', 'clock', 'cow', 'cup', 'diningtable', 'dog', 'donut', 'elephant', 'fire hydrant',
                   'fork', 'frisbee', 'giraffe', 'hair drier', 'handbag', 'horse', 'hot dog', 'keyboard', 'kite', 'knife',
                   'laptop', 'microwave', 'motorbike', 'mouse', 'orange', 'oven', 'parking meter', 'person', 'pizza', 'pottedplant',
                   'refrigerator', 'remote', 'sandwich', 'scissors', 'sheep', 'sink', 'skateboard', 'skis', 'snowboard', 'sofa',
                   'spoon', 'sports ball', 'stop sign', 'suitcase', 'surfboard', 'teddy bear', 'tennis racket', 'tie', 'toaster',
                   'toilet', 'toothbrush', 'traffic light', 'train', 'truck', 'tvmonitor', 'umbrella', 'vase', 'wine glass', 'zebra']

wanted_classes = ["bus", "car", "person", "train", "truck", "motorbike"]  # The classes that is not going to be deleted.
index_of_classes = [str(coco_class_list.index(i)) for i in wanted_classes]
classes_model = {"car": 0, "van": 0, "truck": 0, "bus": 0, "motor": 0, "motorbike": 0, "train": 0, "pedestrian": 1, "people": 1, "person": 1}
count_classes_model = {"car": 0, "truck": 0, "bus": 0, "motorbike": 0, "train": 0, "person": 0}

count = 0
count_deleted = 0
label_direc = os.listdir("train/labels")
total_image = len(label_direc)

for filename in label_direc:
    if count % 100 == 0:
        print("Editing " + filename + "...")
    count += 1
    wanted_lines = []
    with open("train/labels/" + filename, "r+") as f:
        lines = f.read().splitlines()
        f.truncate(0)
        f.seek(0)
        for i in lines:
            lst = i.split(" ")
            if lst[0] in index_of_classes:
                count_classes_model[coco_class_list[int(lst[0])]] += 1
                line = str(classes_model[coco_class_list[int(lst[0])]]) + " " + " ".join(lst[1:])
                wanted_lines.append(line)
        f.write("\n".join(wanted_lines))
    if os.stat("train/labels/" + filename).st_size == 0:
        os.remove("train/labels/" + filename)
        os.remove("train/images/" + filename[:-4] + ".jpg")
        count_deleted += 1

print("All done.")
print(f"The number of remaining images is {total_image - count_deleted}.")
print(f"The number of deleted images is {count_deleted}.")
print("The sample number of each classes:")
print(count_classes_model)
