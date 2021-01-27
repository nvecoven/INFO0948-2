# -*- coding: utf-8 -*-
import numpy as np

def angdiff(angle_1, angle_2):
    """
    Perform the difference between 'angle_2' and 'angle_1'
    
    Parameters
    ----------
    angle_1: an angle in rad[-]
    angle_2: an angle in rad[-]
    
    Return
    ------
    diff: the difference between 'angle2' and 'angle_1' ]-2pi, 2pi[
    """
    try:
        diff = abs(angle_2 - angle_1)%(2*np.pi)
        diff *= (angle_2 - angle_1)/abs(angle_2 - angle_1)
    except ZeroDivisionError:
        return 0
    
    return diff