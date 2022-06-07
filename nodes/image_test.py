import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib



# function for circle drawing
def three_circle(event, x, y, flags, params):
	"""
	This function will check for when there is a left mouse click and save the coordinates

	These coordinates will then be used to draw a circle of X thickness at the location of where there was a click

	x and y are the coordinates of the event

	flags pertains to any flags sent by OpenCV

	params are the additional parameters that might be supplied by OpenCV

	points specifies the number of points the user wants to create

	"""

	## this means that the for loop in the function will need to be run three times to create the three points
	#points = 3
	#count = 1
	#coords = []
	#while points <= 0:
		# while loop to loop through each event...
	#	print("Click next point")
	if event == cv2.EVENT_LBUTTONDOWN:
		# when this event occurs.. it is a left mouse click so this signifies point
		print("Creating new Point...")
		#coords.append([x,y])
		#count+=1
		coords = [x,y]

		# Now Draw the Circle
		## radius
		radius = 10
		## center
		center = coords
		## color
		color = (0,0,255)
		## Line Thickness
		thickness = -1

		# Now using the cv2. circle method
		image = cv2.circle(image, center_coordinates, radius, color, thickness)

		# 
	#print(coords)



# image display and actual execution
if __name__=="__main__":

	# read the image from the directory
	img = cv2.imread("Example_image.png", cv2.IMREAD_UNCHANGED)

	# display the image
	cv2.imshow('example image', img)

	# set the mouse handler for the image
	# called the three_circles function in order to provide a means of communciation for the mouse events
	## and what should occur on those events
	cv2.setMouseCallback('example image', three_circle)

	# wait for a key to be pressed to then close the image
	cv2.waitKey(0)

	# after waitkey is pressed then all the images will be closed

	cv2.destroyAllWindows()




