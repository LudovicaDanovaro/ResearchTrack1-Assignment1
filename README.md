# RESEARCH TRACK : ASSIGNMENT1
**Student: Ludovica Danovaro**

## Python Robotics Simulator

### Running the code
It is a simple, portable robot simulator developed by Student Robotics. The simulator requires a Python 2.7 installation, the pygame library, PyPyBox2D, and PyYAML. 

Once the dependencies are installed, simply run the ```test.py``` script to test out the simulator :
```python2 run.py Assignment.py``` where the file ```Assignment.py``` contains the code.

### Goal of the assignment
The goal of the assignment is to make the robot move around the arena and do two consecutive actions:
1. Search and find the closest __silver box__ in the environment
2. Put this silver box close to the closest __golden box__
In the end you should have silver and golden boxes distributes in pairs as:
![ArenaFinale](https://user-images.githubusercontent.com/80389978/199467322-e596464c-1a5f-4570-b78a-c7a04c18fd3f.png)


## The project :warning: :construction:

### Arena
The arena has a given shape, with golden tokens and silver tokens represented as follows:
![ArenaIniziale](https://user-images.githubusercontent.com/80389978/199467187-ee8bbaad-8f26-41fa-bb4d-effe2ab814b1.png)

### Robot

The robot is the following:

![robot](https://user-images.githubusercontent.com/80389978/199465909-7d509c5a-311b-45fb-a21a-91ef15154cb9.png)

It has distance sensors on all sides, so it can detect a box from -180° to 180°; the reference of 0° is the front direction and the angle increases by moving in clockwise direction taking as reference the 0° position and decreases in the other rotation direction.

### Motors

The simulated robot has two motors configured for skid steering, connected to a two-output Motor Board. The left motor is connected to output ```0``` and the right motor to output ```1``` .

The Motor Board API is identical to that of the SR API, except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

``` py
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```
The methods ```drive(speed,time)``` and ```turn(speed,time)``` are used to activate the motors: the first one makes the robot go straight, for a certain time ```time``` at a certain speed ```speed```; the second makes it turn, always for a certain time ```time``` and at a certain speed ```speed```.
If ```speed``` is > 0 it makes the robot turn clockwise and if ```speed``` is < 0 it makes the robot turn on counterclockwise.

### Grab Function
The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, it is used the method ```R.grab()```. It returns a boolean value: ```True``` if a token was succesfully picked up, or ```False``` otherwise.  If the robot is already holding a token, it will throw an ```AlreadyHoldingSomethingException```.

``` py
print("Found it!")
if R.grab(): # we grab the silver token
    print("Gotcha!")
```

### Release Function
The robot can drop a token that has already grabbed using the method ```R.release()```. When the robot releases the token then it goes back and turns to fin a new silver box.

``` py
elif dist <  1.3*d_th : # if we are close to the token, we try grab it.
            print("Found it!")
            R.release() # we release the silver token close to the golden box
            drive(-30,2)
            turn(40,1)
```

### Token

Tokens are of two types, as it can be seen in the arena picture. Each of them is a ```Marker``` and is characterised by many properties which describe all its characteristics and position in the space. 
Each ```Marker``` object has the following attributes:
  * ```info```: a ```MarkerInfo``` object describing the marker itself. Has the following attributes: 
    * ```code```: the numeric code of the marker.
    * ```marker_type```: the type of object the marker is attached to (either ```MARKER_TOKEN_GOLD```, ```MARKER_TOKEN_SILVER``` or ```MARKER_ARENA```).
     * ```offset```: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
     * ```size```: the size that the marker would be in the real game, for compatibility with the SR API.
  * ```centre```: the location of the marker in polar coordinates, as a ```PolarCoord``` object. Has the following attributes: 
    * ```length```: the distance from the centre of the robot to the object (in metres).
    * ```rot_y```: rotation about the Y axis in degrees.
  * ```dist```: an alias for ```centre.length```
  * ```res```: the value of the ```res``` parameter of ```R.see```, for compatibility with the SR API.
  * ```rot_y```: an alias for ```centre.rot_y```
  * ```timestamp```: the time at which the marker was seen (when ```R.see``` was called).

In the program I mainly used:
* ```dist```: an alias for ```centre.length```
* ```rot_y```: an alias for ```centre.rot_y```
* ```info```: a ```MarkerInfo``` object describing the marker itself. Has the following attributes: 
* ```marker_type```: the type of object the marker is attached to (either ```MARKER_TOKEN_GOLD```, ```MARKER_TOKEN_SILVER```)
       
  
![token](https://user-images.githubusercontent.com/80389978/200780089-7d1bba7b-2242-4b32-8aec-0ed687392568.png)

 
![token_silver](https://user-images.githubusercontent.com/80389978/200780182-4c113300-fa7f-4c07-9c3b-0cf4d41a4670.png)

When the silver token is grabbed, it becames: ![token_silver_grabbed](https://user-images.githubusercontent.com/80389978/200780633-260c24c1-599c-4c5b-a80a-9080e1a32cd0.png)

        
### Code
Thanks to the flowchart, the general structure of the code can be described:
##### Flowchart
![Flowchart](https://user-images.githubusercontent.com/80389978/200868443-ac2e8e2e-2edc-4e52-9965-9eb3a9821b8a.png)



The program starts checking if each golden token is close to a silver token. 

``` py
while (len(golden_list) < 6 ):
```

The second step is the check of the boolean variable ```silver```: at the beginning it is set to True, so we will look for a silver token. 

``` py
if silver == True :
```

Then there is the check of the possible presence of a silver token by ```dist,rot_y,silver_code = find_silver_token()``` which looks for a silver token in a pre-determined range of view.

``` py
def find_silver_token():
    """
    Function to find the closest silver token in the range ov view

    Returns:
	dist (float): distance of the closest silver token in the range of view (-1 if no silver token is detected)
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
```

This function checks that the selected silver token is not already in the ```silver_list``` list, which would mean that the silver token has already been brought close to a golden token. If not, the robot can drive to this token and go grabbing it. 
Now the program has to take a decision based on the return of the ```find_silver_token()``` function, controlling the variable```dist``` and the variable ``` rot_y```  :

* if ``` dist == 1```, no token is detected so the robot turns to look for another silver token :
	
	```  py
	    if dist==-1:  
            print("I don't see any token!!")
            turn(+10, 1)	
	``` 
	
	
* if ``` dist < d_th``` , where ``` d_th``` is the distance threshold, the robot is close to the silver token and try to grab it using the ``` R.grab()```  method. The second step is to add the code of the silver marker to the ``` silver_list``` , that contains all the tokens that has been taken. The third step is to change the boolean variable ``` silver```  in order to look for a golden token in the next step :
	
	```  py
	elif dist < d_th: 
            print("Found it!")
            if R.grab(): # we grab the silver token
                print("Gotcha!")
                silver_list.extend([silver_code]) 
                print("Silver list:", silver_list)
                silver = not silver 
	``` 
	
* if ``` -a_th<= rot_y <= a_th``` , the robot is well aligned with the token, so it can go forward :
	
	```  py
	elif -a_th<= rot_y <= a_th: 
            print("Ah, that'll do.")
            drive(70, 0.5)
	``` 
	
* if the robot is not well aligned with the token, we move it on the left or on the right :
	
	``` py
	elif rot_y < -a_th: 
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)
	``` 
	
* if the robot is too far from the token :
	
	``` py
	else:
            print("Aww, I'm not close enough.")
	``` 




In the second part, when the boolean variable ``` silver```  is set to ``` False``` , the program checks a possible presence of a golden token by ```dist,rot_y,golden_code = find_golden_token()```  which looks for a golden token in a pre-determined range of view.


``` py
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
	
```

This function checks that the selected golden token is not already in the ```golden_list``` list, which would mean that a silver token has already been brought close to it. If not, the robot can drive to this token and go releasing the token. Now the program has to take a decision based on the return of the ```find_golden_token()``` function, controlling the variable ```dist``` and the variable ```rot_y``` :


* if ``` dist == 1```, no token is detected so the robot turns to look for another golden token :
	
	```  py
	    if dist==-1:  
            print("I don't see any token!!")
            turn(+10, 1)	
	``` 

* if ``` dist < 1.3*d_th``` , where ``` d_th``` is the distance threshold, the robot is close to the golden token and try to release the silver token using the ``` R.release()```  method. The second step is to add the code of the golden marker to the ``` golden_list``` , that contains all the tokens to which we have already brought a silver marker. The third step is to change the boolean variable ``` silver```  in order to look for a silver token in the next step :

	``` py
	elif dist <  1.3*d_th : 
            print("Found it!")
            golden_list.extend([golden_code]) 
            print("Golden list: ", golden_list)
            R.release() 
            drive(-30,2)
            turn(30,1)
            silver = not silver 
	```
	
* if ``` -a_th<= rot_y <= a_th``` , the robot is well aligned with the token, so it can go forward :
	
	```  py
	elif -a_th<= rot_y <= a_th: 
            print("Ah, that'll do.")
            drive(70, 0.5)
	``` 
	
* if the robot is not well aligned with the token, we move it on the left or on the right :
	
	``` py
	elif rot_y < -a_th: 
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)
	``` 
	
* if the robot is too far from the token :
	
	``` py
	else:
            print("Aww, I'm not close enough.")
	``` 

### Final Arena
In the end I have silver and golden boxes distributes in pairs as:
![ArenaFinale](https://user-images.githubusercontent.com/80389978/199467322-e596464c-1a5f-4570-b78a-c7a04c18fd3f.png)

### Video Demonstration

https://user-images.githubusercontent.com/80389978/201900773-14e13022-5552-4235-baf3-689244dee0c3.mp4


### Future Improvements

Another possibility to do this exercise is to make a function Grabbing() and a function Releasing() to avoid having a single block of code. I didn't do it because it seems to me that was much clear see what the program does consecutively. But the only differences stay in :

* calling the function Grabbing() in the first case ( silver == true ) when : 
	
	```  py
	elif dist < d_th: 
	``` 
	
	where the function Grabbing() is:
	
	``` py
	def Grabbing():
	    print("Found it!")
            if R.grab(): # we grab the silver token
                print("Gotcha!")
                silver_list.extend([silver_code]) 
                print("Silver list:", silver_list)
                silver = not silver 
	```

* calling the function Releasing() in the second case ( silver == false ) when :
	``` py
	elif dist <  1.3*d_th : 
	```
	
	where the function Releasing() is :
	
	``` py
	def Releasing():
	    print("Found it!")
            golden_list.extend([golden_code]) 
            print("Golden list: ", golden_list)
            R.release() 
            drive(-30,2)
            turn(30,1)
            silver = not silver 
	```
	
		

A possible improvement of this exercise could be that the robot goes grabbing the closest silver marker and releases it to the closest golden marker; moreover, since the robot has many distance sensors, it could be also useful to detect a possible path to be followed so that the robot doesn't collide with any token while it's moving.
