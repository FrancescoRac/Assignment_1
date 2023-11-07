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

def find_token_color(v):
    """
    Function to find the closest token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist=500
    mark = R.see()
    print("Marker already seen: " + str(v))
    for token in R.see():
        if token.dist < dist and not (token.info.code in v): # conditions to verify if there are any token in the arena.
            dist=token.dist
	    rot_y=token.rot_y
    #if len(mark) == 0:
    #	return find_token_color(v) # if the robot can'
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
   	
   	
def seeCenterArena():
	R.see()
        with R.lock:
            x, y = R.location
            heading = R.heading

        acq_time = time.time()

        rel_x, rel_y = (-x, -y)

        dist_arena = hypot(rel_x, rel_y)
        rot_arena = degrees(atan2(rel_y, rel_x) - heading)
        
        return dist_arena, rot_arena
        
        
   	
v = []
dist_arena, rot_arena = seeCenterArena() #look for the center of arena.

while 1:

    dist_arena = dist_arena + 0.5;
    
    markers = R.see()
    for m in markers:
    	v = v
    	
    dist, rot_y = find_token_color(v)  # we look for markers.
    
    if dist==-1:
        print("I don't see any token!!")
        turn(45, 0.5)
	
    elif dist < d_th:
    
    	print("Found it!")
    	
        grabbed = R.grab() # if we are close to the token, we grab it.
        
        v.append(m.info.code) # put into the vector v the code of the marker grabbed.
        
        print("Gotcha!")
        
        while (d_arena < dist_arena or 0.4 < abs(rot_arena)) and grabbed is True:
        	
        	dist_arena, rot_arena = seeCenterArena()
	    	
	    	if rot_arena < -a_th:
			
			turn(-10, 0.25) # turn left if the robot can't see the center of arena
        	
		elif rot_arena > a_th:
			
			turn(+10, 0.25) # turn right if the robot can't see the center of arena
			
		elif -a_th<= rot_arena <= a_th: # if the robot is well aligned with the token, we go forward
			
			drive(50, 0.5)
			
		if d_arena > dist_arena:
		
			grabbed = R.release() # release the marker when the robot is in the center of arena
			grabbed = False
			print("Box released" + str(grabbed) )
			
			drive(-50, 1)
			
			turn(-35, 1)
			
    
    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
        print("Ah, here we are!.")
        drive(50, 0.5)
        
    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-5, 0.25)
    
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+5, 0.25)
        
    box = R.see() # control if there are any token in the arena
			
    if not box:
	turn(15, 0.5)
	if not box:
		turn(400, 1)
		if not box:
			exit()

