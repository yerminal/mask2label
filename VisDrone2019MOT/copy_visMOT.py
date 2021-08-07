"""
Copying images and moving them to the intended destination.
And desired number of forward frames can be skipped.
"""
import shutil
import os
import re
import winsound

source = "sequences"
destination = r"D:\UlasimDataYarisma\ALLdatasets\VisDrone2019-MOT-train\new"

freq = 300
dur = 1000

count = 0
skip = 20

for foldername in os.listdir(source):
    dirFiles = os.listdir(source + "/" + foldername)
    dirFiles.sort(key=lambda f: int(re.sub('\D', '', f)))
    i = 0
    print(f"length = {len(dirFiles)}")
    while i < len(dirFiles):
        f1 = dirFiles[i]
        f2 = dirFiles[i + 1]
        for filename in [f1, f2]:
            shutil.copy(source + "/" + foldername + "/" + filename, destination)
            print(f"{filename} copied successfully.")
            count += 1
        print(f"{foldername} - i")
        i += 2 * skip
print("\nAll done.\n")
for _ in range(5):
    winsound.Beep(freq, dur)
print("TOTAL IMAGES COPIED =", str(count))
