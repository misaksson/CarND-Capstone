#!/bin/python

import csv
import glob
import os
import cv2


def category(c):
    return {
     "go": 1,
     "stop": 0,
     "warning": 2
    }.get(c, 3)


def create_boxes(origin, file_n, points):
    try:
        img = cv2.imread(file_n)
        size_x = img.shape[1]
        size_y = img.shape[0]
    except:
        return
    print(file_n)

    path = 'images/' + os.path.basename(origin)
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
                                (c[0], c[1]),
                                (c[2], c[3]),
                                (255, 255, 255), -1)
        else:
            f = open(path + '.txt', "a")
            f.write("%i %f %f %f %f\n" % (category, x, y, width, height))
            f.close()
    img = cv2.resize(img, (416, 416), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(path + '.jpg', img)


def read_from_csv(path, list_):
    with open(i + '/frameAnnotationsBOX.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        file_n = ''
        points = []
        for row in reader:
            if file_n != (i + "/" + row[0].replace("dayTraining", "frames")):
                create_boxes(path, file_n, points)
                file_n = (i + "/" + row[0].replace("dayTraining", "frames"))
                points = []
                print(file_n)
            else:
                points.append([int(row[2]),
                               int(row[3]),
                               int(row[4]),
                               int(row[5]),
                               category(row[1])])

os.mkdir("images")

for i in glob.glob('dayTrain/dayClip*'):
    read_from_csv(i, "")
