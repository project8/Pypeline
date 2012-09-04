'''
    Class specifically for interactions with dripline's command database
'''

# standard imports
from time import sleep
from uuid import uuid4

# 3rd party imports

# local imports
try:
    from .DripResponse import DripResponse
except ImportError:
    from DripResponse import DripResponse

class _CmdInterface:
    '''
        Class for interactions with the command database.

        This class is meant to be internal to pypeline and should NOT be used directly
    '''

    def __init__(self, cmd_database):
        '''
            <cmd_database> is the dripline command database (element of a couchdb Server object)
        '''
        self._cmd_database = cmd_database

    def Get(self, channel, wait=False):
        '''
            Post a "get" document to the command database.
    
            Inputs:
                <cmd_database> must be a database object (from couchdb package)
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
        return result

    def Set(self, channel, value):
        '''
            Post a "set" document to the command database

            Inputs:
                <channel> must be an active channel in dripline
                <value> value to assign to <channel>
            
                If <channel> is left blank, this method will print the names
                of all possible channels to set.
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

    def StartLoggers(self, instruments):
        '''
            Tells the dripline logger to start following one or more instruments
        '''
        if type(instruments) == type(''):
            instruments = [instruments]
        result = DripResponse(self._cmd_database, uuid4().hex)
        start_doc = {
            '_id':result['_id'],
            'type':'command',
            'command':{
                "do":"syscmd",
                "action":"start_loggers",
                "args":instruments,
            },
        }
        self._cmd_database.save(start_doc)
        return result

    def StopLoggers(self, instruments):
        '''
            Tells the dripline logger to stop following one or more instruments
        '''
        if type(instruments) == type(''):
            instruments = [instruments]
        result = DripResponse(self._cmd_database, uuid4().hex)
        stop_doc = {
            '_id':result['_id'],
            'type':'command',
            'command':{
                "do":"syscmd",
                "action":"stop_loggers",
                "args":instruments,
            },
        }
        self._cmd_database.save(stop_doc)
        return result

    def CurrentLoggers(self):
        '''
            Tells the dripline logger to list which instruments are currently
            being logged.
        '''
        result = DripResponse(self._cmd_database, uuid4().hex)
        start_doc = {
            '_id':result['_id'],
            'type':'command',
            'command':{
                "do":"syscmd",
                "action":"current_loggers",
            },
        }
        self._cmd_database.save(start_doc)
        return result
    
    def Run(self, duration, rate, filename):
        '''
            Take a digitizer run of fixed time and sample rate.

            Inputs:
                <duration> is the time interval (in ms) that will be digitized
                <rate> is the sample rate (in MHz) of the digitizer
                <filename> is the file on disk where the data will be written
                           [=None] results in a uuid4().hex hash prefix and
                           .egg extension
                           NOTE: you should probably just take the default
                           unless you have
                           a good reason not to do so.
        '''
        result = DripResponse(self._cmd_database, uuid4().hex)
        run_doc = {
            '_id':result['_id'],
            'type':'command',
            'command':{
                "do":"run",
                "duration":str(duration),
                "rate":str(rate),
                "output":filename,
            },
        }
        self._cmd_database.save(run_doc)
        return result

    def CreatePowerSpectrum(self, dripresponse, sp):
        result = DripResponse(self._cmd_database, uuid4().hex)
        pow_doc = {
            '_id':result['_id'],
            'type':'command',
            'command':{
                "do":"run",
                "subprocess":sp,
                "input":dripresponse['command']['output'],
            },
        }
        self._cmd_database.save(pow_doc)
        return result
