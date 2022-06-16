#!/usr/bin/env python3
#modified from f-ponce magnotether_wind.py
#by Ysabel Giraldo, Tim Warren 1.23.20
#modified 11.19.21 to test writing to file
#modified 11.23.21 to add rough code for subscribing to LED node
#modified 5.27.22 for new addition with the LED_Rand Script and added functionality
#modified 5.30.22 Tim Warren Queue 
# convention is led position of 150 is dark
# 149 is stop


# THIS WORKS FOR SHOWCASING THE RAW IMAGE THAT IS UPDATING!!
## NEED TO GET THIS TO WORK MAYBE TEST WITH queues?


# FLY ALIGNMENT CONTROL NODE!!!
# Developed by Logan Rower
## Referenced work by the Giraldo and Dickinson Lab


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
#this is message type that you will subscribe to
#from basic_led_strip_ros.msg import StripLEDInfo
from basic_led_strip_ros.msg import LEDinfo
import os
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import queue
import time 
from std_msgs.msg import Float64

from magnotether.msg import MsgAngleData

from find_fly_angle import find_fly_angle 


import math


class ImageConverter:  

    def __init__(self):

        rospy.init_node('image_converter', anonymous=True)
        self.bridge = CvBridge()
        rospy.on_shutdown(self.clean_up)

        self.image_sub = rospy.Subscriber("/pylon_camera_node/image_raw",Image,self.callback)
        rospy.logwarn('subscribed')

        # self.current_led_position=-1
        # rospy.Subscriber('/led_position', LEDinfo, self.led_callback)
        

        # self.rotated_image_pub = rospy.Publisher('/rotated_image', Image, queue_size=10)
        # self.contour_image_pub = rospy.Publisher('/contour_image', Image, queue_size=10)

        self.queue = queue.Queue()

        # self.threshold = 50
        # self.mask_scale = 0.9
        self.frame_count = 0
        # self.image_save_duration=60
        # self.angle_data = None

        # ##tw added
        # ###You need to change self.data_path to a valid path for your filesystem
        # ###e.g. '/home/giraldolab/data/'
        # rospy.logwarn(self.params['data_base_name'])

        # self.data_path=self.params['data_base_name'] +'/'
        
        # self.image_path=self.params['image_data_base_name'] + '/'
        
        # if os.path.isdir(self.data_path) is False:
        #     os.makedirs(self.data_path)
        # if os.path.isdir(self.image_path) is False:
        #     os.makedirs(self.image_path)


        # self.file_name=self.data_path +time.strftime("%Y%m%d%H%M%S") + '.txt'
        # self.image_file_name_base=time.strftime("%Y%m%d%H%M%S") + '_'
        
        # self.file_handle = open(self.file_name,mode='w+')
    

        #cv2.namedWindow('raw image', cv2.WINDOW_NORMAL)
        #cv2.namedWindow('contour image', cv2.WINDOW_NORMAL)
        #cv2.namedWindow('rotated image', cv2.WINDOW_NORMAL)

        # moveable window

        
        #cv2.moveWindow('raw image', 100, 100)
        #cv2.moveWindow('contour image', 110, 110)
        #cv2.moveWindow('rotated image', 120, 120)cd ~
        # resize the windows

        #cv2.resizeWindow('raw image',50,50)
        #cv2.resizeWindow('contour image',50,50)
        #cv2.resizeWindow('rotated image',50,50)


        # IN THEORY FOR CIRCLE:
        ## Need to essentially save the information from the first test image
        ## And then we need to have all of that information essentially saved to
        ## the iniitalized variables refereced in the init..
        ## this will allow these variables to be referenced later on with their new values after the first initialized procedure..
        

        # STEP 1: Coordinates for the 3 outer selections were determined.
        # Created an empty list of outer coordinates of the circle 
        ## values will be appended to this in the function referenced in analyzing the first image
        self.outer_coords = []

        # Created inital circle parameters for the coordinates that will be drawn on the image
        ## Created an arbitrary radius size that seems to function well for the user to be able to see
        self.outer_radius = 20
        ## Created a thickness that will be standardized for all circles
        self.thickness = 2
        ## Outer Circle Color
        self.outer_color = (255,0,0)

        # STEP 2: The outer coordinates were then utilized with the circle functions to compute the center coordinates of the circle
        
        # Created an empty list for the center coordinates
        ## These will be filled in based on the readings from the first image
        self.ctr_crd = []
        # The radius of the circle...
        ## This radius will be changed based on what was established as the center...
        self.main_rad = 0
        self.main_color = (255,0,0)
        # how thick the circles will be 
        self.thickness = 2
        self.count = 0


        
    def clean_up(self):
        cv2.destroyAllWindows()

    def callback(self,data): 
        
        self.queue.put(data)
        
        #rospy.logwarn('printing queue_size')
        #rospy.logwarn(np.shape(tst))

