'''
    File for the pypeline class. At least for now I suspect this entire project goes in one class, if that changes it will need to be split into more files.
'''

#standard imports
from time import sleep
from uuid import uuid4
from datetime import datetime

#3rd party imports
from couchdb import Server as CouchServer

#local imports (the try is python 3 syntax, the cought exceptions try python 2 syntax)
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
try:
    from .LogInterface import _LogInterface
except ImportError:
    from LogInterface import _LogInterface

class DripInterface:
    '''
        Class to facilitate user interact with Dripline via couchDB. The 
        actual database manipulations are contained in _CmdInterface and 
        _ConfInterface. Scripting tasts will involve primarily an 
        instance of this class and those python.DripResponse instances 
        which it creates.
    '''

    def __init__(self, dripline_url="http://127.0.0.1:5984"):
        '''
            Internal: Initializes each instance by doing the following:
                1) connecting to the provided dripline couchdb (default is localhost)
                2) sets initial/default value for attributes
                3) finds the command and configuration databases within the server
                4) checks the status of dripline for checking for a heartbeat
    
            Inputs:
                <dripline_url> is the url to use when connecting to the couch.
                    (default is http://127.0.0.1:5984 ie. localhost).

            Returns:
                no return
        '''
        self._server = CouchServer(dripline_url)
        self._timeout = 15 #timeout is 15 seconds...
        self._sleep_time = .1 #number of seconds to sleep while waiting
        self._wait_state = {}
        if (self._server.__contains__('dripline_cmd')):
            self._cmd_database = self._server['dripline_cmd']
            self._cmd_interface = _CmdInterface(self._cmd_database)
        else:
            raise UserWarning('The dripline command database was not found!')
        if (self._server.__contains__('dripline_conf')):
            self._conf_database = self._server['dripline_conf']
            self._conf_interface = _ConfInterface(self._conf_database)
        else:
            raise UserWarning('The dripline conf database was not found!')
        if (self._server.__contains__('dripline_logged_data')):
            self._log_database = self._server['dripline_logged_data']
            self._log_interface = _LogInterface(self._log_database)
        else:
            raise UserWarning('The dripline conf database was not found!')

    def Get(self, channel='', wait=False):
        '''
            Post a document to the command database using the get verb for a specific channel.

            Inputs:
                <channel> is any configured channel in dripline.
                    If no channel is given, or the value passed evaluates as False, gives the available channels

            Returns:
                IF a channel was given: returns a pypeline.DripResponse instance.
                OTHERWISE: returns a list of strings of the available channel names.

            Notes:
                1) The channel name is not validated, invalid channel names will still be posted.
        '''
        if not channel:
            result = self._conf_interface.EligibleChannels()
        else:
            result = self._cmd_interface.Get(channel)
            if wait:
                result.Wait()
        return result

    def Set(self, channel=None, value=None, wait=False):
        '''
            Post a document to the command database using the set verb for a specific channel.

            Inputs:
                <channel> is any dripline channel
                    If no channel is given, or the the value passed evaluates as False, gives the available channels
                <value> value to assign to <channel>
                <wait> If wait evaluates as True, wait for either a timeout or a response from dripline before returning

            Returns:
                IF: a channel was given, returns a pypeline.DripResponse instance.
                OTHERWISE: returns a list of strings of the available channel names.

            Notes:
                1) The channel name is not validated as an existing channel, or as one which admits the set verb.
        '''
        if not channel:
            result = self._conf_interface.EligibleChannels()
        elif not value:
            print("Please input value to assign to channel")
            result = False
        else:
            result = self._cmd_interface.Set(channel, value)
            if wait:
                result.Wait()
        return result

    def StartLoggers(self, instruments=False, wait=False):
        '''
            Posts a document to the command database to start the logging one or more instruments.

            Inputs:
                <instruments> is either the name of a channel or a list of channel names for which logging should start
                    If no instrument is given, or the the value passed evaluates as False, gives the available instruments
                    as determined by the loggers view of the configuration database.
                <wait> If wait evaluates as True, wait for either a timeout or a response from dripline before returning

            Returns:
                IF: a channel was given, returns a pypeline.DripResponse instance
                OTHERWISE: returns a list of eligible loggers
        '''
        if not instruments:
            result = self._conf_interface.EligibleLoggers()
        else:
            result = self._cmd_interface.StartLoggers(instruments)
            if wait:
                result.Wait()
        return result

    def StopLoggers(self, instruments=False, wait=False):
        ''' 
            Posts a document to the command database to stop the logging one or more instruments.

            Inputs:
                <instruments> is either the name of a channel or a list of channel names for which logging should stop
                    If no instrument is given, or the the value passed evaluates as False, gives the available instruments
                    as determined by the loggers view of the configuration database.
                <wait> If wait evaluates as True, wait for either a timeout or a response from dripline before returning

            Returns:
                IF: a channel was given, returns a pypeline.DripResponse instance
                OTHERWISE: returns a list of eligible loggers

            Notes:
                1) Dripline seems to have a bug, these documents are posting and being responded to, but logging does not stop.
        '''
        if not instruments:
            result = self._conf_interface.EligibleLoggers()
        else:
            result = self._cmd_interface.StopLoggers(instruments)
            if wait:
                result.Wait()
        return result

    def CurrentLoggers(self, wait=False):
        '''
            Posts a document to the command database which requests the list of channels currently being logged.

            Inputs:
                <wait> If wait evaluates as True, wait for either a timeout or a response from dripline before returning

            Returns:
                A pypeline.DripResponse instance

            Notes:
                1) Dripline seems to have a bug, these documents are posting but receive no response.
        '''
        result = self._cmd_interface.CurrentLoggers()
        if wait:
            result.Wait()
        return result
    
    def AddLoggers(self, instruments=False, intervals=False):
        '''
            Posts a document to the configuration database making an instrument into a potential logger.

            Inputs:
                <instruments> an instrument name or list of names for which logging capabilities are to be established
                <intervals> matched set of values, giving the logging interval

            Returns:
                nothing is returned
        '''
        if not instruments:
            return self._conf_interface.EligibleChannels()
        if type(instruments) == type(''):
            instruments = [instruments]
        if not intervals:
            intervals = ['10' for i in range(len(instruments))]
        elif type(intervals) == type(''):
            intervals = [intervals]
        self._conf_iterface.AddLoggers(instruments, intervals)

    def RemoveLoggers(self, instruments=''):
        '''
            Removes the docuemnt(s) from the configuration database which makes <instruments> (a) potential logger(s)

            Inputs:
                <instruments> an instrument name or list of names for which logging capabilities are to be removed.

            Returns:
                nothing is returned
        '''
        if not instruments and not instruments == False:
            return self._conf_interface.EligibleLoggers()
        elif type(instruments) == type(''):
            instruments = [instruments]
        self._conf_interface.RemoveLoggers(instruments)
            
    def Run(self, duration=250, rate=500, filename=None, channels=2):
        '''
            Posts a document to the command database instructing dripline to start a mantis run.

            Inputs:
                <duration> is the time interval (in ms) that will be digitized
                <rate> is the sample rate (in MHz) of the digitizer
                <filename> is the file on disk where the data will be written
                           [=None] results in a uuid4().hex hash prefix and
                           .egg extension
                           NOTE: you should probably just take the default
                           unless you have a good reason not to do so.

            Returns:
                An instance of pypeline.DripResponse
        '''
        if not filename:
            filename = '/data/' + uuid4().hex + '.egg'
        return self._cmd_interface.Run(duration, rate, filename, channels)

    def LogValue(self, sensor, uncal_val, cal_val, timestamp=datetime.now()):
        '''
            Posts a document to the logged data database, logging a channel reading.

            This being put in for the B field measured by dpph but the result of any other scripted measurement could also be logged in this way

            Inputs:
                <sensor> is the atom for the sensor being logged
                <uncal_val> is the uncalibrated value string
                <cal_val> is the calibrated value string
                <timestamp> is a datetime object
            Returns:
                An instance of pypeline.DripResponse

            NOTE: Dripline doesn't listen to the log database so DripResponse should NOT get a response
        '''
        return self._log_interface.LogValue(sensor, uncal_val, cal_val, timestamp)

    def CreatePowerSpectrum(self, dripresponse, sp):
        '''
            Posts a document to the command database requesting a power spectrum be created for a given run.

            Inputs:
                <dripresponse> a pypeline.DripResposne object which instigated the relavent mantis run
                <sp> the executable to be used (powerline or any other which may be added)

            Returns:
                A pypeline.DripResponse instance.
        '''
        return self._cmd_interface.CreatePowerSpectrum(dripresponse, sp)
        
    def CheckHeartbeat(self):
        '''
            Checks to see if dripline is listing and responding to the command database.

            Inputs:
                no inputs

            Returns:
                The 'final' field fron the couch document produced by calling pypeline.DripInterface.Get("heartbeat")
        '''
        status = self.Get("heartbeat")
        status.Wait()
        if not status['final'] == 'thump':
           raise UserWarning('Could not find dripline pulse. Make sure it is running.')
        return status['final']

