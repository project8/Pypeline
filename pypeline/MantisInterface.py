'''
    Mantis uses a client/server model to control signal digitization systems. Being purely software, the interface to that client should be taken care of directly by pypeline, without a dripline translation layer.

    The DripResponse object does not apply but equivalent behavior is desired.
'''

from __future__ import print_function, absolute_import
from datetime import datetime, timedelta

class MantisResponse():
    '''
    '''


    def __init__(self, kwargs={}):
        '''
            
        '''
        self.mantis_client = None
        pass

    def Update(self):
        '''
        '''
        pass

    def Waiting(self):
        '''
        '''
        return if self.mantis_client.poll() is None

    def Wait(self, timeout=60):
        '''
        '''
        finished = False
        if not isinstance(timeout, timedelta):
            timeout = timedelta(seconds=timeout)
        if self.mantis_client is None:
            finished = "Mantis not started"
        else:
            finished = "Mantis still running"
            start = datetime.now()
            while (datetime.now() - start) < timeout:
                if not self.mantis_client.poll() is None:
                    finished = self.mantis_client.returncode
