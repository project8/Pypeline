from __future__ import print_function, absolute_import

# Standard
from multiprocessing import Process, Queue
from time import sleep

# 3rd party

# Local


class pid_gremlin:
    '''
    '''

    def __init__(self, q):
        '''
        '''
        q.put(':-)')

def start_gremlin(q):
    '''
    '''
    q.put([':)'])
    grem = pid_gremlin(q)


if __name__ == '__main__':
    q = Queue()
    p = Process(target=start_gremlin, args=(q,))
    p.start()
    sleep(2)
    print(q.empty())
    while not q.empty():
        print(q.get())
    print('got no more gets')
    p.join()
