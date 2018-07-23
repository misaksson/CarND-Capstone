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

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """

        scores, classes = self.yolo.detect_image(image)
        state = self.getState(scores, classes)
        print(state)
        if state == 0:
            return TrafficLight.RED
        elif state == 1:
            return TrafficLight.GREEN
        elif state == 2:
            return TrafficLight.YELLOW
        elif state == 3:
            return TrafficLight.UNKNOWN
    
        #ROS_INFO("%s", "test");
        #ts = time.time()
        #st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
        #print('Save image as : ' + st + '.png')
        #cv2.imwrite(st + '.png',image)
        #light color prediction
        '''int_state  = img_proc.analyze_image(image)

        if int_state == 0:
            return TrafficLight.UNKNOWN
        elif int_state == 1:
            return TrafficLight.RED
        elif int_state == 2:
            return TrafficLight.YELLOW
        elif int_state == 3:
            return TrafficLight.GREEN

        return TrafficLight.UNKNOWN'''

    def getState(self, scores, classes):
        states = []
        index = 0
        final_state = 3
        for score in scores:
            score = score*100
            if score >= 75:
                states.append(classes[index])
            index += 1
        red = 0
        green = 0
        yellow = 0
        for state in states:
            if state == 0:
                red += 1
            if state == 1:
                green += 1
            if state == 2:
                yellow += 1
        if red > green and red > yellow:
            final_state = 0
        elif green > red and green > yellow:
            final_state = 1
        elif yellow > red and yellow > green:
            final_state = 2

        return final_state
