from __future__ import print_function, absolute_imports
from sys import version_info
inpy3 = not version_info[0] < 3

# Standard
# 3rd party
# Local
from ..pypeline import DripInterface


class pid_gremlin:
    '''
        A class to handle software controlled temperature stabilization via heater adjustment.
    '''


    def __init__():
        '''
            Set default values
        '''
        self.abort_T = 500. # in K
        self.panic_T = 450. # in K
        self.goal_T = False # needs to be set, in K

        self.pype = DripInterface('http://myrna.phys.washington.edu:5984')
        self.reading_channel = False # give me a temperature sensor
        self.setting_channel = False # give me a heater
        self.last_set = False
        self.max_readings = 50
        self.readings = []

    def TempToK(value, units='C'):
        '''
            Convert a temperature to Kelvin
        '''
        if units == 'F':
            print('Did you really use Fahrenheit?\n\n
                   You know that this is science right?')
            value = (5./9.)*(value-32.)
            units = 'C'
        if units == 'C':
            value = value - 273.15
            units = 'K'
        if not units == 'K':
            print('what kind of units are', units, '?')
        else:
            return value

    def GetReading():
        '''
            Update the list of Readings with the current value.
        '''
        reading = self.pype.Get(self.reading_channel).Wait()
        if not len(self.readings) < self.max_readings:
            self.readings.pop(0)
        self.readings.append((reading['timestamp'],
                              TempToK(reading['final'].split())))

    def UpdateCurrent():
        '''
            Call algorithm to get new setting and pype.Set() that value
        '''
        self.GetReading()
        if not self.last_set:
            self.last_set = self.pype.Get(self.setting_channel)['final']
        #some call that computes the needed change to the current
        if not self.pype.Set(self.setting_channel, new_cur).Wait()['final'] == 'ok'
            raise ValueError('failed to set current')
        self.last_set = new_cur
