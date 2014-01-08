'''
    Mantis uses a client/server model to control signal digitization systems. Being purely software, the interface to that client should be taken care of directly by pypeline, without a dripline translation layer.

    The DripResponse object does not apply but equivalent behavior is desired.
'''

from __future__ import print_function, absolute_import
from datetime import datetime, timedelta
from subprocess import Popen
from shlex import split
from uuid import uuid4
from glob import glob
from json import dump

class MantisResponse():
    '''
    '''


    def __init__(self):
        '''
            
        '''
        self.mantis_client = None
        self.conf_dict = {"data-chunk-size": 1024,
                             "digitizer": "px1500",
                             "buffer-size": 512,
                             "record-size": 4194304,
                             "port": 98342
        }
        pass

    def Run(self):
        '''
        '''
        #should use <something> = subprocess.Popen(shlex.split(<command_string>),
        #                                          stdout=<some_file_object>)
        ####### deal with files
        status_files = glob('/tmp/mantis_client_*.status')
        out_file_name = '/tmp/mantis_client_' + uuid4().hex[0:8] + '.status'
        while out_file_name in statusfiles:
            out_file_name = '/tmp/mantis_client_' + uuid4().hex[0:8] + '.status'
        self.out_file_name = out_file_name
        self.out_file = open(out_file_name, 'w')
        self.reading_file = open(out_file_name, 'r')
        conf_file = open('/tmp/mantis_client_conf.json','w')
        dump(self.conf_dict, conf_file, indent=4)
        conf_file.flush()
        conf_file.close()

        ####### build the execution string
        client_exe = '/home/laroque/Repos/mantis/cbuild/bin/mantis_client'
        self.mantis_client = Popen(split(client_exe + 'config=/tmp/mantis_client_conf.json'),
                                   stdout=out_file_name)

    def Update(self):
        '''
        '''
        #This should read the file to which output is being redirected and determine the status,
        #should also see if the client process has been started and if so, if it is finished
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
                if not self.Waiting():
                    finished = self.mantis_client.returncode
                    break
        return finished
