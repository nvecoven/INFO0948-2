# -*- coding: utf-8 -*-
from vrchk import vrchk

def youbot_init(vrep, id):
    #Initialize youBot
    
    # (C) Copyright Renaud Detry 2013, Norman 2019.
    # Distributed under the GNU General Public License.
    # (See http://www.gnu.org/copyleft/gpl.html)
    
    # Retrieve all handles, and stream arm and wheel joints, the robot's pose,
    # the Hokuyo, and the arm tip pose. Store them in a structure. 
    handles = {}
    handles['id'] = id
    
    # Wheel handles. 
    wheelJoints = [0]*4 # front left, rear left, rear right, front right
    res, wheelJoints[0] = vrep.simxGetObjectHandle(id, 'rollingJoint_fl', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    res, wheelJoints[1] = vrep.simxGetObjectHandle(id, 'rollingJoint_rl', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    res, wheelJoints[2] = vrep.simxGetObjectHandle(id, 'rollingJoint_rr', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    res, wheelJoints[3] = vrep.simxGetObjectHandle(id, 'rollingJoint_fr', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    
    for i in range(0, 4):
        vrep.simxSetJointTargetVelocity(id, wheelJoints[i], 0, vrep.simx_opmode_oneshot)
        vrchk(vrep, res)

    handles['wheelJoints'] = wheelJoints
    
    #♦ Have a look at youbot_drive for these values. 
    handles['previousForwBackVel'] = 0
    handles['previousLeftRightVel'] = 0
    handles['previousRotVel'] = 0
    
    ## Sensor handles. 
    # The Hokuyo sensor is implemented with two planar sensors that each cover 120 degrees, hence the two handles 
    res, hokuyo1 = vrep.simxGetObjectHandle(id, 'fastHokuyo_sensor1', vrep.simx_opmode_oneshot_wait); vrchk(vrep, res)
    res, hokuyo2 = vrep.simxGetObjectHandle(id, 'fastHokuyo_sensor2', vrep.simx_opmode_oneshot_wait); vrchk(vrep, res)
    
    handles['hokuyo1'] = hokuyo1
    handles['hokuyo2'] = hokuyo2
    
    res, xyzSensor = vrep.simxGetObjectHandle(id, 'xyzSensor', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    res, rgbSensor = vrep.simxGetObjectHandle(id, 'rgbSensor', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    res, rgbdCasing = vrep.simxGetObjectHandle(id, 'rgbdSensor', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    
    handles['xyzSensor'] = xyzSensor
    handles['rgbSensor'] = rgbSensor
    handles['rgbdCasing'] = rgbdCasing
    
    ## Robot handles. 
    res, ref = vrep.simxGetObjectHandle(id, 'youBot_center', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    res, armRef = vrep.simxGetObjectHandle(id, 'youBot_ref', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    
    handles['ref'] = ref
    handles['armRef'] = armRef
    
    ## Arm handles. 
    # The project page ( http://renaud-detry.net/teaching/info0948/private/project.php )
    # contains information on the different control modes of the arm. Search for
    # km_mode on the project webpage to find the arm documentation. Read that documentation
    # before working with the code below.
    
    # The *position* of this object always corresponds to the position of the tip of
    # the arm (the tip is somewhere between the two fingers)
    res, ptip = vrep.simxGetObjectHandle(id, 'youBot_gripperPositionTip', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    # In IK mode (km_mode set to 1 or 2), the robot will try to move the *position*
    # of ptip to the *position* of ptarget.
    res, ptarget = vrep.simxGetObjectHandle(id, 'youBot_gripperPositionTarget', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    # The *orientation* of this object always corresponds to the orientation of the tip of
    # the arm (the tip is somewhere between the two fingers)
    res, otip = vrep.simxGetObjectHandle(id, 'youBot_gripperOrientationTip', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    # In IK mode 2 (km_mode set to 2), the robot will try to move the *orientation*
    # of otip to the *orientation* of otarget.
    res, otarget = vrep.simxGetObjectHandle(id, 'youBot_gripperOrientationTarget', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    # Tip orientations are easier to manipulate in the reference frame of Rectangle22,
    # because then the degree of freedom onto which the orientation controller acts
    # corresponds to one of the three Euler angles of the tip orientation.
    res, r22 = vrep.simxGetObjectHandle(id, 'Rectangle22', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    
    handles['ptip'] = ptip
    handles['ptarget'] = ptarget
    handles['otip'] = otip
    handles['otarget'] = otarget
    handles['r22'] = r22
    

    armJoints = [0]*5
    for i in range(0, 5):
        res, armJoints[i] = vrep.simxGetObjectHandle(id, 'youBotArmJoint'+str(i), vrep.simx_opmode_oneshot_wait) 
        vrchk(vrep, res)

    handles['armJoints'] = armJoints
    
    res, mapLooker = vrep.simxGetObjectHandle(id, 'map', vrep.simx_opmode_oneshot_wait); vrchk(vrep, res)
    handles['mapLooker'] = mapLooker
    
    res, landmarks = vrep.simxGetObjectHandle(id, 'Landmarks', vrep.simx_opmode_oneshot_wait); vrchk(vrep, res)
    handles['landmarks'] = landmarks
    
    ## Examples: getting information from the simulator (and testing the connection works). 
    # Stream wheel angles, Hokuyo data, and robot pose (see usage below)
    # Wheel angles are not used in this example, but they may be necessary in
    # your project.
    for i in range(0, 4):
        res,_ = vrep.simxGetJointPosition(id, wheelJoints[i], vrep.simx_opmode_streaming)
        vrchk(vrep, res, True)
        
        
    res,_ = vrep.simxGetObjectPosition(id, ref, -1, vrep.simx_opmode_streaming)
    vrchk(vrep, res, True)
    res,_ = vrep.simxGetObjectOrientation(id, ref, -1, vrep.simx_opmode_streaming)
    vrchk(vrep, res,True)
    res, _, _ = vrep.simxReadVisionSensor(id, hokuyo1, vrep.simx_opmode_streaming)
    vrchk(vrep, res, True)
    res, _, _ = vrep.simxReadVisionSensor(id, hokuyo2, vrep.simx_opmode_streaming)
    vrchk(vrep, res, True)
    
    # Stream the arm joint angles and the tip position/orientation
    res,_ = vrep.simxGetObjectPosition(id, ptip, armRef, vrep.simx_opmode_streaming)
    vrchk(vrep, res, True)
    res,_ = vrep.simxGetObjectOrientation(id, otip, r22, vrep.simx_opmode_streaming)
    vrchk(vrep, res, True)
    
    for i in range(0, 5):
        res,_ = vrep.simxGetJointPosition(id, armJoints[i], vrep.simx_opmode_streaming)
        vrchk(vrep, res, True)

    
    # Make sure that all streaming data has reached the client at least once
    vrep.simxGetPingTime(id)
    
    return handles