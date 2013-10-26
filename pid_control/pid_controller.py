from __future__ import print_function, absolute_import

# Standard
from multiprocessing import Process, Queue
from time import sleep
from datetime import datetime, timedelta
import types

# 3rd party

# Local


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
        self.time_stamps = [datetime.now()]
        self.input_queue = input_q
        self.response_queue = response_q
        self._abort = False

        #adjustable attributes
        self.min_update_time = timedelta(seconds=10)
        self.max_times = 10

    def StartControl(self):
        '''
        '''
        self.filename.write('... starting main loop...\n')
        self.filename.flush()
        while not self._abort:
            if self.input_queue.empty():
                if (datetime.now() - self.time_stamps[-1]) > self.min_update_time:
                    self._UpdateCurrent()
                    self.filename.write(str(self.time_stamps[-1]) + '\n')
                    self.filename.flush()
                else:
                    sleep(2)
            else:
                self._QueueResponse(self.input_queue.get())

    def Set(self, name, value):
        '''
            call setattr (for queue command access)
        '''
        self.response_queue.put(['setting', name, 'to', value])
        setattr(self, name, value)

    def _UpdateCurrent(self):
        '''
        '''
        if len(self.time_stamps) >= self.max_times:
            self.time_stamps.pop(0)
        self.time_stamps.append(datetime.now())

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

if __name__ == '__main__':
    q_in = Queue()
    q_out = Queue()
    print('starting')
    grem = pid_control(q_in, q_out)
    p = Process(target=grem.StartControl, args=())
    p.start()
    sleep(120)
    print('setting min update time')
    q_in.put(['Set', 'min_update_time', timedelta(seconds=5)])
    sleep(3)
    print('supposedly set')
    q_in.put(['min_update_time'])
    sleep(20)
    while not q_out.empty():
        print(q_out.get())
        sleep(3)
    sleep(2)
    print('done')
    p.join()
