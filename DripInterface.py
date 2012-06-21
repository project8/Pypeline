'''
    File for the pypeline class. At least for now I suspect this entire project goes in one class, if that changes it will need to be split into more files.
'''

from time import sleep
from uuid import uuid4
from couchdb import Server as CouchServer

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
        self._sleep_time = 3 #number of seconds to sleep while waiting
        self._wait_state = {}
        if (self._server.__contains__('dripline_cmd')):
            self._cmd_database = self._server['dripline_cmd']
        else:
            raise UserWarning('The dripline command database was not found!')
        self.CheckHeartbeat()

    def _wait_for_changes(self, document_id, last_seq, timeout=False):
        '''
            "Private" method which listens to the changes feed
            for updates to a particular document. Upon seeing an update,
            attempts to return the value of the 'results' field.

            Inputs:
                <document_id> is the value of the '_id' field of the
                              document in the dripline_cmd database
                <timeout>=-1 is the time, in seconds, to wait between failed checks
                               for changes.
                               [<0] uses the value in self._timeout
        '''
        if timeout < 0:
            timeout = self._timeout
        result = None
        timer = 0
        notfound = True
        while (timer < timeout and notfound):
            new_changes = self._cmd_database.changes(since=last_seq)
            if new_changes['last_seq'] > last_seq:
                for a_change in new_changes['results']:
                    if (a_change['id'] == document_id and
                     'result' in self._cmd_database[document_id]):
                        result = self._cmd_database[document_id]['result']
                        notfound = False
                        break
            sleep(self._sleep_time)
            timer = timer + self._sleep_time
        if notfound:
            print('Change never found, timeout exceeded')
        return result

    def HasAResult(self, request):
        '''
            Check for a result from some posted Set(), Get(), or Run().
        '''
        result = False
        if self._cmd_database[request['_id']]['result']:
            result = True
            request['result'] = self._cmd_database[request['_id']]['result']
            if 'timestamp' in self._cmd_database[request['_id']]:
                request['timestamp'] = self._cmd_database[request['_id']]['timestamp']
            if 'final' in self._cmd_database[request['_id']]:
                request['final'] = self._cmd_database[request['_id']]['final']
        return request

    def Get(self, channel, wait_time=False):
        '''
            Request and return the current value of some channel.

            Inputs:
                <channel> must be an active channel in dripline.
                <wait_time> determines if and how long Get() will wait for a changes feed post
                            [=False] (default) does not wait for changes
                            <0 uses default time
        '''
        result = {'_id':uuid4().hex,
            'last_seq':self._cmd_database.changes()['last_seq'],
            'result':{}
        }
        if wait_time < 0:
            wait_time = self._timeout
        get_doc = {
            '_id':result['_id'],
            'type':'command',
            'command':{
                "do":"get",
                "channel":channel,
            },
        }
        self._cmd_database.save(get_doc)
        if wait_time:
            result['result'] = self._wait_for_changes(get_doc['_id'], result['last_seq'], wait_time)
            if 'result' in self._cmd_database[result['_id']]:
                result['result'] = self._cmd_database[result['_id']]['result']
            if 'timestamp' in self._cmd_database[result['_id']]:
                result['timestamp'] = self._cmd_database[result['_id']]['timestamp']
            if 'final' in self._cmd_database[result['_id']]:
                result['final'] = self._cmd_database[result['_id']]['final']
        return result

    def Set(self, channel, value, check=False, wait_time=False):
        '''
            Change the setting of a dripline channel

            Inputs:
                <channel> must be an active channel in dripline
                <value> value to assign to <channel>
                <check> uses Get() to check the value,
                        WARNING: this doesn't deal with machine rounding
                <wait_time> determines if and how long Set() will wait for a changes feed post
                            [=False] (default) does not wait for changes
                            <0 uses default time

            WARNING! I do not yet check to ensure setting of the correct type.
        '''
        result = {'_id':uuid4().hex,
            'last_seq':self._cmd_database.changes()['last_seq'],
            'result':{}
        }
        if wait_time < 0:
            wait_time = self._timeout
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
        if wait_time:
            result = self._wait_for_changes(result['_id'], result['last_seq'], wait_time)
        if check:
            newval = Get(channel, value)
            if not newval == value:
                print("Set() seems to have worked but the value is " + str(newval) + 
                        " not " + str(value) + " as requested!")
                print("returning None")
                result = None
        return result

    def Run(self, durration=250, rate=500, filename=None, wait_time=False):
        '''
            Take a digitizer run of fixed time and sample rate.

            Inputs:
                <durration> is the time interval (in ms) that will be digitized
                <rate> is the sample rate (in MHz) of the digitizer
                <filename> is the file on disk where the data will be written
                           [=None] results in a uuid4().hex hash prefix and .egg extension
                           NOTE: you should probably just take the default unless you have
                           a good reason not to do so.
                <wait_time> determines if and how long Run() will wait for a changes feed post
                            [=False], (ie if not wait_time) returns without waiting for changes
                            if <0 uses default + durration*10^-3 (ie default after end of run)
        '''
        result = {'_id':uuid4().hex,
            'last_seq':self._cmd_database.changes()['last_seq'],
            'result':{}
        }
        print('run doc _id is ' + str(result['_id']))
        if wait_time < 0:
            wait_time = self._timeout + durration * 0.001
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
        if wait_time:
            result['result'] = self._wait_for_changes(run_doc['_id'], result['last_seq'], wait_time)
            if 'timestamp' in self._cmd_database[run_doc['_id']]:
                result['timestamp'] = self._cmd_database[run_doc['_id']]['timestamp']
            if 'final' in self._cmd_database[run_doc['_id']]:
                result['final'] = self._cmd_database[run_doc['_id']]['final']
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
        result = self.Get("heartbeat", wait_time=-1)
        pulse = result['result']
        if not pulse == 'thump':
            raise UserWarning('Could not find dripline pulse. Make sure it is running.')
        return pulse
