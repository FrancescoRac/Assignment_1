Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.


Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/

# RT1 Assignment
The aim of this python script is to bring all the boxes, called `token`, together, in this case all the boxes will be released in the center of arena. 

### Initial state
The following image show the initial state of the robot and the token.
![InitialState](https://github.com/FrancescoRac/Assignment_1/assets/93876265/1b7a4bfd-64ce-4958-a1da-835b95fa094b)

### Goal state
Here is reported the final state of the robot with all the token in the center of the arena.
![GoalState](https://github.com/FrancescoRac/Assignment_1/assets/93876265/b24042c5-7790-4003-86cd-59f86257e511)



### How to run the code ###

To run the code you can follow this step:
* First of all you should have python2 installed, if you don't have click on this link to get it https://www.python.org/downloads/release/python-2718/;
* clone this repository in your machine;
* Execute the script typing "python2 run.py assignment.py" on the terminal.

### Flow chart

![ResearchTrack drawio](https://github.com/FrancescoRac/Assignment_1/assets/93876265/17e38215-b4ee-446b-a71b-f5a6d60a0c43)

# Functions and main

### drive(speed, seconds)

This function makes the robot move forward and backward at certain speed.

Takes as parameter the `speed` that will be assigned to the motors and `seconds` which is the time for which the robot is moving at a certain speed.

### turn(speed, seconds)

This function makes the robot turn left or right.

Takes as parameter the `speed` that will be assigned to the motors to turn the robot, positive values turn the robot to the right and negative values turn the robot to the left, and `seconds` which is the time lapse for which the robot turn.

### seeCenterArena()

This founction return the distance and the angle between the robot and the center of arena.

Return `dist_arena` which is the distance to the center of the arena and `rot_arena` which is the angle between the robot and the center of arena.

### find_token(v)

This function return the code, the distance and the angle between the robot and closest token founded.

Takes as parameter `v` which contains the code of the token already brought into the center of the arena.

Returns `dist` which is the distance to the closest marker and `rot_y` which is the angle between the robot and the closest marker.

### goToArena(dist_arena, rot_arena, grabbed)

This function guide the robot towards the center of arena once it is welle aligned and release the token in the center of the arena.

Takes as parameter `dist_arena` which is the distance from the arena, `rot_arena` is the angle between the robot and the center of arena and `grabbed` which is a boolean parameter that is `true` if the robot is holding a token, `false` if the robot is free.

### goToMarker(code, dist, rot_y, v)

This function guide the robot towards the nearest token once that is well aligned.

Takes as parameter `code` which is the code of the nearest token, `dist` the distance from the token, `rot_y` the angle between the robot and the token and `v` which is the list that contains all the code of the token already brought in the center of the arena.

### main()

Call the function mentioned above to controll the robot with the aim to bring all the token which see in the center of the arena, and contain a while loop that is used when the robot doesn't see any token, and so the robot start turning till he does a rotation of 360°, and then if the robot didn't see any token the script stops.
