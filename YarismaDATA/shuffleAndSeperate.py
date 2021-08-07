import os
import random

source_path = "YarismaData"
main_folder = "DATA"
subfolders = ["train", "val", "test"]
ratios = [0.7, 0.1]  # train, val

filenames = [i for i in os.listdir(source_path) if i[-4:] == ".jpg"]
filenames.sort()
random.seed(45)
random.shuffle(filenames)  # shuffles the ordering of filenames (deterministic given the chosen seed)

split_1 = int(ratios[0] * len(filenames))
split_2 = split_1 + int(ratios[1] * len(filenames))
train_filenames = filenames[:split_1]
val_filenames = filenames[split_1:split_2]
test_filenames = filenames[split_2:]

try:
    os.mkdir(main_folder)
    print("Directory ", main_folder, " Created ")
except FileExistsError:
    print("Directory ", main_folder, " already exists")

for i in subfolders:
    try:
        os.mkdir(main_folder + "/" + i)
        print("Directory ", main_folder + "/" + i, " Created ")
    except FileExistsError:
        print("Directory ", main_folder + "/" + i, " already exists")

for i in train_filenames:
    os.replace(source_path + "/" + i, main_folder + "/" + subfolders[0] + "/" + i)
    try:
        os.replace(source_path + "/" + i[:-4] + ".txt",
                   main_folder + "/" + subfolders[0] + "/" + i[:-4] + ".txt")
    except FileNotFoundError:
        continue

for i in val_filenames:
    os.replace(source_path + "/" + i, main_folder + "/" + subfolders[1] + "/" + i)
    try:
        os.replace(source_path + "/" + i[:-4] + ".txt",
                   main_folder + "/" + subfolders[1] + "/" + i[:-4] + ".txt")
    except FileNotFoundError:
        continue

for i in test_filenames:
    os.replace(source_path + "/" + i, main_folder + "/" + subfolders[2] + "/" + i)
    try:
        os.replace(source_path + "/" + i[:-4] + ".txt",
                   main_folder + "/" + subfolders[2] + "/" + i[:-4] + ".txt")
    except FileNotFoundError:
        continue
os.rmdir(source_path)
print("Done...")
