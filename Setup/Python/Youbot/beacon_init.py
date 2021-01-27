# -*- coding: utf-8 -*-
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
    
    

