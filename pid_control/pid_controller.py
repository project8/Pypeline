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
        self.target_temp = 75.
        self.temp_channel = 'terminator_temp'
        self.current_channel = ''
        self.Kproportional = 1./40.
        self.Kintegral = 1./40./200.
        self.Kdifferential = 1./40./200./50.
        self.max_current = 1.0
        self.min_current_change = 0.001

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
                    self._PIDAdjust()
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
        I = (self.Kintegral / len(self.deltas)) *\
            (self.time_stamps[-1] - self.time_stamps[0]).seconds *\
            (0.5 * (self.deltas[0] + self.deltas[-1]) + sum(self.deltas[1:-1]))
        D = self.Kdifferential * (self.deltas[-1] - self.deltas[-2]) /\
            (self.time_stamps[-1] - self.time_stamps[-2]).seconds
        new_current = self.last_current + current_change
        if new_current > self.max_current:
            new_current = self.max_current
        if new_current < 0.:
            new_current = 0
        self.filename.write('P->' + str(P) + '\n')
        self.filename.write('I->' + str(I) + '\n')
        self.filename.write('D->' + str(D) + '\n')
        self.filename.write('New Current: ' + str(new_current) + '\n')
        self.filename.flush()
        if abs(new_current - self.last_current) < self.min_current_change:
            self.filename.write('current change is small, not changing')
        else:
            self.filename.write('would set the dripline current channel.. if ready')
            self.filename.flush()
            #self.pype.Set(self.current_channel, str(new_current) + ' A')

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
