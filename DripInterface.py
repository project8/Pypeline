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
        if (self._server.__contains__('dripline_cmd')):
            self._cmd_database = self._server['dripline_cmd']
        else:
            raise UserWarning('The dripline command database was not found!')
        self.CheckHeartbeat()

    def _wait_for_changes(self, document_id, last_seq, timeout=None):
        '''
            "Private" method which listens to the changes feed
            for updates to a particular document. Upon seeing an update,
            attempts to return the value of the 'results' field.

            Inputs:
                <document_id> is the value of the '_id' field of the
                              document in the dripline_cmd database
                <timeout>=None is the time, in seconds, to wait between failed checks
                               for changes.
                               [=None] uses the value in self._timeout
        '''
        if timeout == None:
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

    def Get(self, channel):
        '''
            Request and return the current value of some channel.

            Inputs:
                <channel> must be an active channel in dripline.
        '''
        last_sequence = self._cmd_database.changes()['last_seq']
        get_doc = {
            '_id':uuid4().hex,
            'type':'command',
            'command':{
                "do":"get",
                "channel":channel,
            },
        }
        self._cmd_database.save(get_doc)
        change = self._wait_for_changes(get_doc['_id'], last_sequence)
        if not change:
            print("wait for changes returned None, doing the same")
        return self._cmd_database[get_doc['_id']]['result']

    def Set(self, channel, value, check=False):
        '''
            Change the setting of a dripline channel

            Inputs:
                <channel> must be an active channel in dripline
                <value> value to assign to <channel>
                <check> uses Get() to check the value,
                        WARNING: this doesn't deal with machine rounding

            WARNING! I do not yet check to ensure setting of the correct type.
        '''
        last_sequence = self._cmd_database.changes()['last_seq']
        set_doc = {
            '_id':uuid4().hex,
            'type':'command',
            'command':{
                "do":"set",
                "channel":channel,
                "value":str(value),
            },
        }
        self._cmd_database.save(set_doc)
        result = self._wait_for_changes(set_doc['_id'], last_sequence)
        
        #if check evaluates to True, see if Get returns the requested value
        if check:
            newval = Get(channel, value)
            if not newval == value:
                print("Set() seems to have worked but the value is " + str(newval) + 
                        " not " + str(value) + " as requested!")
                print("returning None")
                result = None
        return result

    def Run(self, durration=250, rate=500, filename=None)
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
        if not filename:
            filename = uuid4().hex + '.egg'
        last_sequence = self._cmd_database.changes()['last_seq']
        run_doc = {
            '_id':uuid4().hex,
            'type':'command',
            'command':{
                "do":"run",
                "durration":durration,
                "rate":rate,
                "output":filename,
            },
        }
        self._cmd_database.save(run_doc)
        result = self._wait_for_changes(run_doc['_id'], last_sequence)
        return result

    def ChangeTimeout(self, duration):
        '''
            Change how long a get will look for changes before timeout.a
        '''
        self._timeout = duration

    def CheckHeartbeat(self):
        '''
            Checks dripline's heartbeat to be sure it is running.
        '''
        pulse = self.Get("heartbeat")
        if not pulse == 'thump':
            raise UserWarning('Could not find dripline pulse. Make sure it is running.')
        return pulse
