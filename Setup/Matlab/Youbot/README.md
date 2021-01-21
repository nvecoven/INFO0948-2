# First test of the youbot

In MATLAB, run the startup_robot.m file provided via the Git repository. 
```matlab
run('~/trs/Setup/Matlab/Youbot/startup_robot.m');
```

This line needs to be run every time MATLAB restarts. 
You may want to add it to your MATLAB startup file. 
This first checks whether P. Corke's RVC toolbox is downloaded (and downloads it if it's not),
 and then updates MATLAB's path so that it can find the toolbox functions and the V-REP binding.
 
 # Programming the youBot

First, follow the [setup procedure](setup.html) to get your laptop ready.

Most of the youBot functionalities can be understood by browsing through the [youBot example script](https://github.com/ULgRobotics/trs/blob/master/youbot/youbot.m), which shows how to access to the sensors and actuators of the youBot.

The [example script](https://github.com/ULgRobotics/trs/blob/master/youbot/youbot.m) is located in the directory `youbot` of the [course's Git repository](#git). To run the example:

1.  Open the file [`house.ttt`](https://github.com/nvecoven/robotic_rework/blob/main/Setup/Coppelia/Scenes/House/house.ttt) in CoppeliaSim.

2.  In MATLAB, go to (`cd`) to the `youbot` directory, and start the `youbot` script. It automatically starts the simulation; if it did not work, hit the _start simulation_ button ![start](https://github.com/nvecoven/robotic_rework/blob/main/img/simulation1.jpg).

The sections below provide more details about the youBot's sensors, actuators, and gripper.

## Names of CoppeliaSim Components

The CoppeliaSim names of the youBot's components are listed below. You can get a programmatic handle to these components via the [simxGetObjectHandle](#simxGetObjectHandle) method. It is automatically done when you use the `youbot_init` script: the fields of the returned structure have slightly different names, they are given between parentheses.

*   `youBot_ref` (`armRef`): a point on the rotation axis of the first arm joint.
*   `youBot_center` (`ref`): the center of the youBot's frame.
*   `rollingJoint_fl` (`wheelJoints(1)`), `rollingJoint_rl` (`wheelJoints(2)`), `rollingJoint_rr` (`wheelJoints(3)`), `rollingJoint_fr` (`wheelJoints(4)`): the four wheel joints.
*   `rgbdSensor` (`rgbdCasing`): the box containing the depth and photometric cameras.
*   ``xyzSensor (`xyzSensor`)``, `rgbSensor` (`rgbSensor`), `fastHokuyo_sensor1` (`hokuyo1`), `fastHokuyo_sensor2` (`hokuyo2`): the depth and photometric cameras, and the two 120–degree Hokuyo sensors.
\>*   `Rectangle22` (`r22`): the rectangle at the bottom of the arm.

## Signals for Controlling the youBot's Sensors and Gripper

The youBot's sensors can be turned on or off through following CoppeliaSim signals: `handle_xyz_sensor`, `handle_xy_sensor` and `handle_rgb_sensor`. (See for instance [simxSetIntegerSignal](#simxSetIntegerSignal).) The value of `handle_xyz_sensor` controls the depth camera:

*   `handle_xyz_sensor` set to 0 (or undefined): the depth camera is off.
*   `handle_xyz_sensor` set to 1: the depth camera is turned on, takes one shot, and is automatically turned off again.
*   `handle_xyz_sensor` set to 2: the depth camera is turned on, and stays on until the value of the signal is changed again.

The RGB camera is controlled in the same way with `handle_rgb_sensor`. The signal `handle_xy_sensor` controls _both_ `fastHokuyo_sensor1` and `fastHokuyo_sensor2`.

The three signals `handle_xyz_sensor`, `handle_xy_sensor` and `handle_rgb_sensor` only control whether CoppeliaSim is computing what the sensors see. Setting one of these signals to 1 or 2 will **not** make CoppeliaSim send the data over to MATLAB. Whether and how the data is sent to MATLAB is controlled via [simxReadVisionSensor](#simxReadVisionSensor) or [simxGetVisionSensorImage2](#simxGetVisionSensorImage2) and [remote operation modes](http://www.coppeliarobotics.com/helpFiles/en/remoteApiConstants.htm#operationModes) (such as _streaming_, _oneshot_, etc.).

It generally presents no problem to leave the Hokuyo sensor continuously on, and to get its data with the _streaming_ operation mode (see the [example script](https://github.com/ULgRobotics/trs/blob/master/youbot/youbot.m)). However, the RGB and depth cameras however are expensive to run. They slow down CoppeliaSim, and clog the network. It is advised to turn the two cameras on only when needed, by setting their signal to 1, and recovering the generated image or point cloud with the _oneshot_ or _oneshot\_wait_ operation mode (see the [main example script](https://github.com/ULgRobotics/trs/blob/master/youbot/youbot.m) and the focused examples for the [RGB](https://github.com/ULgRobotics/trs/blob/master/youbot/focused/youbot_photo.m) and [depth](https://github.com/ULgRobotics/trs/blob/master/youbot/focused/youbot_3dpointcloud.m) cameras).

The view angle of the depth camera and the RGB camera can be controlled via a signal named `rgbd_sensor_scan_angle`:

`res = vrep.simxSetFloatSignal(id, 'rgbd_sensor_scan_angle', pi/8, vrep.simx_opmode_oneshot_wait); check(vrep, res);`

The default angle is `pi/4`.

The `gripper_open` signal controls the gripper:

*   `gripper_open` set to 1 or unset: the gripper opens.
*   `gripper_open` set to 0: the gripper closes and applies a constant force inwards (it is not possible to control it).

The `km_mode` signal turns the robot's inverse kinematics mode on or off:

*   `km_mode` set to 0 or unset: the arm joints are in position-control mode. Use [simxSetJointTargetPosition](#simxSetJointTargetPosition) to change the arm's configuration.
*   `km_mode` set to 1: activates a controller that attempts to move the tip of the gripper to the _position_ of `youBot_gripperPositionTarget`. Use [simxSetObjectPosition](#simxSetObjectPosition) on `youBot_gripperPositionTarget` to move the tip of the arm to a position in the youBot's frame.
*   `km_mode` set to 2: activates a controller that attempts to move the tip of the gripper to the position of `youBot_gripperPositionTarget`, and to partially align the gripper to the orientation of `youBot_gripperPositionTarget`. Since the youBot's arm has only five DOFs, it cannot reach any arbitrary orientation. This controller only changes the orientation of the gripper around the axis of the second/third/fourth joint. Use [simxSetObjectPosition](#simxSetObjectPosition) on `youBot_gripperPositionTarget` to move the tip of the arm to a position in the youBot's frame, and [simxSetObjectOrientation](#simxSetObjectOrientation) on `youBot_gripperOrientationTarget` to partially orient the tip of the arm to an angle in the frame of the first link of the arm. See example below for details.

The `displaylasers` signal turns the CoppeliaSim laser display on or off. When `displaylasers` is set (whatever its value), CoppeliaSim displays red rays along the scanning lines of the Hokuyo, or red dots at the scanning points of the depth sensor. The only purpose served by this signal is illustration, and displaying the lasers slows CoppeliaSim down. You will generally want to keep this function off.