################### CIRCLE FUNCTIONS ########################
    # STEP 1: GET OUTER COORDS
    def coord(self,event, x, y, flags, params):
        """

        This function will check for when there is a left mouse click and save the coordinates

        

        x and y are the coordinates of the event

        flags pertains to any flags sent by OpenCV

        params are the additional parameters that might be supplied by OpenCV

        points specifies the number of points the user wants to create

        """
        #cv_image = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
        if event == cv2.EVENT_LBUTTONDOWN:
            # when this event occurs.. it is a left mouse click so this signifies point
            print("Creating new Point...")
            #coords.append([x,y])
            #count+=1
            coord = [x,y]
            radius = 20
            color = (255,0,0)
            thickness = 2
            cv2.circle(self.cv_image, coord, self.outer_radius, self.outer_color, self.thickness)
            # Now using the cv2. circle method
            #image = cv2.circle(image, center_coordinates, radius, color, thickness)
            self.outer_coords.append(coord)
            print(self.outer_coords)
            cv2.imshow('image window', self.cv_image)
            # Show the new image with the circle

    # STEP 2: CALCULATE THE CENTER AND RADIUS
    def find_coords(self):
        """
        The circle coordinates will be used to compute the radius and the center of the circle

        These were set to be equal to x1, y1, x2, y2, x3 and y3
        """
        #x1, y1, x2, y2, x3, y3
        findcirc_ls = [0,0,0,0,0,0]
        count = 0
        for sub_list in np.arange(len(self.outer_coords)):
        # selects the sub list
            for inter_idx in np.arange(2):
                # selects the idx within the list and puts it into the index of the findcirc_ls
                findcirc_ls[count]=self.outer_coords[sub_list][inter_idx]
                count+=1
        return findcirc_ls

    # Calculating the Equation for the Circle with the Points..
    # First assume three points....
    # IF MORE THAN THREE POINTS ONLY TAKE FIRST 3...
    def midpoint(self):
        mid1 = [((self.x1+self.x2)/2),((self.y1+self.y2)/2)]
        mid2 = [((self.x1+self.x3)/2),((self.y1+self.y3)/2)]
        midpoints = [mid1, mid2]
        return midpoints
    def slope(self):
        m1 = (self.y2-self.y1)/(self.x2-self.x1)
        m2 = (self.y3-self.y1)/(self.x3-self.x1)
        slopes = [m1,m2]
        return slopes
    def C(self):
        C_value = ((self.midpoint()[0][0]))+ (self.slope()[0])*self.midpoint()[0][1]
        return C_value
    def K(self):
        K_value = ((self.midpoint()[1][0]))+(self.slope()[1])*self.midpoint()[1][1]
        return K_value
    # def perp_slope():
    #   perp_m1 = -1* (1/(slope()[0]))
    #   perp_m2 = -1* (1/(slope()[1]))
    #   perpslopes = [perp_m1,perp_m2]
    #   return perpslopes




