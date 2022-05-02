# -*- coding: utf-8 -*-
"""
# youbot Illustrates the V-REP MATLAB bindings, more specifically the way to take a 3D point cloud.

# (C) Copyright Renaud Detry 2013, Thibaut Cuvelier 2017.
# Distributed under the GNU General Public License.
# (See http://www.gnu.org/copyleft/gpl.html)
"""
# VREP
import sim as vrep

# Useful import
import time
import numpy as np
import sys
import matplotlib.pyplot as plt
import open3d

from cleanup_vrep import cleanup_vrep
from vrchk import vrchk
from youbot_init import youbot_init
from youbot_drive import youbot_drive
from youbot_hokuyo_init import youbot_hokuyo_init
from youbot_hokuyo import youbot_hokuyo
from youbot_xyz_sensor import youbot_xyz_sensor
from utils_sim import angdiff
from scipy.spatial.transform import Rotation as R

def get_transform(handle1, handle2):
    """Return the transform matrix (4x4)."""
    res, pos = vrep.simxGetObjectPosition(clientID, handle1, handle2, vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res, True)
    res, euler_angles = vrep.simxGetObjectOrientation(clientID, handle1, handle2, vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res, True)
    T = np.eye(4)
    T[:3, :3] = open3d.geometry.TriangleMesh.create_coordinate_frame().get_rotation_matrix_from_xyz(euler_angles)
    T[:3, 3] = np.array(pos).T
    
    return T

def get_transform_ori(handle1, handle2):
    """Return the transform matrix 4x4 only for rotation."""
    res, euler_angles = vrep.simxGetObjectOrientation(clientID, handle1, handle2, vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res, True)
    T = np.eye(4)
    T[:3, :3] = open3d.geometry.TriangleMesh.create_coordinate_frame().get_rotation_matrix_from_xyz(euler_angles)
    
    return T

def get_transform_from_euler(euler_angles):
    T = np.eye(4)
    T[:3, :3] = open3d.geometry.TriangleMesh.create_coordinate_frame().get_rotation_matrix_from_xyz(euler_angles)
    
    return T
    

# Test the python implementation of a youbot
# Initiate the connection to the simulator.
print('Program started')
# Use the following line if you had to recompile remoteApi
# vrep = remApi('remoteApi', 'extApi.h')
# vrep = remApi('remoteApi')

# Close the connection in case if a residual connection exists
vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1',  19997, True, True, 2000, 5)

# The time step the simulator is using (your code should run close to it).
timestep = .05

# Synchronous mode
returnCode = vrep.simxSynchronous(clientID, True)

# If you get an error like: 
#   Remote API function call returned with error code: 64. Explanation: simxStart was not yet called.
# Make sure your code is within a function! You cannot call V-REP from a script. 
if clientID < 0:
    sys.exit('Failed connecting to remote API server. Exiting.')

print('Connection ' + str(clientID) + ' to remote API server open')

# Make sure we close the connection whenever the script is interrupted.
# cleanup_vrep(vrep, id)

# This will only work in "continuous remote API server service".
# See http://www.v-rep.eu/helpFiles/en/remoteApiServerSide.htm
vrep.simxStartSimulation(clientID, vrep.simx_opmode_blocking)

# Send a Trigger to the simulator: this will run a time step for the physic engine
# because of the synchronous mode. Run several iterations to stabilize the simulation
for i in range(int(1./timestep)):
    vrep.simxSynchronousTrigger(clientID)
    vrep.simxGetPingTime(clientID)

# Retrieve all handles, mostly the Hokuyo.
h = youbot_init(vrep, clientID)
h = youbot_hokuyo_init(vrep, h)

# Send a Trigger to the simulator: this will run a time step for the physic engine
# because of the synchronous mode. Run several iterations to stabilize the simulation
for i in range(int(1./timestep)):
    vrep.simxSynchronousTrigger(clientID)
    vrep.simxGetPingTime(clientID)


