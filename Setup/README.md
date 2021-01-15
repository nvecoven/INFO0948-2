# Setup for the project.

## Coppelia installation

First, download and install the Coppelia application as detailed in the "Coppelia" subfolder.

## Install python / matlab components

Install the CoppeliaSim bindings for Python or Matlab. Explanations are given in the respective subfolders.

You should now have been able to perform the binding test without getting errors.


---

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

---

# Programming the youBot

First, follow the [setup procedure](setup.html) to get your laptop ready.

Most of the youBot functionalities can be understood by browsing through the [youBot example script](https://github.com/ULgRobotics/trs/blob/master/youbot/youbot.m), which shows how to access to the sensors and actuators of the youBot.

The [example script](https://github.com/ULgRobotics/trs/blob/master/youbot/youbot.m) is located in the directory `youbot` of the [course's Git repository](#git). To run the example:

1.  Open the file `house.ttt` in CoppeliaSim.

2.  In MATLAB, go to (`cd`) to the `youbot` directory, and start the `youbot` script. It automatically starts the simulation; if it did not work, hit the _start simulation_ button ![start](../img/simulation1.jpg).

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

# Documentation And Useful Links

The Robotics Toolbox's documentation is available [here](http://petercorke.com/Robotics_Toolbox.html).

The documentation of the CoppeliaSim simulator is available [here](http://www.CoppeliaSim.eu/helpFiles/index.html) (also available via the Help menu in CoppeliaSim). Within the doc, the two most important pages are:

*   The [Simulation](https://www.coppeliarobotics.com/helpFiles/en/simulation.htm) and [Simulation settings dialog](https://www.coppeliarobotics.com/helpFiles/en/simulationPropertiesDialog.htm), that explain how the simulator works.
*   The [Remote API](https://www.coppeliarobotics.com/helpFiles/en/remoteApiOverview.htm), that allows you to speak to CoppeliaSim through the network:
    *   [Enabling the Remote API - server side](https://www.coppeliarobotics.com/helpFiles/en/remoteApiServerSide.htm): Read if you want to enable the _continuous_ service, for instance to allow MATLAB to start/stop the simulation. **Do not enable the _syncSimTrigger_ option, as you will not be allowed to do so during the project evaluation.**
    *   [Remote API modus operandi](https://www.coppeliarobotics.com/helpFiles/en/remoteApiModusOperandi.htm): Explains the network-related client-server issues.
    *   [Remote API constants](https://www.coppeliarobotics.com/helpFiles/en/remoteApiConstants.htm)
    *   [Remote API functions (C/C++)](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctions.htm#simxEraseFile)
    *   [Remote API functions (Python)](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm)
    *   [Remote API functions (MATLAB)](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm)

Other useful tools:

*   [MeshLab](http://meshlab.sourceforge.net) is an open-source graphical app for manipulating meshes. For instance, you can use it to inspect shapes from the CoppeliaSim environment. In CoppeliaSim, click on a shape and use the _Export as OBJ_ menu to write the shape to a file. In MeshLab, you can for instance use the ruler tool ![ruler](raster/ruler.png) to measure the length of the object.

# CoppeliaSim Remote API: Authorized Calls

In your project, you will be allowed to use only a subset of the CoppeliaSim API. Off-limits functions are, for instance, functions that change the environment (adding/removing/moving objects), functions that access information that would not be available to the robot in a real setup, or functions that move the robot in an unrealistic way.

The list below shows the functions that are authorized, some with restrictions. I built this list conservatively. It will probably grow in the coming weeks. I'm open to your suggestions.

Click here to [show](javascript: $('.vrep_denied').show())/[hide](javascript: $('.vrep_denied').hide()) unauthorized functions. Note that, by default, functions not shown in the list are off-limits.

*   [simxAddStatusbarMessage](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxAddStatusbarMessage)

*   [simxAppendStringSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxAppendStringSignal)

*   [simxAuxiliaryConsoleClose](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxAuxiliaryConsoleClose)

*   [simxAuxiliaryConsoleOpen](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxAuxiliaryConsoleOpen)

*   [simxAuxiliaryConsolePrint](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxAuxiliaryConsolePrint)

*   [simxAuxiliaryConsoleShow](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxAuxiliaryConsoleShow)

*   [simxBreakForceSensor](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxBreakForceSensor)

*   [simxClearFloatSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxClearFloatSignal)

*   [simxClearIntegerSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxClearIntegerSignal)

    Only on the following signals: [`displaylasers`](#displaylasers), `handle_xyz_sensor`, `handle_xy_sensor`, `handle_rgb_sensor`, [`gripper_open`](#gripper_open), [`km_mode`](#km_mode).

*   [simxClearStringSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxClearStringSignal)

*   [simxCloseScene](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxCloseScene)

*   [simxCopyPasteObjects](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxCopyPasteObjects)

*   [simxCreateBuffer](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxCreateBuffer)

*   [simxCreateDummy](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxCreateDummy)

*   [simxDisplayDialog](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxDisplayDialog)

*   [simxEndDialog](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxEndDialog)

*   [simxEraseFile](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxEraseFile)

*   [simxFinish](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxFinish)

*   [simxGetAndClearStringSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetAndClearStringSignal)

*   [simxGetArrayParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetArrayParameter)

*   [simxGetBooleanParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetBooleanParameter)

*   [simxGetCollisionHandle](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetCollisionHandle)

*   [simxGetConnectionId](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetConnectionId)

*   [simxGetDialogInput](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetDialogInput)

*   [simxGetDialogResult](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetDialogResult)

*   [simxGetDistanceHandle](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetDistanceHandle)

*   [simxGetFloatingParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetFloatingParameter)

*   [simxGetFloatSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetFloatSignal)

    Only with the following signal: `rgbd_sensor_scan_angle`.

*   [simxGetInMessageInfo](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetInMessageInfo)

*   [simxGetIntegerParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetIntegerParameter)

*   [simxGetIntegerSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetIntegerSignal)

    Only on the following signals: [`displaylasers`](#displaylasers), `handle_xyz_sensor`, `handle_xy_sensor`, `handle_rgb_sensor`, [`gripper_open`](#gripper_open), [`km_mode`](#km_mode).

*   [simxGetJointMatrix](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetJointMatrix)

    Only on the robot's joints.

*   [simxGetJointPosition](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetJointPosition)

    Only on the robot's joints.

*   [simxGetLastCmdTime](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetLastCmdTime)

*   [simxGetLastErrors](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetLastErrors)

*   [simxGetModelProperty](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetModelProperty)

*   [simxGetObjectChild](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetObjectChild)

*   [simxGetObjectFloatParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetObjectFloatParameter)

*   [simxGetObjectGroupData](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetObjectGroupData)

*   [simxGetObjectHandle](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetObjectHandle)

    Only for objects that are part of the robot.

*   [simxGetObjectIntParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetObjectIntParameter)

*   [simxGetObjectOrientation](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetObjectOrientation)

    Only with the following handle arguments, as in the simulator (the values between parentheses indicate the corresponding field of the structure returned by `youbot_init`):

    |objectHandle|relativeToObjectHandle|Milestone|
    |--- |--- |--- |
    |rgbdSensor (`rgbdCasing`)|youBot_ref (`armRef`), youBot_center (`ref`)|all except E|
    |xyzSensor (`xyzSensor`)|rgbdSensor (rgbdCasing)|(any)|
    |rgbSensor (`rgbSensor`)|rgbdSensor (rgbdCasing)|(any)|
    |fastHokuyo_sensor1 (`hokuyo1`)|youBot_ref (`armRef`), youBot_center (`ref`)|(any)|
    |fastHokuyo_sensor2 (`hokuyo2`)|youBot_ref (`armRef`), youBot_center (`ref`)|(any)|
    |youBot_ref (`armRef`), youBot_center (`ref`)|-1|all except A.2|
    |youBot_gripperPositionTip (`ptip`)|youBot_ref (`armRef`)|all except B.4|
    |youBot_gripperPositionTarget (`ptarget`)|youBot_ref (`armRef`)|all except B.4|
    |youBot_gripperOrientationTip (`otip`)|Rectangle22 (`r22`)|all except B.4|
    |youBot_gripperOrientationTarget (`otarget`)|Rectangle22 (`r22`)|all except B.4|

    In particular, in order to get the position of the arm, you must use `youBot_ref` as reference. Using the world (`-1`) will return inconsistent results.

    If these functions return inconsistent results, try with another mode (such as `vrep.simx_opmode_oneshot_wait` instead of the default `vrep.simx_opmode_buffer`).

*   [simxGetObjectParent](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetObjectParent)

*   [simxGetObjectPosition](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetObjectPosition)

    See [simxGetObjectOrientation](#simxGetObjectOrientation).

*   [simxGetObjects](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetObjects)

*   [simxGetObjectSelection](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetObjectSelection)

*   [simxGetOutMessageInfo](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetOutMessageInfo)

*   [simxGetPingTime](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetPingTime)

*   [simxGetStringParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetStringParameter)

*   [simxGetStringSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetStringSignal)

*   [simxGetUIButtonProperty](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetUIButtonProperty)

*   [simxGetUIEventButton](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetUIEventButton)

*   [simxGetUIHandle](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetUIHandle)

*   [simxGetUISlider](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetUISlider)

*   [simxGetVisionSensorDepthBuffer](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetVisionSensorDepthBuffer)

*   [simxGetVisionSensorImage](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetVisionSensorImage)

*   [simxGetVisionSensorImage2](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetVisionSensorImage2)

*   [simxJointGetForce](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxJointGetForce)

*   [simxLoadModel](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxLoadModel)

*   [simxLoadScene](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxLoadScene)

*   [simxLoadUI](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxLoadUI)

*   [simxPackFloats](remoteApiFunctionsPython.htm#simxPackFloats)

*   [simxPackInts](remoteApiFunctionsPython.htm#simxPackInts)

*   [simxPauseCommunication](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxPauseCommunication)

*   [simxPauseSimulation](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxPauseSimulation)

*   [simxQuery](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxQuery)

*   [simxReadCollision](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxReadCollision)

*   [simxReadDistance](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxReadDistance)

*   [simxReadForceSensor](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxReadForceSensor)

*   [simxReadProximitySensor](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxReadProximitySensor)

*   [simxReadVisionSensor](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxReadVisionSensor)

*   [simxReleaseBuffer](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxReleaseBuffer)

*   [simxRemoveObject](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxRemoveObject)

*   [simxRemoveUI](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxRemoveUI)

*   [simxRMLPosition](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxRMLPosition)

*   [simxRMLVelocity](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxRMLVelocity)

*   [simxSetArrayParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetArrayParameter)

*   [simxSetBooleanParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetBooleanParameter)

*   [simxSetFloatingParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetFloatingParameter)

*   [simxSetFloatSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetFloatSignal)

    Only with the following signal: `rgbd_sensor_scan_angle`.

*   [simxSetIntegerParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetIntegerParameter)

*   [simxSetIntegerSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetIntegerSignal)

    Only on the following signals: [`displaylasers`](#displaylasers), `handle_xyz_sensor`, `handle_xy_sensor`, `handle_rgb_sensor`, [`gripper_open`](#gripper_open), [`km_mode`](#km_mode).

*   [simxSetJointForce](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetJointForce)

*   [simxSetJointPosition](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetJointPosition)

*   [simxSetJointTargetPosition](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetJointTargetPosition)

    Only with the following joints: `youBotArmJoint*`.

*   [simxSetJointTargetVelocity](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetJointTargetVelocity)

    Only on the following joints: `rollingJoint_*`.

*   [simxSetModelProperty](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetModelProperty)

*   [simxSetObjectFloatParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetObjectFloatParameter)

*   [simxSetObjectIntParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetObjectIntParameter)

*   [simxSetObjectOrientation](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetObjectOrientation)

    Only with the following handle arguments, as in the simulator (the values between parentheses indicate the corresponding field of the structure returned by `youbot_init`):

    |objectHandle|relativeToObjectHandle|eulerAngles|Milestone|
    |--- |--- |--- |--- |
    |rgbdSensor (`rgbdCasing`)|youBot_ref (`armRef`), youBot_center (`ref`)|[0, 0, *]|(any)|
    |youBot_gripperOrientationTarget (`otarget`)|Rectangle22 (`r22`)|(any)|all except B.4|

*   [simxSetObjectParent](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetObjectParent)

*   [simxSetObjectPosition](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetObjectPosition)

    Only with the following handle arguments, as in the simulator (the values between parentheses indicate the corresponding field of the structure returned by `youbot_init`):

    |objectHandle|relativeToObjectHandle|Milestone|
    |--- |--- |--- |
    |youBot_gripperPositionTarget (`ptarget`)|youBot_ref (`armRef`)|all except B.4|

*   [simxSetObjectSelection](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetObjectSelection)

*   [simxSetSphericalJointMatrix](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetSphericalJointMatrix)

*   [simxSetStringSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetStringSignal)

*   [simxSetUIButtonLabel](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetUIButtonLabel)

*   [simxSetUIButtonProperty](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetUIButtonProperty)

*   [simxSetUISlider](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetUISlider)

*   [simxSetVisionSensorImage](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetVisionSensorImage)

*   [simxStart](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxStart)

*   [simxStartSimulation](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxStartSimulation)

*   [simxStopSimulation](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxStopSimulation)

*   [simxSynchronous](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSynchronous)

*   [simxSynchronousTrigger](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSynchronousTrigger)

*   [simxTransferFile](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxTransferFile)

*   [simxUnpackFloats](remoteApiFunctionsPython.htm#simxUnpackFloats)

*   [simxUnpackInts](remoteApiFunctionsPython.htm#simxUnpackInts)

# MATLAB Tips

## Avoiding Loops

MATLAB is an interpreted language. Despite recent progress in the JIT accelerator, running loops in MATLAB is still _much_ slower than running loops in native code. Since most MATLAB functions rely on a C implementation of large loops, it is good practice to always prefer calling a function over writing a loop when handling large datatypes. In your project, the two datatypes that you need to handle with care are images and point clouds (from the RGB camera, or from the 2D/3D laser scanners). **Handling images and point clouds with MATLAB functions or MEX functions instead of MATLAB loops will often make your code 100 times faster.**

An example of the computational cost of flipping an image with a loop vs. a MATLAB function is provided [here](https://github.com/ULgRobotics/trs/blob/master/matlab/test_loop_vs_native.m).

## Running Code from Files

The MATLAB JIT accelerator doesn't optimize code typed into the console, even though recent versions of MATLAB have greatly improved in terms of performance. To verify this behavior, run the function above by typing `test_loop_vs_native` in the console, then by copy-pasting the contents of the `test_loop_vs_native` function directly into the console. As a result of this behavior, always run your code from `.m` files.

# youBot Tips

## Unintentional Movements

CoppeliaSim does a pretty good job of simulating the real world. This can sometimes lead to unexpected problems. For instance, if no input is given to the wheels and the arm is swung back and front, the robot will move back and forth (slightly). In the third example below, you can verify that the final robot position is about a centimeter further than the initial position.

## Physics Engine

We recommend using the ODE engine.

## Use the Toolboxes!

There are plenty of functions in Peter Corke's Robotics Toolbox that will help you with high-level algorithms (path planning, vision…), but also low-level computations (pose transformation, angle distance…). Don't forget to use them!

If you have them, MATLAB also has many interesting toolboxes for this project: for computer vision ([MATLAB Image Processing Toolbox](https://fr.mathworks.com/products/image.html), [MATLAB Computer Vision System](https://www.mathworks.com/products/computer-vision.html)), machine learning ([Statistics and Machine Learning](https://www.mathworks.com/products/statistics.html)), and robotics ([Robotics System](https://www.mathworks.com/products/robotics.html)), more specifically. Pay attention that not all of them are included in the student version of MATLAB.

## Useful Functions/Tools

*   The MATLAB `inpolygon` function

# Troubleshooting CoppeliaSim

## Avoiding Mysteriously Dangerous Calls

For a mysterious reason, calling

`res = vrep.simxReadVisionSensor(id, hokuyo1Handle, vrep.simx_opmode_buffer);`

with only **one return value** crashes some versions of MATLAB. Always use the multi-return call instead:

`[res det auxData auxPacketInfo] = vrep.simxReadVisionSensor(id, hokuyo1Handle, vrep.simx_opmode_buffer);`

## CoppeliaSim Crashing at Startup, or MATALB Cannot Connect to CoppeliaSim

When CoppeliaSim quits, the port that it was using to listen for connexions is not freed immediately. If your CoppeliaSim crashes when you try to start it up, or if you cannot connect to CoppeliaSim from MATLAB, quit CoppeliaSim, wait a few dozen seconds, and try again.
