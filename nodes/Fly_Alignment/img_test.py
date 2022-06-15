#!/usr/bin/env python3
# Node to test functionality of viewing an image within ROS
## By Logan Rower
## Referenced Dickison Lab

# Will be utilizing the image data recived from the pylon camera ros node
import rospy
import sys
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class FlyAlign:  
    def __init__(self):
        # started the node...
        rospy.init_node('fly_align', anonymous=True)
        self.bridge = CvBridge()

        # created the subscriber object
        self.image_sub = rospy.Subscriber("/pylon_camera_node/image_raw",Image, self.align)
    
    def display(self):
        cv2.imshow("Window", self.img)
        cv2.waitKey(1)
    def align(self,Image):
        try:
            self.img = self.bridge.imgmsg_to_cv2(Image,"bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)
            return
        self.display(self.img)

        #print("hellow")
    # def run(self):
    #     #self.cv_image = self.bridge.imgmsg_to_cv2(image, "bgr8")
    #     cv2.waitKey(1)
if __name__=='main':
    flyalignment = FlyAlign()
    try: 
        flyalignment.align()
    except rospy.ROSInterruptException:
        cv2.destroyAllWindows()