# Parameters for controlling the youBot's wheels: at each iteration,
# those values will be set for the wheels.
# They are adapted at each iteration by the code.
forwBackVel = 0  # Move straight ahead.
rightVel = 0  # Go sideways.
rotateRightVel = 0  # Rotate.

# First state of state machine
fsm = 'take_shot'
print('Switching to state: ', fsm)

# Get the initial position
res, youbotPos = vrep.simxGetObjectPosition(clientID, h['ref'], -1, vrep.simx_opmode_buffer)
# Set the speed of the wheels to 0.
h = youbot_drive(vrep, h, forwBackVel, rightVel, rotateRightVel)


# Get the target orientation
[res, targetori] = vrep.simxGetObjectOrientation(clientID, h["otarget"], h["r22"], vrep.simx_opmode_oneshot_wait)
# Get the gripper orientation
[res, tori] = vrep.simxGetObjectOrientation(clientID, h["otip"], h["r22"], vrep.simx_opmode_oneshot_wait)

# Send a Trigger to the simulator: this will run a time step for the physic engine
# because of the synchronous mode. Run several iterations to stabilize the simulation.
for i in range(int(1./timestep)):
    vrep.simxSynchronousTrigger(clientID)
    vrep.simxGetPingTime(clientID)
    


# Start the demo. 
while True:
    try:
        # Time management
        t_loop = time.perf_counter()
        # Check the connection with the simulator
        if vrep.simxGetConnectionId(clientID) == -1:
            sys.exit('Lost connection to remote API.')

        # Get the position and the orientation of the robot.
        res, youbotPos = vrep.simxGetObjectPosition(clientID, h['ref'], -1, vrep.simx_opmode_streaming)
        vrchk(vrep, res, True) # Check the return value from the previous V-REP call (res) and exit in case of error.
        res, youbotEuler = vrep.simxGetObjectOrientation(clientID, h['ref'], -1, vrep.simx_opmode_streaming)
        vrchk(vrep, res, True)
        
        # Apply the state machine.
        if fsm == 'take_shot':

            # Read data from the depth camera (Hokuyo)
            # Reading a 3D image costs a lot to VREP (it has to simulate the image). It also requires a lot of 
            # bandwidth, and processing a 3D point cloud (for instance, to find one of the boxes or cylinders that 
            # the robot has to grasp) will take a long time in MATLAB. In general, you will only want to capture a 3D 
            # image at specific times, for instance when you believe you're facing one of the tables.
            
            # Reduce the view angle to pi/8 in order to better see the objects. Do it only once. 
            # ^^^^^^     ^^^^^^^^^^    ^^^^                                     ^^^^^^^^^^^^^^^ 
            # simxSetFloatSignal                                                simx_opmode_oneshot_wait
            #            |
            #            rgbd_sensor_scan_angle
            # The depth camera has a limited number of rays that gather information. If this number is concentrated 
            # on a smaller angle, the resolution is better. pi/8 has been determined by experimentation. 
            res = vrep.simxSetFloatSignal(clientID, 'rgbd_sensor_scan_angle', np.pi/8, vrep.simx_opmode_oneshot_wait)
            vrchk(vrep, res) # Check the return value from the previous V-REP call (res) and exit in case of error.
            
            # Ask the sensor to turn itself on, take A SINGLE POINT CLOUD, and turn itself off again. 
            # ^^^     ^^^^^^                ^^       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            # simxSetIntegerSignal          1        simx_opmode_oneshot_wait
            #         |
            #         handle_xyz_sensor
            res = vrep.simxSetIntegerSignal(clientID, 'handle_xyz_sensor', 1, vrep.simx_opmode_oneshot_wait)
            vrchk(vrep, res)
            
            ################# BE CAREFUL #################
            # For some reasons, the vrep call can return None. In this case, you can safetly ignore the verification 'vrchk'
            
            vrep.simxSynchronousTrigger(clientID)
            vrep.simxGetPingTime(clientID)
            
            # Simulation with capturing raw point cloud.
            # Then retrieve the last point cloud the depth sensor took.
            # If you were to try to capture multiple images in a row, try other values than 
            # vrep.simx_opmode_oneshot_wait. 
            print('Capturing point cloud...\n');
            pts = youbot_xyz_sensor(vrep, h, vrep.simx_opmode_oneshot_wait)
            print(pts.shape)
            vrep.simxSynchronousTrigger(clientID)
            vrep.simxGetPingTime(clientID)
            
            ###################################################################
            # Processing of your point cloud, depth images, etc...
            
            # Get the transform point cloud to ref
            T_xyz_ref = get_transform(h["xyzSensor"], h["ref"])
            
            # Change to rotate
            fsm = "rotate"
            init_youbot_z = youbotEuler[2]
            print('Switching to state: ', fsm)

        elif fsm == 'rotate':
            # Rotate until the robot has an angle of -pi/2 (measured with respect to the world's reference frame). 
            # Again, use a proportional controller. In case of overshoot, the angle difference will change sign, 
            # and the robot will correctly find its way back (e.g.: the angular speed is positive, the robot overshoots, 
            # the anguler speed becomes negative). 
            # youbotEuler(3) is the rotation around the vertical axis.              
            rotateRightVel = angdiff(youbotEuler[2], (init_youbot_z-np.pi))

            # Stop when the robot is at an angle close to -pi/2.
            if abs(angdiff(youbotEuler[2], (init_youbot_z-np.pi))) < .002:
                rotateRightVel = 0
                # Turn the robot of 180°
                T_ref1_ref2 = np.eye(4)
                T_ref1_ref2[:3, :3] = open3d.geometry.TriangleMesh.create_coordinate_frame().get_rotation_matrix_from_xyz([0., 0., np.pi])
                fsm = 'rotate_arm'
                print('Switching to state: ', fsm)
        
        elif fsm == 'rotate_arm':
            # Rotate the arm
            # Joint 0
            target_joint_0 = np.pi            
            res = vrep.simxSetJointTargetPosition(clientID, h["armJoints"][0], target_joint_0, vrep.simx_opmode_oneshot)            
            res, joint_0 = vrep.simxGetJointPosition(clientID, h["armJoints"][0], vrep.simx_opmode_buffer)
            # Joint 1
            target_joint_1 = -np.pi/4            
            res = vrep.simxSetJointTargetPosition(clientID, h["armJoints"][1], target_joint_1, vrep.simx_opmode_oneshot)            
            res, joint_1 = vrep.simxGetJointPosition(clientID, h["armJoints"][1], vrep.simx_opmode_buffer)
            # Joint 3
            target_joint_3 = 0.
            res = vrep.simxSetJointTargetPosition(clientID, h["armJoints"][3], target_joint_3, vrep.simx_opmode_oneshot)            
            res, joint_3 = vrep.simxGetJointPosition(clientID, h["armJoints"][3], vrep.simx_opmode_buffer)
            # Stop when the robot is at an angle close to -pi/2.
            cond0 = abs(angdiff(joint_0, target_joint_0)) < .001
            cond1 = abs(angdiff(joint_1, target_joint_1)) < .001
            cond3 = abs(angdiff(joint_3, target_joint_3)) < .001
            
            if cond0 & cond1 & cond3:
                fsm = 'compute_target'
                print('Switching to state: ', fsm)
                      
        elif fsm == 'compute_target':
            # Compute arm to ref
            T_arm_ref = get_transform(h["armRef"], h["ref"])
            # Compute the grasp
            # INSERT HERE THE POSITION OF THE TCP
            # Get the gripper position
            [res, tpos] = vrep.simxGetObjectPosition(clientID, h["ptip"], h["armRef"], vrep.simx_opmode_buffer)
            vrchk(vrep, res, True)
            center = np.array([tpos[0], tpos[1] + 0.2, tpos[2] - 0.3])
            # Get the arm tip position. 
            res, tpos = vrep.simxGetObjectPosition(clientID, h["ptip"], h["armRef"], vrep.simx_opmode_buffer)
            vrchk(vrep, res, True)
            # Send the order to move the arm
            res = vrep.simxSetIntegerSignal(clientID, 'km_mode', 2, vrep.simx_opmode_oneshot_wait)
            vrchk(vrep, res, True)
            
            fsm = 'move_arm'
            print('Switching to state: ', fsm)
        
        elif fsm == 'move_arm':
            # Transform for the arm orientation
            rot1 = R.from_quat([0., np.sin(-3/8*np.pi), 0., np.cos(-3/8*np.pi)])
            rot2 = R.from_quat([np.sin(-np.pi/4), 0., 0., np.cos(-np.pi/4)])
            quats = (rot1*rot2).as_quat()
            # Send command to the robot arm
            res = vrep.simxSetObjectQuaternion(clientID, h["otarget"], h["r22"], quats, vrep.simx_opmode_oneshot)
            res = vrep.simxSetObjectPosition(clientID, h["ptarget"], h["armRef"], center, vrep.simx_opmode_oneshot)
            vrchk(vrep, res, True)
            # Get the gripper position and check whether it is at destination (the original position).
            [res, tpos] = vrep.simxGetObjectPosition(clientID, h["ptip"], h["armRef"], vrep.simx_opmode_buffer)
            vrchk(vrep, res, True)
            # Get the gripper orientation and check whether it is at destination (the original position).
            [res, targetori] = vrep.simxGetObjectOrientation(clientID, h["otarget"], h["r22"], vrep.simx_opmode_buffer)
            [res, tori] = vrep.simxGetObjectOrientation(clientID, h["otip"], h["r22"], vrep.simx_opmode_buffer)
            # Check only position but orientation can be added
            cond_pos = np.linalg.norm(tpos - center) < .005
            if cond_pos:
                fsm = 'close_gripper'
                print('Switching to state: ', fsm)
                time_to_close = time.time()
        
        elif fsm == 'close_gripper':
            # Closing the gripper is done by sending 0
            # Opening the gripper is done by sending 1
            res = vrep.simxSetIntegerSignal(clientID, 'gripper_open', 0, vrep.simx_opmode_oneshot_wait);
            vrchk(vrep, res)
            
            if time.time()-time_to_close > 3.:
                fsm = 'lift_up'
                ######### BE CAREFUL #############
                # Don't forget to send a signal to move the robot arm in the forward mode !
                res = vrep.simxSetIntegerSignal(clientID, 'km_mode', 0, vrep.simx_opmode_oneshot_wait)
                vrchk(vrep, res, True)
                print('Switching to state: ', fsm)
                
        elif fsm == "lift_up":
            # Joint 3
            target_joint_3 = 0.
            joint_index = 3
            res = vrep.simxSetJointTargetPosition(clientID, h["armJoints"][joint_index], target_joint_3, vrep.simx_opmode_oneshot)            
            res, joint_3 = vrep.simxGetJointPosition(clientID, h["armJoints"][joint_index], vrep.simx_opmode_buffer)
            # Condition
            cond = abs(angdiff(joint_3, target_joint_3)) < .001
            if cond:
                fsm = "finished"
        
        elif fsm == 'finished':
            print('Finish')
            time.sleep(2)
            break
        else:
            sys.exit('Unknown state ' + fsm)

        # Update wheel velocities.
        h = youbot_drive(vrep, h, forwBackVel, rightVel, rotateRightVel)

        # What happens if you do not update the velocities?
        # The simulator always considers the last speed you gave it,
        # until you set a new velocity.

        # Send a Trigger to the simulator: this will run a time step for the physic engine
        # because of the synchronous mode.
        vrep.simxSynchronousTrigger(clientID)
        vrep.simxGetPingTime(clientID)
    except KeyboardInterrupt:
        cleanup_vrep(vrep, clientID)
        sys.exit('Stop simulation')

cleanup_vrep(vrep, clientID)
print('Simulation has stopped')
