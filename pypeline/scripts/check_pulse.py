#!/usr/bin/python3

from __future__ import absolute_import

# import ..DripInterface


def check_pulse(pype):
    '''
        check for a dripline heartbeat
    '''
    print(pype.CheckHeartbeat())
