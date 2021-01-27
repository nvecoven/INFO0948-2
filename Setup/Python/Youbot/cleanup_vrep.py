# -*- coding: utf-8 -*-


def cleanup_vrep(vrep, id):
  print('Closing connection' + str(id))
  vrep.simxStopSimulation(id, vrep.simx_opmode_oneshot_wait)
  vrep.simxFinish(id)
  print('Program ended')


# (C) Copyright Renaud Detry 2013, Norman Marlier 2019.
# Distributed under the GNU General Public License.
# (See http://www.gnu.org/copyleft/gpl.html)