from __future__ import print_function

import time
from sr.robot import *

"""
The code should make the robot:
	- 1) find and grab a silver box in the environment that you haven't taken yet
	- 2) find the closest golden box which is not already coupled to another silver box
    - 3) put the silver box already taken close to this golden marker (token)
	- 4) start again from 1
"""

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

silver_list = []
golden_list = []
""" lists of the silver boxes that are already taken and golden boxes to which we have already brought a silver marker """

R = Robot()
""" instance of the class Robot"""

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

def find_silver_token():
    """
    Function to find the closest silver token in the range of view

    Returns:
	dist (float): distance of the closest silver token in the range of view(-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    silver_code (float): numeric code of the silver marker
    """
    dist=100
    for token in R.see():
            """If the silver marker can be grabbed (if its code is not in the list of the boxes already taken)"""
            if token.info.code not in silver_list:
                """ We want to take the closest silver marker"""
                if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER: 
                 dist=token.dist
                 rot_y=token.rot_y
                 silver_code= token.info.code
    if dist==100:
        return -1, -1, -1
    else:
        return dist, rot_y, silver_code

def find_golden_token():
    """
    Function to find the closest golden token in the range of view

    Returns:
	dist (float): distance of the closest golden token in the range of view(-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    golden_code (float): numeric code of the golden marker
    """
    dist=100
    for token in R.see():
        """If the silver marker can be taken to the closest golden marker 
            (if the code of the golden marker is not in the list of the boxes to which we have already brought a silver marker)"""
        if token.info.code not in golden_list: 
                """ We want to take the silver marker to the closest golden marker"""
                if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD: 
                    dist=token.dist
                    rot_y=token.rot_y
                    golden_code= token.info.code
    if dist==100:
        return -1, -1, -1
    else:
        return dist, rot_y, golden_code


while (len(golden_list) < 6 ):
    if silver == True : # if silver is True, than we look for a silver token, otherwise for a golden one
        dist, rot_y, silver_code = find_silver_token()
        
        if dist==-1: # if no token is detected, we make the robot turn 
            print("I don't see any token!!")
            turn(+10, 1)
        elif dist < d_th: # if we are close to the token, we try grab it.
            print("Found it!")
            if R.grab(): # we grab the silver token
                print("Gotcha!")
                silver_list.extend([silver_code]) # we add the code of the silver marker that has been taken to the list 
                print("Silver list:", silver_list)
                silver = not silver # we modify the value of the variable silver, so now we will look for the other type of token
        elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
            print("Ah, that'll do.")
            drive(70, 0.3)
        elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)
        else:
            print("Aww, I'm not close enough.")



    else:
        dist, rot_y, golden_code = find_golden_token()
        #print("Golden code :", golden_code)
        if dist==-1: # if no token is detected, we make the robot turn 
            print("I don't see any token!!")
            turn(+10, 1)
        elif dist <  1.3*d_th : # if we are close to the token, we try release the silver token.
            print("Found it!")
            golden_list.extend([golden_code]) # we add the code of the golden marker to the list of the golden markers to which we have already brought a silver marker
            print("Golden list: ", golden_list)
            R.release() # we release the silver token close to the golden box
            drive(-30,2)
            turn(30,1.3)
            silver = not silver # we modify the value of the variable silver, so that in the next step we will look for the other type of token             
        elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
            print("Ah, that'll do.")
            drive(70, 0.3)
        elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)
        else:
            print("Aww, I'm not close enough.") 

print("Finish!!")
        

