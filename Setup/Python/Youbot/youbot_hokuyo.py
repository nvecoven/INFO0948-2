# -*- coding: utf-8 -*-
import numpy as np

def youbot_hokuyo(vrep, h, opmode, trans=None):
    # Reads from Hokuyo sensor.
    
    # (C) Copyright Renaud Detry 2013, Norman Marlier 2019.
    # Distributed under the GNU General Public License.
    # (See http://www.gnu.org/copyleft/gpl.html)
    
    if trans is not None:
        t1 = trans*h['hokuyo1Trans']
        t2 = trans*h['hokuyo2Trans']
    else:
        t1 = h['hokuyo1Trans']
        t2 = h['hokuyo2Trans']
      
    
    # The Hokuyo data comes in a funny format. Use the code below to move it
    # to a Matlab matrix
    res, det, auxData = vrep.simxReadVisionSensor(h['id'], h['hokuyo1'], opmode)
    if res == 0:
        width = int(auxData[1][0])
        height = int(auxData[1][1])
        pts1 = np.reshape(auxData[1][2:], (width*height, 4))
        # Each column of pts1 has [x;y;z;distancetosensor]
        # The Hokuyo sensor has a range of 5m. If there are no obstacles, a point
        # is returned at the 5m limit. As we do not want these points, we throw
        # away all points that are 5m far from the sensor.
        obst1 = pts1[:, 3] < 4.9999
        pts1 = pts1[:, 0:3]
    else:
        return [], []
    
    # Process the other 120 degrees      
    res, det, auxData = vrep.simxReadVisionSensor(h['id'], h['hokuyo2'], opmode)
    if res == 0:    
        width = int(auxData[1][0])
        height = int(auxData[1][1])
        pts2 = np.reshape(auxData[1][2:], (width*height, 4))
        obst2 = pts2[:, 3] < 4.9999
        pts2 = pts2[:, 0:3]
    else:
        return [], []
        
    # Translate the points in the repere of the Hokuyo
    pts_1 = np.ones((pts1.shape[0], pts1.shape[1]+1)); pts_1[:,:-1] = pts1
    pts_2 = np.ones((pts2.shape[0], pts2.shape[1]+1)); pts_2[:,:-1] = pts2
    pts1 = t1*pts_1.T
    pts2 = t2*pts_2.T
      
    scanned_points = np.vstack((pts1[:-1, :], pts2[:-1, :]))
    contacts = np.vstack((obst1, obst2))

    return scanned_points, contacts