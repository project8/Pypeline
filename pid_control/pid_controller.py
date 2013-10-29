from __future__ import print_function, absolute_import

# Standard
from multiprocessing import Process, Queue
from time import sleep
from datetime import datetime, timedelta
import types

# 3rd party

# Local
from pypeline import DripInterface


class pid_controller:
    '''
    '''

    def __init__(self, input_q, response_q):
        '''
        '''
        #internal vars
        self.filename = open('/tmp/tempstatus.txt','a')
        self.filename.write('again....\n')
        self.filename.flush()
        self.input_queue = input_q
        self.response_queue = response_q
        self.pype = DripInterface('http://myrna.phys.washington.edu:5984')
        self.last_current = 0

        #adjustable attributes
        self.min_update_time = timedelta(seconds=10)
        self.max_history = 20 
        self.target_temp = 4
        self.temp_channel = ''
        self.Kproportional = 0
        self.Kintegral = 0
        self.Kdifferential = 0

    def StartControl(self):
        '''
        '''
        self.filename.write('... prep main loop...\n')
        self.filename.flush()
        self.time_stamps = []
        self.temperatures = []
        self.deltas = []
        self._UpdateValues()
        self.filename.write('... starting main loop...\n')
        self.filename.flush()
        while True:
            if not self.input_queue.empty():
                self._QueueResponse(self.input_queue.get())
            else:
                if (datetime.now() - self.time_stamps[-1]) > self.min_update_time:
                    self._UpdateValues()
                    self.filename.write(str(self.time_stamps[-1]) + ': ')
                    self.filename.write(str(self.temperatures[-1]))
                    self.filename.write(' -> ' + str(self.deltas[-1]) + '\n')
                    self.filename.flush()
                else:
                    sleep(2)

    def _UpdateValues(self):
        '''
        '''
        if len(self.time_stamps) >= self.max_history:
            self.time_stamps.pop(0)
            self.temperatures.pop(0)
            self.deltas.pop(0)

        self.time_stamps.append(datetime.now())
        temp_doc = self.pype.Get('terminator_temp').Wait()
        assert temp_doc['final'].split()[1] == 'K', 'No valid dripline response'
        self.temperatures.append(float(temp_doc['final'].split()[0]))
        self.deltas.append(self.target_temp - self.temperatures[-1])

    def _PIDAdjust(self):
        '''
        '''
        P = self.Kproportional * self.deltas[-1]
        I = self.Kintegral 

    def Set(self, name, value):
        '''
            call setattr (for queue command access)
        '''
        self.response_queue.put(['setting', name, 'to', value])
        setattr(self, name, value)

    def _QueueResponse(self, q_item):
        '''
        '''
        attr = getattr(self, q_item[0])
        if isinstance(attr, types.MethodType):
            self.response_queue.put(['calling method'])
            self.response_queue.put(attr(*q_item[1:]))
            self.response_queue.put(['method call complete'])
        else:
            print('getting attr')
            self.response_queue.put(attr)
            print('attr put')
