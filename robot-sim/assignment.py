from __future__ import print_function

import time
from sr.robot import *

R = Robot()

a_th = 3.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""
d_arena = 0.7


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

def find_token_color():
    """
    Function to find the closest token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist=500
    mark = R.see()
    print("mark is " + str(mark))
    for token in R.see():
        if token.dist < dist:
            dist=token.dist
	    rot_y=token.rot_y
    if len(mark) == 0:
    	turn(20,0.5)
    	return find_token_color()
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
   	
markers = R.see()
    
dist_arena, rot_arena = R.seeCenterArena() #look for the center of arena

while 1:
    
    
    
    dist, rot_y = find_token_color()  # we look for markers  
       
    if dist==-1:
        print("I don't see any token!!")
        turn(45, 0.5)
	
    elif dist < d_th: 
    	print("Found it!")
        grabbed = R.grab() # if we are close to the token, we grab it.
        for m in markers:
        	code = m.info.code
        	print(code)
        print("Gotcha!") 
        
        
        while (d_arena < dist_arena or 0.4 < abs(rot_arena)) and grabbed is True:
	    	if rot_arena < -a_th: 
			
			turn(-5, 0.5)
        	
		elif rot_arena > a_th:
			
			turn(+5, 0.5)
			
		elif -a_th<= rot_arena <= a_th: # if the robot is well aligned with the token, we go forward
			
			drive(30, 0.4)
			
		if d_arena > dist_arena:
			R.release()
			grabbed = R.release()
			drive(-50, 0.5)
			turn(-35, 1)
			box = R.see()
			if not box:
				exit()
			
			print("Box out = " + str(box))
		dist_arena, rot_arena = R.seeCenterArena()
    
    

    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
        print("Ah, here we are!.")
        drive(30, 2)
        
    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-5, 0.5)
        	
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+5, 0.5)          		
     
