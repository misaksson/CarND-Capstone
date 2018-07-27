from styx_msgs.msg import TrafficLight
import cv2
import time
import datetime
import random
import img_proc
from classifier.yolo import YOLO
import rospy
import yaml
import os
import numpy as np

class TLClassifier(object):
    yolo = None
    def __init__(self):
        traffic_light_config = rospy.get_param("/traffic_light_config")
        self.config = yaml.load(traffic_light_config)
        self.yolo = YOLO(self.config['classification']['model'], self.config['classification']['anchors'], self.config['classification']['classes'])
        pass

    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:rew
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        secs = int(time.time() * 10)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB) 
        scores, classes, img = self.yolo.detect_image(image)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
        state = self.getState(scores, classes)
        '''
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2

        cv2.putText(img, 'state: {}'.format(state), 
            (100, 30), 
            font, 
            fontScale,
            fontColor,
            lineType)
        tempClass = ""
        for index in classes:
            tempClass = tempClass+","+str(index)
        cv2.putText(img, tempClass, 
            (100, 70), 
            font, 
            fontScale,
            fontColor,
            lineType)
        tempScore = ""
        for index in scores:
            tempScore = tempScore+","+str(index)
        cv2.putText(img, tempScore, 
            (100, 110), 
            font, 
            fontScale,
            fontColor,
            lineType)
        secs = int(time.time() * 10)
        cv2.imwrite('./sim_imgs/img_%d.jpg' % secs, img)'''
        print(state)
        if state == 0:
            return TrafficLight.RED
        elif state == 1:
            return TrafficLight.GREEN
        elif state == 2:
            return TrafficLight.YELLOW
        elif state == 3:
            return TrafficLight.UNKNOWN
    

    def getState(self, scores, classes):
        final_state = 3
        if len(classes) > 0:
            final_state = np.max(classes)

        return final_state
