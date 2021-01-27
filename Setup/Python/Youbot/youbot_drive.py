# -*- coding: utf-8 -*-
import numpy as np

from vrchk import vrchk


def youbot_drive(vrep, h, forwBackVel, leftRightVel, rotVel):
    # Sets the youBot wheel speed to achieve the given forward, lateral
    # and rotational velocities. The velocities are normalized to say
    # within the bounds of the actuator capabilities.
    
    # (C) Copyright Renaud Detry 2013, Norman Marlier 2019.
    # Distributed under the GNU General Public License.
    # (See http://www.gnu.org/copyleft/gpl.html)
    
    ## Physical limits of the youBot. 
    pParam = 20
    maxV = 12
    pParamRot = 10
    maxVRot = 4
    accelF = 0.05
    
    ## Compute the velocities. 
    forwBackVel = forwBackVel * pParam
    leftRightVel = leftRightVel * pParam
    
    # Ensure the velocities are within the acceptable physical range. 
    v = np.sqrt(forwBackVel * forwBackVel + leftRightVel * leftRightVel)
    if v > maxV:
        forwBackVel = forwBackVel * maxV / v
        leftRightVel = leftRightVel * maxV / v
    
    rotVel = rotVel * pParamRot
    if np.abs(rotVel) > maxVRot:
        rotVel = maxVRot * rotVel / np.abs(rotVel)

    
    ## Compute the accelerations for each velocity. 
    df = forwBackVel - h['previousForwBackVel']
    ds = leftRightVel - h['previousLeftRightVel']
    dr = rotVel - h['previousRotVel']
    
    # Ensure the accelerations are within the acceptable physical range. 
    if np.abs(df) > maxV * accelF:
        df = np.sign(df) * maxV * accelF
    
    if np.abs(ds) > maxV * accelF:
        ds = np.sign(ds) * maxV * accelF
    
    if np.abs(dr) > maxVRot * accelF:
        dr = np.sign(dr) * maxVRot * accelF
    
    ## Update the robot velocities. 
    # Compute the new velocities based on the acceleration. 
    forwBackVel = h['previousForwBackVel'] + df
    leftRightVel = h['previousLeftRightVel'] + ds
    rotVel = h['previousRotVel'] + dr
    
    # Store the new velocities as the previous ones. 
    h['previousForwBackVel'] = forwBackVel
    h['previousLeftRightVel'] = leftRightVel
    h['previousRotVel'] = rotVel
    
    # Communicate the new wheel velocities to the simulator.
    res = vrep.simxPauseCommunication(h['id'], True)
    vrchk(vrep, res)
    res = vrep.simxSetJointTargetVelocity(h['id'], h['wheelJoints'][0],
            - forwBackVel - leftRightVel + rotVel, vrep.simx_opmode_oneshot)
    vrchk(vrep, res)
    res = vrep.simxSetJointTargetVelocity(h['id'], h['wheelJoints'][1],
            - forwBackVel + leftRightVel + rotVel, vrep.simx_opmode_oneshot) 
    vrchk(vrep, res)
    res = vrep.simxSetJointTargetVelocity(h['id'], h['wheelJoints'][2],
            - forwBackVel - leftRightVel - rotVel, vrep.simx_opmode_oneshot)
    vrchk(vrep, res)
    res = vrep.simxSetJointTargetVelocity(h['id'], h['wheelJoints'][3],
            - forwBackVel + leftRightVel - rotVel, vrep.simx_opmode_oneshot) 
    vrchk(vrep, res)
    res = vrep.simxPauseCommunication(h['id'], False) 
    vrchk(vrep, res)
    
    return h