'''
    File for the pypeline class. At least for now I suspect this entire project goes in one class, if that changes it will need to be split into more files.
'''

#standard imports
from time import sleep
from uuid import uuid4

#3rd party imports
from couchdb import Server as CouchServer

#local imports
try:
    from .DripResponse import DripResponse
except ImportError:
    from DripResponse import DripResponse
try:
    from .CmdInterface import _CmdInterface
except ImportError:
    from CmdInterface import _CmdInterface
try:
    from .ConfInterface import _ConfInterface
except ImportError:
    from ConfInterface import _ConfInterface

class DripInterface:
    '''
        Class to interact with Dripline via couchDB.
    '''

    def __init__(self, dripline_url="http://127.0.0.1:5984"):
        '''
            Initializes an instance of pypeline by connecting to the server.
    
            Inputs:
                <dripline_url> is the url to use when connecting to the couchDB
                server,
                if none is provided then the default (http://127.0.0.1:5984/).
        '''
        self._server = CouchServer(dripline_url)
        self._timeout = 15 #timeout is 15 seconds...
        self._sleep_time = .1 #number of seconds to sleep while waiting
        self._wait_state = {}
        if (self._server.__contains__('dripline_cmd')):
            self._cmd_database = self._server['dripline_cmd']
            self._cmd_interface = _CmdInterface(self._server['dripline_cmd'])
        else:
            raise UserWarning('The dripline command database was not found!')
        if (self._server.__contains__('dripline_conf')):
            self._conf_database = self._server['dripline_conf']
            self._conf_interface = _ConfInterface(self._server['dripline_conf'])
        else:
            raise UserWarning('The dripline conf database was not found!')
        self.CheckHeartbeat()

    def Get(self, channel=None, wait=False):
        '''
            Request and return the current value of some channel.

            Inputs:
                <channel> must be an active channel in dripline.
            
                If <channel> is left blank, this method will print the names
                of all possible channels to set.
        '''
        if not channel:
            print(self._conf_interface.EligibleChannels())
        else:
            result = self._cmd_interface.Get(channel)
            if wait:
                result.Wait()
            return result

    def Set(self, channel=None, value=None, wait=False):
        '''
            Change the setting of a dripline channel

            Inputs:
                <channel> must be an active channel in dripline
                <value> value to assign to <channel>
                <check> uses Get() to check the value,
                        WARNING: this doesn't deal with machine rounding
            
                If <channel> is left blank, this method will print the names
                of all possible channels to set.
            
            WARNING! I do not yet check to ensure setting of the correct type.
        '''
        if not channel:
            print(self.EligibleChannels())
        elif not value:
            print("Please input value to assign to channel")
        else:
            result = self._cmd_interface.Set(channel, value)
            if wait:
                result.Wait()
            return result

    def StartLoggers(self, instruments=False, wait=False):
        '''
            Tells the dripline logger to start following one or more instruments
        '''
        if not instruments:
            print(self.EligibleLoggers())
        else:
            result = self._cmd_interface.StartLoggers(instruments)
            if wait:
                result.Wait()
            return result

    def StopLoggers(self, instruments=False, wait=False):
        '''
            Tells the dripline logger to stop following one or more instruments
        '''
        if not instruments:
            print(self.EligibleLoggers())
        else:
            result = self._cmd_interface.StartLoggers(instruments)
            if wait:
                result.Wait()
            return result

    def CurrentLoggers(self, wait=False):
        '''
            Tells the dripline logger to list which instruments are currently
            being logged.
        '''
        result = self._cmd_interface.CurrentLoggers()
        if wait:
            result.Wait()
        return result
    
    def AddLoggers(self, instruments=False, intervals=False):
        if not instruments:
            self._conf_interface.EligibleChannels()
        else:
            if type(instruments) == type(''):
                instruments = [instruments]
            if not intervals:
                intervals = ['10' for a in range(len(instruments))]
            elif type(intervals) == type(''):
                intervals = [intervals]
            for i in range(len(instruments)):
                match = False
                for row in self._conf_database.view('objects/loggers'):
                    if instruments[i] == row.key:
                        match = True
                if match:
                    print(instruments[i] + " already added")
                    continue
                add_doc = {
                    '_id':uuid4().hex,
                    'channel':instruments[i],
                    'interval':intervals[i],
                    'type':'logger',
                }
                self._conf_database.save(add_doc)

    def RemoveLoggers(self, instruments=False):
        if not instruments:
            for row in self._conf_database.view('objects/loggers'):
                print(row.key)
        else:
            if type(instruments) == type(''):
                instruments = [instruments]
            for inst in instruments:
                for row in self._conf_database.view('objects/loggers'):
                    if row.key == inst:
                        self._conf_database.delete(self._conf_database.get(row.id))
            
    def Run(self, duration=250, rate=500, filename=None):
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
        if not filename:
            filename = '/data/' + uuid4().hex + '.egg'
        result = self._cmd_interface.Run(duration, rate, filename)
        return result

    def CreatePowerSpectrum(self, dripresponse, sp):
        '''
        '''
        return self._cmd_interface.CreatePowerSpectrum(dripresponse, sp)
        
    def CheckHeartbeat(self):
        '''
            Checks dripline's heartbeat to be sure it is running.
        '''
        status = self.Get("heartbeat")
        status.Wait()
        if not status['final'] == 'thump':
           raise UserWarning('Could not find dripline pulse. Make sure it is running.')
        return status['final']
