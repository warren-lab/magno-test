#!/usr/bin/env python3
#modified from f-ponce magnotether_wind.py
#by Ysabel Giraldo, Tim Warren 1.23.20
#modified 11.19.21 to test writing to file
#modified 11.23.21 to add rough code for subscribing to LED node

# NEED TO ADD:
### IF LED POSITION IS = to -1 then Make it NaN

# convention is led position of 150 is dark
# 149 is stop


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



def set_init_params():


    rospy.logwarn('current flyname is')
    
    
    rospy.logwarn(rospy.get_param('flyname','flydef'))


    params={
        #these initial parameters need to be set differently for different experiments
        #'gain_x': -.5,
       
        'flyname':rospy.get_param('flyname','flydef'),  
        'exec_file_name':os.path.abspath(__file__),
        #'initpos':INITPOS
    }
    #rospy.logwarn(params['flyname'])
    params['data_base_name']='/home/flyranch/data/' +time.strftime("%Y%m%d") +'/'+params['flyname']
    params['image_data_base_name']='/home/flyranch/image_data/' +time.strftime("%Y%m%d") +'/'+params['flyname']
    time.sleep(.1)

    return(params)
    



class ImageConverter:  

    def __init__(self,input):

        self.params=input


        rospy.init_node('image_converter', anonymous=True)
        self.bridge = CvBridge()
        rospy.on_shutdown(self.clean_up)

        self.image_sub = rospy.Subscriber("/pylon_camera_node/image_raw",Image,self.callback)
        self.angle_pub = rospy.Publisher('/angle_data', MsgAngleData, queue_size=10)
        rospy.logwarn('subscribed')

        self.current_led_position=-1
        rospy.Subscriber('/led_position', LEDinfo, self.led_callback)
        

        self.rotated_image_pub = rospy.Publisher('/rotated_image', Image, queue_size=10)
        self.contour_image_pub = rospy.Publisher('/contour_image', Image, queue_size=10)

        self.queue = queue.Queue()

        self.threshold = 50
        self.mask_scale = 0.9
        self.frame_count = 0
        self.image_save_duration=60
        self.angle_data = None

        ##tw added
        ###You need to change self.data_path to a valid path for your filesystem
        ###e.g. '/home/giraldolab/data/'
        rospy.logwarn(self.params['data_base_name'])

        self.data_path=self.params['data_base_name'] +'/'
        
        self.image_path=self.params['image_data_base_name'] + '/'
        
        if os.path.isdir(self.data_path) is False:
            os.makedirs(self.data_path)
        if os.path.isdir(self.image_path) is False:
            os.makedirs(self.image_path)


        self.file_name=self.data_path +time.strftime("%Y%m%d%H%M%S") + '.txt'
        self.image_file_name_base=time.strftime("%Y%m%d%H%M%S") + '_'
        
        self.file_handle = open(self.file_name,mode='w+')
    

        #cv2.namedWindow('raw image', cv2.WINDOW_NORMAL)
        cv2.namedWindow('contour image', cv2.WINDOW_NORMAL)
        #cv2.namedWindow('rotated image', cv2.WINDOW_NORMAL)

        # moveable window

        
        #cv2.moveWindow('raw image', 100, 100)
        cv2.moveWindow('contour image', 110, 110)
        #cv2.moveWindow('rotated image', 120, 120)cd ~
        # resize the windows

        #cv2.resizeWindow('raw image',50,50)
        cv2.resizeWindow('contour image',50,50)
        #cv2.resizeWindow('rotated image',50,50)
        
    def clean_up(self):
        cv2.destroyAllWindows()

    def callback(self,data): 
        
        self.queue.put(data)
        
        #rospy.logwarn('printing queue_size')
        #rospy.logwarn(np.shape(tst))

    def run(self): 

        start_time=time.time()
        image_save_count=0
        while not rospy.is_shutdown():

            # Pull all new data from queue
            new_image_list = []
           
            if self.current_led_position==149:
                break
            while True:
                


                try:
                    ros_image = self.queue.get_nowait()
                   

                    new_image_list.append(ros_image)
                    #rospy.logwarn(len(new_image_list))
                    if len(new_image_list)>5:
                        #rospy.logwarn('dropping frames')
                        new_image_list=new_image_list[-2:]

                except queue.Empty:
                    #print('error getting image')    
                    break

            for image_ct,ros_image in enumerate(new_image_list):
                try:
                    cv_image = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
                except CvBridgeError as e:
                    rospy.logwarn('error')
                    print(e)

                self.frame_count += 1
                cv_image_in = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)  
                #rospy.logwarn(np.shape(cv_image_in))
                red_image=cv_image_in[:,360:1560]
                
                angle_rad, angle_data = find_fly_angle(red_image, self.threshold, self.mask_scale)

                angle_deg = np.rad2deg(angle_rad)
                #rospy.logwarn(str(angle_deg))
                angle_data['raw_image'] = red_image

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

                
                #self.rotated_image_pub.publish(rotated_ros_image)
                #self.contour_image_pub.publish(contour_ros_image)

                self.angle_data = angle_data 
               
                cr_time=time.time()
            
                try:
                    #rospy.logwarn(self.led_state.led_position)
                    self.current_led_position=self.led_state.led_position
                except:
                    self.current_led_position=-1


            #rospy.logwarn(angle_deg)
            
            #ex
             #   self.write_data(cr_time,angle_deg)

            
                if self.angle_data is not None :
                    self.write_data_with_led(cr_time,angle_deg) 
                    
                    if cr_time-start_time<self.image_save_duration:
                        image_save_count=image_save_count+1
                        image_add_str=str(image_save_count).rjust(4, '0')

                        image_file_name=self.image_file_name_base + image_add_str + '.png'
                        #rospy.logwarn(image_file_name)
                        cv2.imwrite(self.image_path+image_file_name,self.angle_data['raw_image'])
                        
                    if image_ct==0:
                        cv2.imshow('contour image', self.angle_data['contour_image'])
                    #cv2.imshow('rotated image', self.angle_data['rotated_image'])
                        rospy.sleep(0.001)
                        cv2.waitKey(1)
        rospy.logwarn('closing file handle')
        self.file_handle.close()
    
    def write_data(self,time,angle_deg):
        self.file_handle.write('%f %f NaN\n'%(time,angle_deg))
        self.file_handle.flush()
    def write_data_with_led(self,time,angle_deg):
        self.file_handle.write('%f %f %d\n'%(time,angle_deg, self.current_led_position))
        self.file_handle.flush()
    def led_callback(self,led_info):
        self.led_state=led_info
        rospy.logwarn('getting led state')


def main(params):
    ic = ImageConverter(params)
    ic.run()


# ---------------------------------------------------------------------------------------
if __name__ == '__main__': 
    params=set_init_params()
    main(params)
