import yaml
import cv2
import os


def create_boxes(file_n, points):
    try:
        img = cv2.imread(file_n)
        size_x = img.shape[1]
        size_y = img.shape[0]
    except:
        return
    print(file_n)

    path = 'images/'
    i = 0
    while(os.path.exists(path + "%s.jpg" % i)):
            i += 1
    path = path + str(i)

    for c in points:
        width = float(c[2]-c[0])/size_x
        height = float(c[3]-c[1])/size_y
        x = float(c[0])/size_x + width/2
        y = float(c[1])/size_y + height/2
        category = c[4]
        if category == 3:
            img = cv2.rectangle(img,
                                (int(c[0]), int(c[1])),
                                (int(c[2]), int(c[3])),
                                (255, 255, 255), -1)
        else:
            f = open(path + '.txt', "a")
            f.write("%i %f %f %f %f\n" % (category, x, y, width, height))
            f.close()
    img = cv2.resize(img, (416, 416), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(path + '.jpg', img)


def category(c):
    return {
     "Green": 1,
     "Red": 0,
     "Yellow": 2
    }.get(c, 3)


def parse(yml):
    for entry in yml:
        print(entry)
        path = entry['path']
        points = []
        for p in entry['boxes']:
            cat = category(p['label'])
            points.append([p['x_min'], p['y_min'], p['x_max'], p['y_max'], cat])
        create_boxes(path, points)


os.mkdir("images")
with open("train.yaml", 'r') as stream:
    try:
        parse(yaml.load(stream))
    except yaml.YAMLError as exc:
        print(exc)
