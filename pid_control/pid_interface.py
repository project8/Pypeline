#!/bin/python2
from __future__ import print_function, absolute_import

# Standard
from multiprocessing import Process, Queue
from time import sleep
from types import MethodType

# 3rd Party

# Local
from .pid_controller import pid_controller

class pid_interface:
    '''
    '''

    def __init__(self):
        '''
        '''
        self.controllers = {}

    def AddController(self, interface_name):
        '''
        '''
        q_in = Queue()
        q_out = Queue()
        ctrl = pid_controller(q_in, q_out)
        self.controllers[interface_name]={
            'q_input': q_in,
            'q_response': q_out,
            'controller': ctrl
        }
        self._StartLoop(interface_name)

    def _StartLoop(self, interface_name):
        '''
        '''
        print('starting...')
        self.controllers[interface_name]['process'] = Process(
            target=self.controllers[interface_name]['controller'].StartControl, args=())
        print(dir(self.controllers[interface_name]['process']))
        self.controllers[interface_name]['process'].start()
        sleep(5)
        print('should be done')

    def Abort(self, interface_name):
        '''
        '''
        self.controllers[interface_name]['process'].terminate()

    def Start(self, interface_name):
        '''
        '''
        qitem = ['Set', '_controlling', True]
        self.controllers[interface_name]['q_input'].put(qitem)

    def Stop(self, interface_name):
        '''
        '''
        qitem = ['Set', '_controlling', False]
        self.controllers[interface_name]['q_input'].put(qitem)

    def Set(self, interface_name=None, attribute=None, value=None):
        '''
        '''
        try:
            value = float(value)
        except:
            pass
        if not interface_name:
            print('valid interfaces are:')
            print(self.controllers.keys())
            return self.controllers.keys()
        elif not attribute:
            print('valid attributes are:')
            members = [mbr for mbr in dir(self.controllers[interface_name]['controller']) if not mbr.startswith('_')]
            print(members)
            members = [mbr for mbr in members if not\
                isinstance(getattr(self.controllers[interface_name]['controller'], mbr), MethodType)]
            return members
        elif not value:
            print('a value is required')
        self.controllers[interface_name]['q_input'].put(['Set', attribute, value])
