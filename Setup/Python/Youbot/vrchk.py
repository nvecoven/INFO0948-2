# -*- coding: utf-8 -*-
import sys

def vrchk(vrep, res, buffer=False):
    # Checks VREP return code. Set buffer to 1 if you are reading from a buffered
    #call.
    
    # (C) Copyright Renaud Detry 2013, Norman Marlier 2019.
    # Distributed under the GNU General Public License.
    # (See http://www.gnu.org/copyleft/gpl.html)

      
    expl = 'Undefined error';
      
    if res == vrep.simx_error_noerror:
        # Nothing to say
        return
    elif res == vrep.simx_error_novalue_flag:
        if buffer:
        #    No problem to report
            return
        else:
            expl = 'There is no command reply in the input buffer. This should not always be considered as an error, depending on the selected operation mode';
    
    elif res == vrep.simx_error_timeout_flag:
        expl = 'The function timed out (probably the network is down or too slow)'
    elif res == vrep.simx_error_illegal_opmode_flag:
        expl = 'The specified operation mode is not supported for the given function'
    elif res == vrep.simx_error_remote_error_flag:
        expl = 'The function caused an error on the server side (e.g. an invalid handle was specified)'
    elif res == vrep.simx_error_split_progress_flag:
        expl = 'The communication thread is still processing previous split command of the same type'
    elif res == vrep.simx_error_local_error_flag:
        expl = 'The function caused an error on the client side'
    elif res == vrep.simx_error_initialize_error_flag:
        expl = 'simxStart was not yet called'
    
    sys.exit('Remote API function call returned with error code: ' + str(res) + '. Explanation: ' + expl)
    