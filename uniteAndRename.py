import os

folder_path_list = ["B160519_V1_K1", "T190619_V1_K1", "T190619_V2_K1", "T190619_V3_K1"]
prefix = "frame"
unite_folders = True
united_folder_path = "YarismaData"
number = 0  # initial number of renaming

if unite_folders:
    try:
        os.mkdir(united_folder_path)
        print("Directory ", united_folder_path, " Created ")
    except FileExistsError:
        print("Directory ", united_folder_path, " already exists")

    for folder_path in folder_path_list:
        files = [i for i in os.listdir(folder_path) if i[-4:] == ".jpg"]
        for filename in files:
            os.rename(folder_path + "/" + filename,
                      united_folder_path + "/" + prefix + str(number) + filename[-4:])
            os.rename(folder_path + "/" + filename[:-4] + ".txt",
                      united_folder_path + "/" + prefix + str(number) + ".txt")
            number = number + 1
    for folder_path in folder_path_list:
        os.rmdir(folder_path)
else:
    for folder_path in folder_path_list:
        files = [i for i in os.listdir(folder_path) if i[-4:] == ".jpg"]
        for filename in files:
            os.rename(folder_path + "/" + filename,
                      folder_path + "/" + prefix + str(number) + filename[-4:])
            os.rename(folder_path + "/" + filename[:-4] + ".txt",
                      folder_path + "/" + prefix + str(number) + ".txt")
            number = number + 1
        number = 0
