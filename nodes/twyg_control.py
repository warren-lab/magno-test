#!/usr/bin/env python
#modified from f-ponce magnotether_wind.py
#by Ysabel Giraldo, Tim Warren 1.23.20
#modified 11.19.21 to test writing to file

from __future__ import print_function

import roslib
import sys
import rospy
import cv2
from std_msgs.msg import Header
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from datetime import datetime
import os
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import Queue
import time 
from std_msgs.msg import Float64

from magnotether.msg import MsgAngleData

from find_fly_angle import find_fly_angle

class ImageConverter:  

    def __init__(self):

        rospy.init_node('image_converter', anonymous=True)
        self.bridge = CvBridge()
        rospy.on_shutdown(self.clean_up)

        self.image_sub = rospy.Subscriber("/camera_array/cam0/image_raw",Image,self.callback)
        self.angle_pub = rospy.Publisher('/angle_data', MsgAngleData, queue_size=10)

        self.rotated_image_pub = rospy.Publisher('/rotated_image', Image, queue_size=10)
        self.contour_image_pub = rospy.Publisher('/contour_image', Image, queue_size=10)

        self.queue = Queue.Queue()

        self.threshold = 50
        self.mask_scale = 0.9
        self.frame_count = 0

        self.angle_data = None

        ##tw added
        self.data_path='/home/timothy/data/'
        self.file_name=self.data_path +time.strftime("%Y%m%d") + '.txt'
        self.file_handle = open(self.file_name,mode='w')
    

        cv2.namedWindow('raw image')
        cv2.namedWindow('contour image')
        cv2.namedWindow('rotated image')

        cv2.moveWindow('raw image', 100, 100)
        cv2.moveWindow('contour image', 110, 110)
        cv2.moveWindow('rotated image', 120, 120)
	print('finish')

    def clean_up(self):
        cv2.destroyAllWindows()

    def callback(self,data): 
        self.queue.put(data)

    def run(self): 

        while not rospy.is_shutdown():

            # Pull all new data from queue
            new_image_list = []

            while True:
                try:
                    ros_image = self.queue.get_nowait()
                    new_image_list.append(ros_image)
                except Queue.Empty:
                    print('error getting image')    
		    break

            for ros_image in new_image_list:
                try:
                    cv_image = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
                except CvBridgeError as e:
                    print(e)

                self.frame_count += 1
                cv_image_gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)  
		
                angle_rad, angle_data = find_fly_angle(cv_image_gray, self.threshold, self.mask_scale)

                angle_deg = np.rad2deg(angle_rad)
                angle_data['raw_image'] = cv_image_gray

                rotated_ros_image = self.bridge.cv2_to_imgmsg(angle_data['rotated_image'])
                rotated_ros_image.header = ros_image.header
                
                contour_ros_image = self.bridge.cv2_to_imgmsg(angle_data['contour_image'])
                contour_ros_image.header = ros_image.header
                
                msg_angle_data = MsgAngleData()
                msg_angle_data.header.stamp = ros_image.header.stamp
                msg_angle_data.frame = self.frame_count
                msg_angle_data.angle = angle_deg
                msg_angle_data.rotated_image = rotated_ros_image
                self.angle_pub.publish(msg_angle_data) 

                self.rotated_image_pub.publish(rotated_ros_image)
                self.contour_image_pub.publish(contour_ros_image)

                self.angle_data = angle_data 
                #tw added
                self.write_data(angle_deg)
                
            if self.angle_data is not None:
                cv2.imshow("raw image", self.angle_data['raw_image'])
                cv2.imshow('contour image', self.angle_data['contour_image'])
                cv2.imshow('rotated image', self.angle_data['rotated_image'])
                cv2.waitKey(1)
        self.file_handle.close()
    #tw added
    def write_angle_data(self,angle_deg)
        self.file_handle.write('%f \n'%(angle_deg))
        self.file_handle.flush()



def main(args):
    ic = ImageConverter()
    ic.run()


# ---------------------------------------------------------------------------------------
if __name__ == '__main__': 
    main(sys.argv)
