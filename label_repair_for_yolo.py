import os
import cv2

def edit(xc,yc,xw,yh,width=1920,height=1080): # x_center, y_center, x_width, y_width, 1920,1080
    x1 = xc-xw/2
    y1 = yc-yh/2
    x2 = xc+xw/2
    y2 = yc+yh/2
  
    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0
    if x2 > width:
        x2 = width
    if y2 > height:
        y2 = height

    nxc = (x1+x2)/2
    nyc = (y1+y2)/2
    nxw = x2-x1
    nyh = y2-y1
    
    return nxc, nyc, nxw, nyh

paths = ["/content/ULASIM_DATA_v2/train","/content/ULASIM_DATA_v2/test","/content/ULASIM_DATA_v2/val"]
for path in paths:
    file_names = [i for i in os.listdir(path) if i[-4:] == ".txt"]

    for file_name in file_names:
        with open(os.path.join(path, file_name), "r+") as f:
            lines = f.read().splitlines()
            f.truncate(0)
            f.seek(0)
            for i in lines:
                lst = i.split(" ")
                xc, yc, wc, hc = float(lst[1]), float(lst[2]), float(lst[3]), float(lst[4])
                nxc, nyc, nxw, nyh = edit(xc,yc,wc,hc,width=1,height=1)
                lst[1] = nxc
                lst[2] = nyc
                lst[3] = nxw
                lst[4] = nyh
                f.write(f"{lst[0]} {lst[1]} {lst[2]} {lst[3]} {lst[4]}")
                if i != lines[-1]:
                    f.write("\n")
                    
