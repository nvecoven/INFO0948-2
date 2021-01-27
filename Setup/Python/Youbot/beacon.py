# -*- coding: utf-8 -*-
import numpy as np
from vrchk import vrchk


def beacon_init(vrep, clientID):
    """Create a handle for beacons."""
    beacons = [0]*3
    # Load the handle
    res, beacons[0] = vrep.simxGetObjectHandle(clientID, 'Beacon1', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    res, beacons[1] = vrep.simxGetObjectHandle(clientID, 'Beacon2', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    res, beacons[2] = vrep.simxGetObjectHandle(clientID, 'Beacon3', vrep.simx_opmode_oneshot_wait)
    vrchk(vrep, res)
    
    return beacons

def get_beacon_distance(vrep, clientID, beacons_handle, youbot_handle, flag):
    """Return the position of the beacons with respect to the youbot.

    Add Gaussian noise to the distance: d ~ N(d_true, std_d)

    Parameters
    ----------
    vrep: the vrep simulator
    clientID: (int) the client identification number
    beacons_handle: (list of int) the beacons identification numbers
    youbot_handle: (int) the youbot identification number
    flag: (bool) If true, impose a constraint on the range of the beacon.

    Return
    ------
    dist: (np.array of shape=(3)), the distance from the youbot to the beacons
            If the beacon is to far, return np.nan
    """
    dist = np.zeros(3, dtype=np.float32)
    std = 0.01  # Error of ~1cm
    radius = 5.  # Range of the beacon
    # Loop
    for i, beacon in enumerate(beacons_handle):
        # Get the position (x, y, z)
        res, beacon_pos = vrep.simxGetObjectPosition(clientID, beacon,
                                                     youbot_handle["ref"],
                                                     vrep.simx_opmode_streaming) 
        # Get the noisy distance 
        dist[i] = np.linalg.norm(beacon_pos) + np.random.default_rng().normal(0, std)
    # If the range is take into account
    if flag:
        dist[dist > radius] = np.nan
    return dist
    
    

