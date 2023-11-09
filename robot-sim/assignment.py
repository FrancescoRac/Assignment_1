from __future__ import print_function

import time
from sr.robot import *

from math import pi, sin, cos, degrees, hypot, atan2


R = Robot()

a_th = 3.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""
d_arena = 0.7 # Threshold for the control of the linear distance with the arena


def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_token(v):
    """
    Function to find the closest token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist=500
    print("Marker already seen: " + str(v))
    for token in R.see():
    	code = token.info.code
        if token.dist < dist and not (code in v): # conditions to verify if there are any token in the arena.
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1, -1
    else:
   	return code, dist, rot_y
    	

def seeCenterArena():

	'''

	This function return the distance and the angle between the robot and the center of the arena

	Returns:
		dist_arena (float): distance of the center of the arena
		rot_arena (float): angle between the robot and the arena 
	
	'''
	R.see()
        with R.lock:
            x, y = R.location
            heading = R.heading

        rel_x, rel_y = (-x, -y)  

        dist_arena = hypot(rel_x, rel_y)
        rot_arena = degrees(atan2(rel_y, rel_x) - heading)
        
        return dist_arena, rot_arena
        
        
   	
v = [] # this vector contain the code of the marker grabbed and released in the center of the arena
dist_arena, rot_arena = seeCenterArena() # look for the center of arena.


while 1:

    dist_arena = dist_arena + 0.5;
    
    
    markers = R.see() 
    
    while not markers:
    	dist_arena, rot_arena = seeCenterArena() # look for the center of the arena
	turn(-25, 0.1)
	markers = R.see() # look for markers
	for m in markers:
		if m.info.code in v: # markers already seen will not be taken in consideration
			markers = []
    	if abs(rot_arena) <= a_th:
		exit()
		
    code, dist, rot_y = find_token(v)  # we look for markers. 	
	
    if dist < d_th:
    
    	print("Found it!")
    	
        grabbed = R.grab() # if we are close to the token, we grab it.
        
        v.append(code) # put into the vector v the code of the marker grabbed.
        
        print("Gotcha!")
        
        while (d_arena < dist_arena or 0.4 < abs(rot_arena)) and grabbed is True:
        	
        	dist_arena, rot_arena = seeCenterArena() # look for the center of the arena
	    	
	    	if rot_arena < -a_th:
			
			turn(-10, 0.1) # turn left if the robot can't see the center of arena
        	
		elif rot_arena > a_th:
			
			turn(+10, 0.1) # turn right if the robot can't see the center of arena
			
		elif -a_th<= rot_arena <= a_th: 
			
			drive(50, 0.2) # if the robot is well aligned with the token, we go forward
			
		if d_arena > dist_arena:
		
			R.release() # release the marker when the robot is in the center of arena
			grabbed = False
						
			drive(-50, 1) # go back 
			
			turn(-35, 1) # turn
			    
    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
        print("Ah, here we are!.")
        drive(50, 0.2)
        
    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-10, 0.1)
    
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+10, 0.1)
        
