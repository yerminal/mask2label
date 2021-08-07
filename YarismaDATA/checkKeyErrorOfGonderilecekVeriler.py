import cv2
import json

images_path = './'

file_path = "./veriler.json"
countForKeyError = 0
count = 0
d = {"B160519_V1_K1": 0, "T190619_V1_K1": 0, "T190619_V2_K1": 0, "T190619_V3_K1": 0}
with open(file_path) as json_file:
    data = json.load(json_file)
    # print(data)
    for jsn in data['frameler']:
        url = images_path + jsn['frame_url']
        d[str(jsn['frame_url'])[:13]] += 1
        objs = jsn['objeler']
        image = cv2.imread(url, cv2.IMREAD_COLOR)
        for order, o in enumerate(objs):
            try:
                if (o['tur'] == 'yaya'):
                    color = (0, 0, 255)
                else:
                    color = (255, 0, 0)
                cv2.rectangle(image, (int(o['x0']), int(o['y0'])), (int(o['x1']), int(o['y1'])), color, 2)
            except KeyError:
                print(f"error url : {url}\nobj_order: {order}")
                countForKeyError = countForKeyError + 1
                color = (0, 255, 0)
                cv2.rectangle(image, (int(o['x0']), int(o['y0'])), (int(o['x1']), int(o['y1'])), color, 2)
                cv2.imshow(f"error{countForKeyError}", image)
                cv2.waitKey(0)
        print(url)
cv2.destroyAllWindows()
print(count)
print(d)
