#!/usr/bin/env python3
# Node to test functionality of viewing an image within ROS
## By Logan Rower
## Referenced Dickison Lab

# Will be utilizing the image data recived from the pylon camera ros node
from pickle import NONE
import rospy
import sys
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import Queue
#import multiprocessing as mp
class FlyAlign:  
    def __init__(self):
        # started the node...
        rospy.init_node('fly_align', anonymous=True)
        self.bridge = CvBridge()

        # created the subscriber object
        self.image_sub = rospy.Subscriber("/pylon_camera_node/image_raw",Image, self.align)

        # Created the Queue where the image messages would be stored
        self.que_img_msg = Queue.Queue()

    def img_callback(self, msg):
        """
        This callback function is referenced by the subscriber
        The subscriber inputs the msg (in this case Image) into this function
        This function will put the image message into the queue that was set up
        """
        # Add the image message into the queue
        self.que_img_msg.put(msg)
    
    def display(self, img):
        print("New WINDOW")
        cv2.imshow("Window", img)
        cv2.waitKey(1)
    # def align(self,Image):
    #     try:
    #         print("CONVERT TO ")
    #         self.img = self.bridge.imgmsg_to_cv2(Image,"bgr8")
    #     except CvBridgeError as e:
    #         rospy.logerr(e)
    #         return
    #     self.display(self.img)

    def run_alignment(self):
        """
        This function will ensure that the alignment program will run
        with the image continuously updating until the script is killed
        """
        while not rospy.is_shutdown():
            # Initially set the image message to be none
            img_msg = NONE
            # while loop will check to see if there is anything in the queue
            ## the loop will continue to run as long as there are image messages within the queue
            while self.que_img_msg.qsize()>0:
                # within the while loop we know that there are image messages
                # Use get() to get the first message in
                img_msg = self.que_img_msg.get()
            if img_msg == NONE:
                continue
            
            # Now process the image through the alignment..
            try:
               cv_img = self.cv_bridge.imgmsg_to_cv2(img_msg, desired_encoding="passthrough")
            except CvBridgeError as e:
                rospy.logwarn(str(e))
            
            self.display(self, cv_img)
        #print("hellow")
    # def run(self):
    #     #self.cv_image = self.bridge.imgmsg_to_cv2(image, "bgr8")
    #     cv2.waitKey(1)
if __name__=='main':
    flyalignment = FlyAlign()
    try: 
        flyalignment.run_alignment()
    except rospy.ROSInterruptException:
        cv2.destroyAllWindows()