################################################
    def run(self): 

        start_time=time.time()
        image_save_count=0
        while not rospy.is_shutdown():

            # Pull all new data from queue
            new_image_list = []
           
            # if self.current_led_position==149:
            #     break
            while True:
                try:
                    ros_image = self.queue.get_nowait()
                    #print("ROS MeSSAGE",ros_image)
                    new_image_list.append(ros_image)
                    #rospy.logwarn(len(new_image_list))
                    if len(new_image_list)>5:
                        #rospy.logwarn('dropping frames')
                        new_image_list=new_image_list[-2:]

                except queue.Empty:
                    #print('error getting image')    
                    break
            #count = 0
            for image_ct,ros_image in enumerate(new_image_list):
                ## Added count +1 in order to make it so that it is only the first image that this occurs to...
                self.count+=1
                # When the first image....
                if self.count == 1:

                    print("Find the Outer Coordinates")
                    print(type(ros_image))
                    self.cv_image = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
                    cv2.imshow('image window', self.cv_image)
                    cv2.setMouseCallback('image window',self.coord)
                    #print(self.outer_coords)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    self.x1, self.y1, self.x2, self.y2, self.x3, self.y3 = self.find_coords()

                    A = np.array([[1,-self.slope()[0]], [1, -self.slope()[1]]])
                    b = np.array([self.C(), self.K()])
                    # Now We solve for Z which is [x, y]
                    z = np.linalg.solve(A,b)
                    zlst = []
                    for each in z:
                        zlst.append(int(str(each).split('.')[0]))
                    zlst[1]=zlst[1]*-1
                    print(zlst)

                    #  CENTER COORDS
                    self.ctr_crd  = zlst
                    # Find the Radius
                    ### Using the Distance Equation
                    r = np.sqrt(((self.x1-self.ctr_crd[0])**2)+((self.y1-self.ctr_crd[1])**2))
                    self.main_rad = int(r)
                    print(f"Radius (px): {self.main_rad}")

                else:
                    try:
                        self.cv_image = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")

                    except CvBridgeError as e:
                        rospy.logwarn('error')
                        print(e)

                self.frame_count += 1
                cv_image_in = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2GRAY)  
                #rospy.logwarn(np.shape(cv_image_in))
                # red_image=cv_image_in[:,360:1560]
                
                # angle_rad, angle_data = find_fly_angle(red_image, self.threshold, self.mask_scale)

                # angle_deg = np.rad2deg(angle_rad)
                # #rospy.logwarn(str(angle_deg))
                # angle_data['raw_image'] = red_image

                # rotated_ros_image = self.bridge.cv2_to_imgmsg(angle_data['rotated_image'])
                # rotated_ros_image.header = ros_image.header
                
                # contour_ros_image = self.bridge.cv2_to_imgmsg(angle_data['contour_image'])
                # contour_ros_image.header = ros_image.header
                
                # msg_angle_data = MsgAngleData()
                # msg_angle_data.header.stamp = ros_image.header.stamp
                # msg_angle_data.frame = self.frame_count
                # msg_angle_data.angle = angle_deg
                # msg_angle_data.rotated_image = rotated_ros_image
                # self.angle_pub.publish(msg_angle_data) 

                
                #self.rotated_image_pub.publish(rotated_ros_image)
                #self.contour_image_pub.publish(contour_ros_image)

                # self.angle_data = angle_data 
               
                # cr_time=time.time()
            
                # try:
                #     #rospy.logwarn(self.led_state.led_position)
                #     self.current_led_position=self.led_state.led_position
                # except:
                #     self.current_led_position=-1


            #rospy.logwarn(angle_deg)
            
            #ex
             #   self.write_data(cr_time,angle_deg)

            
                # if self.angle_data is not None :
                #     self.write_data_with_led(cr_time,angle_deg) 
                    
                    # if cr_time-start_time<self.image_save_duration:
                        # image_save_count=image_save_count+1
                        # image_add_str=str(image_save_count).rjust(4, '0')

                        # image_file_name=self.image_file_name_base + image_add_str + '.png'
                        # #rospy.logwarn(image_file_name)
                        # cv2.imwrite(self.image_path+image_file_name,self.angle_data['raw_image'])
                        
                if image_ct==0:

                    # Reference the function that will essentially plot the points... 
                    coord = self.ctr_crd
                    radius = self.main_rad
                    color = self.main_color
                    thickness = self.thickness

                    # Draw concentric Circles of decreasing radius..
                    ## 5 concentric circles so divide radius by /2 5 times
                    circle_array = np.arange(1,6)
                    for circle in circle_array:
                        ## 
                        radius = radius //2
                        print(radius)
                        cv2.circle(self.cv_image, self.ctr_crd, radius, self.main_color, self.thickness)
                    cv2.imshow('raw image',self.cv_image)
                        #cv2.imshow('rotated image', self.angle_data['rotated_image'])
                    rospy.sleep(0.001)
                    cv2.waitKey(1)
            #rospy.logwarn('closing file handle')
        # self.file_handle.close()
    
    # def write_data(self,time,angle_deg):
    #     self.file_handle.write('%f %f NaN\n'%(time,angle_deg))
    #     self.file_handle.flush()
    # def write_data_with_led(self,time,angle_deg):
    #     self.file_handle.write('%f %f %d\n'%(time,angle_deg, self.current_led_position))
    #     self.file_handle.flush()
    # def led_callback(self,led_info):
    #     self.led_state=led_info
    #     rospy.logwarn('getting led state')


# def main(params):
#     ic = ImageConverter(params)
#     ic.run()


# ---------------------------------------------------------------------------------------
if __name__ == '__main__': 
    ic = ImageConverter()
    ic.run()
