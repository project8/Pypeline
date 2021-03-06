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

class MantisInterface():
    '''
    '''


    def __init__(self):
        '''
            
        '''
        self.mantis_client = None
        self.conf_dict = {}
        self.actions = []
        self.errors = []

    def Run(self, conf_dict={}):
        '''
        '''
        #should use <something> = subprocess.Popen(shlex.split(<command_string>),
        #                                          stdout=<some_file_object>)
        self.conf_dict.update(conf_dict)
        ####### deal with files
        status_files = glob('/tmp/mantis_client_*.status')
        out_file_name = '/tmp/mantis_client_' + uuid4().hex[0:8] + '.status'
        while out_file_name in status_files:
            out_file_name = '/tmp/mantis_client_' + uuid4().hex[0:8] + '.status'
        self.out_file_name = out_file_name
        self.out_file = open(out_file_name, 'w')
        self.reading_file = open(out_file_name, 'r')
        conf_file = open('/tmp/mantis_client_conf.json','w')
        dump(self.conf_dict, conf_file, indent=4)
        conf_file.flush()
        conf_file.close()

        ####### build the execution string
        client_exe = 'mantis_client'
        try:
            self.mantis_client = Popen(split(client_exe + ' config="/tmp/mantis_client_conf.json"'),
                                   stdout=self.out_file,
                                   stderr=self.out_file)
        except OSError:
            raise EnvironmentError("the mantis_client executable is likely not being found")
        #print(client_exe + ' config=/tmp/mantis_client_conf.json')
        return self

    def GetConf(self, param=None):
        '''
        '''
        print(self.conf_dict)
        if not param is None:
            ret_val = self.conf_dict[param]
        else:
            ret_val = self.conf_dict
        return ret_val

    def Update(self):
        '''
        '''
        which_list = self.actions
        if not isinstance(self.mantis_client, Popen):
            ret_val = 'client not started'
        else:
            line = self.reading_file.readline()
            while not line == '':
                if line.startswith('\033[1;32m'):
                    which_list = self.actions
                    which_list.append([line])
                elif line.startswith('\033[1;21m'):
                    which_list = self.errors
                    which_list.append([line])
                else:
                    self.actions[-1].append(line)
                line = self.reading_file.readline()
            ret_val = self.actions[-1]
        return ret_val

    def Waiting(self):
        '''
        '''
        return self.mantis_client.poll() is None

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
