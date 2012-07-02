'''
    File for the pypeline class. At least for now I suspect this entire project goes in one class, if that changes it will need to be split into more files.
'''

from time import sleep
from uuid import uuid4
from couchdb import Server as CouchServer
from DripResponse import DripResponse

class DripInterface:
    '''
        Class to interact with Dripline via couchDB.
    '''

    def __init__(self, dripline_url="http://127.0.0.1:5984"):
        '''
            Initializes an instance of pypeline by connecting to the server.
    
            Inputs:
                <dripline_url> is the url to use when connecting to the couchDB server,
                if none is provided then the default (http://127.0.0.1:5984/).
        '''
        self._server = CouchServer(dripline_url)
        self._timeout = 15 #timeout is 15 seconds...
        self._sleep_time = .1 #number of seconds to sleep while waiting
        self._wait_state = {}
        if (self._server.__contains__('dripline_cmd')):
            self._cmd_database = self._server['dripline_cmd']
        else:
            raise UserWarning('The dripline command database was not found!')
        self.CheckHeartbeat()

    def Get(self, channel):
        '''
            Request and return the current value of some channel.

            Inputs:
                <channel> must be an active channel in dripline.
        '''
        result = DripResponse(self._cmd_database, uuid4().hex)
        get_doc = {
            '_id':result['_id'],
            'type':'command',
            'command':{
                "do":"get",
                "channel":channel,
            },
        }
        self._cmd_database.save(get_doc)
        result.Update()
        return result

    def Set(self, channel, value, check=False,):
        '''
            Change the setting of a dripline channel

            Inputs:
                <channel> must be an active channel in dripline
                <value> value to assign to <channel>
                <check> uses Get() to check the value,
                        WARNING: this doesn't deal with machine rounding
            
            WARNING! I do not yet check to ensure setting of the correct type.
        '''
        result = DripResponse(self._cmd_database, uuid4().hex)
        set_doc = {
            '_id':result['_id'],
            'type':'command',
            'command':{
                "do":"set",
                "channel":channel,
                "value":str(value),
            },
        }
        self._cmd_database.save(set_doc)
        result.Update()
        return result

    def Run(self, durration=250, rate=500, filename=None):
        '''
            Take a digitizer run of fixed time and sample rate.

            Inputs:
                <durration> is the time interval (in ms) that will be digitized
                <rate> is the sample rate (in MHz) of the digitizer
                <filename> is the file on disk where the data will be written
                           [=None] results in a uuid4().hex hash prefix and .egg extension
                           NOTE: you should probably just take the default unless you have
                           a good reason not to do so.
        '''
        result = DripResponse(self._cmd_database, uuid4().hex)
        if not filename:
            filename = '/data/' + uuid4().hex + '.egg'
        run_doc = {
            '_id':result['_id'],
            'type':'command',
            'command':{
                "do":"run",
                "durration":str(durration),
                "rate":str(rate),
                "output":filename,
            },
        }
        self._cmd_database.save(run_doc)
        result.Update()
        return result

    def SetDefaultTimeout(self, duration):
        '''
            Change how long a get will look for changes before timeout.a
        '''
        if duration < 0:
            raise ValueError('timeout must be >= 0')
        self._timeout = duration

    def CheckHeartbeat(self):
        '''
            Checks dripline's heartbeat to be sure it is running.
        '''
        status = self.Get("heartbeat")
        status.Wait()
        if not status['result'] == 'thump':
            raise UserWarning('Could not find dripline pulse. Make sure it is running.')
        return status['result']