#!/usr/bin/python
'''
    A script which should:
        1) Set some channel(s)
        2) Start a short digitizer run
        3) Monitor some channel(s) while the digitizer is running
        4) Report some sort of feedback
'''

from Pypeline import DripInterface
import time

drip = DripInterface('http://p8portal.phys.washington.edu:5984')

drip.Set('test_6v', '0.25V')
short_run = drip.Run(duration=250, rate=500, filename=None)

valve_temps = []
while short_run.Waiting():
    print('status check')
    dum_temp = drip.Get('pump_valve_t')
    dum_temp.Wait()
    print(dum_temp['result'])
    valve_temps.append(dum_temp)
    time.sleep(3)

print('run doc is: ' + str(short_run['_id']))
print('final status was: ' + str(short_run['result']))
