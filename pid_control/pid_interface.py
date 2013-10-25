from __future__ import print_function, absolute_import

# Standard

# 3rd Party

# Local

class pid_interface
    '''
    '''

    def __init__(self):
        '''
        '''
        self.controllers = {}

    def AddController():
        '''
        '''
        q_in = Queue()
        q_out = Queue()
        ctrl = pid_control(q_in, q_out)
        self.controllers[len(self.controllers)]={
            'q_input': q_in,
            'q_response': q_out,
            'controller': ctrl,
            'process': Process(target=ctrl.StartControl, args())
        }
        self.controllers['process'].start()
