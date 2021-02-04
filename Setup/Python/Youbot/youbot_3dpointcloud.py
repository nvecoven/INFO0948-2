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
from mpl_toolkits.mplot3d import Axes3D

from cleanup_vrep import cleanup_vrep
from vrchk import vrchk
from youbot_init import youbot_init
from youbot_hokuyo_init import youbot_hokuyo_init
from youbot_hokuyo import youbot_hokuyo
from youbot_xyz_sensor import youbot_xyz_sensor

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

vrep.simxSynchronousTrigger(clientID)
vrep.simxGetPingTime(clientID)

# Ask the sensor to turn itself on, take A SINGLE POINT CLOUD, and turn itself off again. 
# ^^^     ^^^^^^                ^^       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# simxSetIntegerSignal          1        simx_opmode_oneshot_wait
#         |
#         handle_xyz_sensor
res = vrep.simxSetIntegerSignal(clientID, 'handle_xyz_sensor', 1, vrep.simx_opmode_oneshot_wait)
vrchk(vrep, res)

vrep.simxSynchronousTrigger(clientID)
vrep.simxGetPingTime(clientID)

# Then retrieve the last point cloud the depth sensor took.
# If you were to try to capture multiple images in a row, try other values than 
# vrep.simx_opmode_oneshot_wait. 
print('Capturing point cloud...\n');
pts = youbot_xyz_sensor(vrep, h, vrep.simx_opmode_oneshot_wait)


vrep.simxSynchronousTrigger(clientID)
vrep.simxGetPingTime(clientID)
# Each column of pts has [x;y;z;distancetosensor]. However, plot3 does not have the same frame of reference as 
# the output data. To get a correct plot, you should invert the y and z dimensions. 

# Plot all the points. 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(pts[:, 0], pts[:, 2], pts[:, 1], marker="*")

# Plot the points of the wall (further away than 1.87 m, which is determined either in the simulator by measuring 
# distances or by trial and error) in a different colour. This value is only valid for this robot position, of
# course. This simple test ignores the variation of distance along the wall (distance between a point and several
# points on a line). 
#pts_wall = pts[pts[:, 3] >= 1.87]
#ax.scatter(pts_wall[:, 0], pts_wall[:, 2], pts_wall[:, 1], marker="+")

plt.show()

cleanup_vrep(vrep, clientID)
print('Simulation has stopped')
