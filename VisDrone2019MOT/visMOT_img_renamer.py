import os

folder_path = "VisDrone2019-MOT-train/sequences"
prefix = "_"
count = 0

if folder_path[-1] == "/":
    folder_path = folder_path[:-1]

for foldername in os.listdir(folder_path):
    for filename in os.listdir(folder_path + "/" + foldername):
        if count % 10 == 0:
            print("Renaming", foldername + "/" + filename, "to", foldername + prefix + str(int(filename[:-4]))
                  + filename[-4:])
        os.rename(folder_path + "/" + foldername + "/" + filename, folder_path + "/" + foldername + "/" + foldername
                  + prefix + str(int(filename[:-4])) + filename[-4:])
        count += 1
print("\nAll done.\n")
print(f"The number of renamed files is {count}.")
