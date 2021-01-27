# -*- coding: utf-8 -*-
import numpy as np


def angdiff(angle_1, angle_2):
    """Perform the difference between two angles.

    Parameters
    ----------
    angle_1: (float) an angle in rad[-]
    angle_2: (float) an angle in rad[-]

    Return
    ------
    diff: the difference between 'angle2' and 'angle_1' ]-2pi, 2pi[
    """
    try:
        diff = np.abs(angle_2 - angle_1) % (2*np.pi)
        diff *= (angle_2 - angle_1)/np.abs(angle_2 - angle_1)
    except ZeroDivisionError:
        return 0

    return diff


def get_beacon_distance(vrep, clientID, beacons_handle, youbot_handle):
    """Return the position of the beacons with respect to the youbot.

    Add Gaussian noise to the distance: d ~ N(d_true, std_d)

    Parameters
    ----------
    clientID: (int) the client identification number
    youbot_handle: (int) the youbot identification number

    Return
    ------
    dist: (np.array of shape=(3)), the distance from the youbot to the beacons
    """
    dist = np.zeros(3, dtype=np.float32)
    std = 0.01  # Error of ~1cm
    # Loop
    for i, beacon in enumerate(beacons_handle):
        # Get the position (x, y, z)
        res, beacon_pos = vrep.simxGetObjectPosition(clientID, beacon,
                                                     youbot_handle["ref"],
                                                     vrep.simx_opmode_streaming)
        # Get the noisy distance
        dist[i] = np.linalg.norm(beacon_pos[0:2]) + np.random.default_rng().normal(0, std)

    return dist
