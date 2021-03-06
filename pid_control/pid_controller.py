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
        self._outfile = open('/tmp/tempstatus.txt','w')
        self._outfile.write('~Initializing controller @ ')
        self._outfile.write(str(datetime.now()) + str('\n'))
        self._outfile.flush()
        self._input_queue = input_q
        self._response_queue = response_q
        self._pype = DripInterface('http://myrna.phys.washington.edu:5984')
        self._last_current = 0
        self._controlling = False

        self.SetDefaults()

    def SetDefaults(self):  
        '''
        '''
        self.min_update_time = timedelta(seconds=1)
        self.max_history = 40 
        self.target_temp = 75.
        self.temp_channel = 'terminator_temp'
        self.current_channel = 'terminator_heater_current'
        self.Kproportional = 0.005
        self.Kintegral = 0.0002
        self.Kdifferential = 3.0
        self.max_current = 1.0
        self.min_current_change = 0.001

    def StartControl(self):
        '''
        '''
        self._outfile.write('~prep main loop...\n')
        self._outfile.flush()
        self.time_stamps = []
        self.temperatures = []
        self.deltas = []
        self._outfile.write('~starting main loop...\n')
        self._outfile.flush()
        last_update = datetime.now()
        while True:
            if not self._input_queue.empty():
                self._QueueResponse(self._input_queue.get())
                continue
            elif self._controlling and ((datetime.now() - last_update)\
                                        > self.min_update_time):
                last_update = datetime.now()
                self._UpdateValues()
                self._PIDAdjust()
                self._outfile.write(str(self.time_stamps[-1]) + ': ')
                self._outfile.write(str(self.temperatures[-1]))
                self._outfile.write(' -> ' + str(self.deltas[-1]) + '\n')
                self._outfile.flush()
            sleep(1)

    def Start(self):
        self._UpdateValues()
        sleep(1)
        self._controlling = True

    def Stop(self):
        self.time_stamps = []
        self.temperatures = []
        self.deltas = []
        self._controlling = False

    def _UpdateValues(self):
        '''
        '''
        if len(self.time_stamps) >= self.max_history:
            self.time_stamps.pop(0)
            self.temperatures.pop(0)
            self.deltas.pop(0)

        self.time_stamps.append(datetime.now())
        temp_doc = self._pype.Get(self.temp_channel).Wait()
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
        D = 0
        if len(self.time_stamps) > 2:
            D = self.Kdifferential * (self.deltas[-1] - self.deltas[-2]) /\
                (self.time_stamps[-1] - self.time_stamps[-2]).seconds
        current_change = P + I + D
        new_current = self._last_current + current_change
        if new_current > self.max_current:
            new_current = self.max_current
        if new_current < 0.:
            new_current = 0
        self._outfile.write('P->' + str(P) + '\n')
        self._outfile.write('I->' + str(I) + '\n')
        self._outfile.write('D->' + str(D) + '\n')
        self._outfile.flush()
        if abs(new_current - self._last_current) < self.min_current_change:
            self._outfile.write('current change is small, not changing \n')
        else:
            self._outfile.write('setting current to ' + str(new_current) + '\n')
            self._outfile.flush()
            self._pype.Set(self.current_channel, str(new_current) + 'A')
            self._last_current = new_current

    def Set(self, name, value):
        '''
            call setattr (for queue command access)
        '''
        self._response_queue.put(['setting', name, 'to', value])
        self._outfile.write('setting ' + str(name) + ' to ' + str(value) + '\n')
        self._outfile.flush()
        setattr(self, name, value)

    def _QueueResponse(self, q_item):
        '''
        '''
        attr = getattr(self, q_item[0])
        if isinstance(attr, types.MethodType):
            self._response_queue.put(['calling method'])
            self._response_queue.put(attr(*q_item[1:]))
            self._response_queue.put(['method call complete'])
        else:
            print('getting attr')
            self._response_queue.put(attr)
            print('attr put')
