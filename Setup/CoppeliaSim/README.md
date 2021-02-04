# CoppeliaSim Edu

## CoppeliaSim installation

First, download the latest version of [CoppeliaSim Edu](https://www.coppeliarobotics.com/downloads).

Once downloaded, unpack the archive and install it in the folder of your choice.

If your firewall asks you whether CoppeliaSim should be allowed, always answer *yes*: the communication between CoppeliaSim and MATLAB or Python will take place via the network (internal to your computer). Otherwise, you will face problems later on.

Once done, you can proceed to linking [CoppeliaSim with the language of your choice](https://github.com/nvecoven/robotic_rework/tree/main/Setup).

## Documentation And Useful Links

The Robotics Toolbox's documentation is available [here](http://petercorke.com/Robotics_Toolbox.html).

The documentation of the CoppeliaSim simulator is available [here](http://www.CoppeliaSim.eu/helpFiles/index.html) (also available via the Help menu in CoppeliaSim). Within the doc, the two most important pages are:

*   The [Simulation](https://www.coppeliarobotics.com/helpFiles/en/simulation.htm) and [Simulation settings dialog](https://www.coppeliarobotics.com/helpFiles/en/simulationPropertiesDialog.htm), that explain how the simulator works.
*   The [Remote API](https://www.coppeliarobotics.com/helpFiles/en/remoteApiOverview.htm), that allows you to speak to CoppeliaSim through the network:
    *   [Enabling the Remote API - server side](https://www.coppeliarobotics.com/helpFiles/en/remoteApiServerSide.htm): Read if you want to enable the _continuous_ service, for instance to allow MATLAB to start/stop the simulation.
    <!-- **Do not enable the _syncSimTrigger_ option, as you will not be allowed to do so during the project evaluation.** -->
    *   [Remote API modus operandi](https://www.coppeliarobotics.com/helpFiles/en/remoteApiModusOperandi.htm): Explains the network-related client-server issues.
    *   [Remote API constants](https://www.coppeliarobotics.com/helpFiles/en/remoteApiConstants.htm)
    *   [Remote API functions (C/C++)](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctions.htm#simxEraseFile)
    *   [Remote API functions (Python)](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm)
    *   [Remote API functions (MATLAB)](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm)

Other useful tools:

*   [MeshLab](http://meshlab.sourceforge.net) is an open-source graphical app for manipulating meshes. For instance, you can use it to inspect shapes from the CoppeliaSim environment. In CoppeliaSim, click on a shape and use the _Export as OBJ_ menu to write the shape to a file. In MeshLab, you can for instance use the ruler tool ![ruler](https://github.com/nvecoven/INFO0948-2/blob/main/img/ruler.png) to measure the length of the object.


## CoppeliaSim Remote API: Authorized Calls

In your project, you will be allowed to use only a subset of the CoppeliaSim API. Off-limits functions are, for instance, functions that change the environment (adding/removing/moving objects), functions that access information that would not be available to the robot in a real setup, or functions that move the robot in an unrealistic way.

The list below shows the functions that are authorized, some with restrictions. I built this list conservatively. It will probably grow in the coming weeks. I'm open to your suggestions.

<!-- Click here to [show](javascript: $('.vrep_denied').show())/[hide](javascript: $('.vrep_denied').hide()) unauthorized functions.  -->
Note that, by default, functions not shown in the list are off-limits.

<!---*   :white_check_mark: [simxAddStatusbarMessage](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxAddStatusbarMessage)

*   :red_circle: [simxAppendStringSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxAppendStringSignal)

*   [simxAuxiliaryConsoleClose](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxAuxiliaryConsoleClose)

*   [simxAuxiliaryConsoleOpen](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxAuxiliaryConsoleOpen)

*   [simxAuxiliaryConsolePrint](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxAuxiliaryConsolePrint)

*   [simxAuxiliaryConsoleShow](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxAuxiliaryConsoleShow)

*   [simxBreakForceSensor](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxBreakForceSensor)

*   [simxClearFloatSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxClearFloatSignal)--->

*   [simxClearIntegerSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxClearIntegerSignal)

    Only on the following signals: [`displaylasers`](#displaylasers), `handle_xyz_sensor`, `handle_xy_sensor`, `handle_rgb_sensor`, [`gripper_open`](#gripper_open), [`km_mode`](#km_mode).

*   [simxClearStringSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxClearStringSignal)

*   [simxCloseScene](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxCloseScene)

<!---*   [simxCopyPasteObjects](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxCopyPasteObjects)--->

*   [simxCreateBuffer](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxCreateBuffer)

*   [simxCreateDummy](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxCreateDummy)

*   [simxDisplayDialog](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxDisplayDialog)

*   [simxEndDialog](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxEndDialog)

*   [simxEraseFile](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxEraseFile)

*   [simxFinish](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxFinish)

<!---*   [simxGetAndClearStringSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetAndClearStringSignal)

*   [simxGetArrayParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetArrayParameter)

*   [simxGetBooleanParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetBooleanParameter)

*   [simxGetCollisionHandle](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetCollisionHandle)

*   [simxGetConnectionId](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetConnectionId)

*   [simxGetDialogInput](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetDialogInput)

*   [simxGetDialogResult](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetDialogResult)

*   [simxGetDistanceHandle](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetDistanceHandle)--->

*   [simxGetFloatingParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetFloatingParameter)

*   [simxGetFloatSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetFloatSignal)

    Only with the following signal: `rgbd_sensor_scan_angle`.

<!---*   [simxGetInMessageInfo](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetInMessageInfo)--->

*   [simxGetIntegerParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetIntegerParameter)

*   [simxGetIntegerSignal](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetIntegerSignal)

    Only on the following signals: [`displaylasers`](#displaylasers), `handle_xyz_sensor`, `handle_xy_sensor`, `handle_rgb_sensor`, [`gripper_open`](#gripper_open), [`km_mode`](#km_mode).

*   [simxGetJointMatrix](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetJointMatrix)

    Only on the robot's joints.

*   [simxGetJointPosition](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetJointPosition)

    Only on the robot's joints.

*   [simxGetLastCmdTime](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetLastCmdTime)

*   [simxGetLastErrors](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetLastErrors)

<!---*   [simxGetModelProperty](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetModelProperty)

*   [simxGetObjectChild](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetObjectChild)

*   [simxGetObjectFloatParameter](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetObjectFloatParameter)

*   [simxGetObjectGroupData](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxGetObjectGroupData)--->

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

<!---*   [simxSetObjectParent](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm#simxSetObjectParent)--->

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



## CoppeliaSim Tips

### Unintentional Movements

CoppeliaSim does a pretty good job of simulating the real world. This can sometimes lead to unexpected problems. For instance, if no input is given to the wheels and the arm is swung back and front, the robot will move back and forth (slightly). In the third example below, you can verify that the final robot position is about a centimeter further than the initial position.

### Physics Engine

We recommend using the ODE engine.


## Troubleshooting CoppeliaSim with MATLAB

### Avoiding Mysteriously Dangerous Calls

For a mysterious reason, calling

`res = vrep.simxReadVisionSensor(id, hokuyo1Handle, vrep.simx_opmode_buffer);`

with only **one return value** crashes some versions of MATLAB. Always use the multi-return call instead:

`[res det auxData auxPacketInfo] = vrep.simxReadVisionSensor(id, hokuyo1Handle, vrep.simx_opmode_buffer);`

### CoppeliaSim Crashing at Startup, or MATLAB Cannot Connect to CoppeliaSim

When CoppeliaSim quits, the port that it was using to listen for connexions is not freed immediately. If your CoppeliaSim crashes when you try to start it up, or if you cannot connect to CoppeliaSim from MATLAB, quit CoppeliaSim, wait a few dozen seconds, and try again.
