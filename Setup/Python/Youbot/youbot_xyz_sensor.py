"""
Read from xyz sensor.

% (C) Copyright Renaud Detry 2013, Norman Marlier 2021
% Distributed under the GNU General Public License.
% (See http://www.gnu.org/copyleft/gpl.html)

"""
import numpy as np
from vrchk import vrchk


def youbot_xyz_sensor(vrep, youbot_handle, opmode):
    """Get the xyz data from the depth camera.

    Parameters
    ----------
    -vrep: the vrep simulator
    -youbot_handle: (int) the youbot identification number
    -opmode: a vrep mode function

    Return
    ------
    -pts: (np.array (nb_pts, 4)), the 3D point cloud (x, y, z, distance)
    """
    res, det, auxData = vrep.simxReadVisionSensor(youbot_handle["id"],
                                                                 youbot_handle["xyzSensor"],
                                                                 opmode)
    vrchk(vrep, res, True)
    print(auxData[1])
    width = int(auxData[1][0])
    height = int(auxData[1][1])
    pts = np.reshape(auxData[1][2:], (width*height, 4))
    # Each column of pts has [x;y;z;distancetosensor]
    pts = pts[(pts[:, 3] < 4.9999).ravel(), :]

    return pts
