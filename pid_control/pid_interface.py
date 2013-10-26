from __future__ import print_function, absolute_import

# Standard
from multiprocessing import Process, Queue
from time import sleep

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
            'controller': ctrl,
            'process': Process(target=ctrl.StartControl, args=())
        }
        print(dir(self.controllers[interface_name]['process']))
        self.controllers[interface_name]['process'].start()

    def StopController(self, interface_name):
        '''
        '''
        self.controllers[interface_name]['q_input'].put(['Set', '_abort', True])

    def StartController(self, interface_name):
        '''
        '''
        print('restarting...')
        self.controllers[interface_name]['q_input'].put(['Set', '_abort', False])
        sleep(5)
        self.controllers[interface_name]['q_input'].put(['StartControl'])
        print('should be done')
