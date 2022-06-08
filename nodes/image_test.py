import cv2
import numpy as np
#from cv_bridge import CvBridge, CvBridgeError
from datetime import datetime
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib

# Used Geeks for Geeks Python functions for finding the circle equation


circle_coords = []
# function for coordinates
def coord(event, x, y, flags, params):
	"""
	This function will check for when there is a left mouse click and save the coordinates

	

	x and y are the coordinates of the event

	flags pertains to any flags sent by OpenCV

	params are the additional parameters that might be supplied by OpenCV

	points specifies the number of points the user wants to create

	"""
	if event == cv2.EVENT_LBUTTONDOWN:
		# when this event occurs.. it is a left mouse click so this signifies point
		print("Creating new Point...")
		#coords.append([x,y])
		#count+=1
		coord = [x,y]
		# Now using the cv2. circle method
		#image = cv2.circle(image, center_coordinates, radius, color, thickness)
		circle_coords.append(coord)
		print(circle_coords)
	
	# Added the following since it seems like I need all functionality to occur within the buttons
	## So this will take the circle coords list and 
	#elif event == cv2.EVENT_RBUTTONDOWN:

def find_coords(circle_coords):
	"""
	The circle coordinates will be used to compute the radius and the center of the circle

	These were set to be equal to x1, y1, x2, y2, x3 and y3
	"""
	#x1, y1, x2, y2, x3, y3
	findcirc_ls = [0,0,0,0,0,0]
	count
	for sub_list in np.arange(len(circle_coords)):
		# selects the sub list
		for inter_idx in np.arange(2):
			# selects the idx within the list and puts it into the index of the findcirc_ls
			findcirc_ls[inter_idx*sub_list]=circle_coords[sub_list][inter_idx]
			count+=1
	return findcirc_ls


#This was done by using the first three points, and then running it through a 
#These coordinates will then be used to draw a circle of X thickness at the location of where there was a click
# image display and actual execution
# if __name__=="__main__":

# read the image from the directory
img = cv2.imread("Example_image.png", cv2.IMREAD_UNCHANGED)

# display the image    
cv2.imshow('example image', img)

# set the mouse handler for the image
# called the three_circles function in order to provide a means of communciation for the mouse events
## and what should occur on those events

## NEED TO FIGURE OUT HOW TO GET THISMOUSE CALL BACK TO HALT AND ALLOW OTHER PROCESSES TO OCCUR....
cv2.setMouseCallback('example image', coord)
	
print(circle_coords)
# coord = cv2.setMouseCallback('example image', coord)
# wait for a key to be pressed to then close the image
cv2.waitKey(0)

# after waitkey is pressed then all the images will be closed

cv2.destroyAllWindows()




