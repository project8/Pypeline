'''
    File for the pypeline class. At least for now I suspect this entire project goes in one class, if that changes it will need to be split into more files.
'''

from time import sleep
from uuid import uuid4
from couchdb import Server as CouchServer

class Pypeline:
    '''
        Class to interface with dripline. Should allow for natural scripting/automation of run tasks.
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
        timer = 0
        notfound = True
        while (timer < self._timeout and notfound):
            new_change = self._cmd_database.changes(since=last_sequence)
            if new_change['last_seq'] > last_sequence:
                for a_change in new_change['results']:
                    if (a_change['id'] == get_doc['_id'] and 'result' in self._cmd_database[get_doc['_id']]):
                        channelvalue = self._cmd_database[get_doc['_id']]['result']
                        notfound = False
            else:
                sleep(3)
                timer = timer + 3
        if notfound:
            print("timed out waiting for result, returning None")
            return None
        return self._cmd_database[get_doc['_id']]['result']

    def Set(self, channel, value, check=False):
        '''
            Change the setting of a dripline channel

            Inputs:
                <channel> must be an active channel in dripline
                <value> value to assign to <channel>

            WARNING! I do not yet check to ensure setting of the correct type.
        '''
        last_sequence = self._cmd_database.changes()['last_seq']
        set_doc = {
            'type':'command',
            'command':{
                "do":"set",
                "channel":channel,
                "value":str(value),
            },
        }
        self._cmd_database.save(set_doc)
        print('set document saved')
        timer = 0
        notfound = True
        while (timer < self._timeout and notfound):
            new_change = self._cmd_database.changes(since=last_sequence)
            if new_change['last_seq'] > last_sequence:
                for a_change in new_change['results']:
                    if (a_change['id'] == set_doc['_id'] and 'result' in self._cmd_database[set_doc['_id']]):
                        notfound = False
            else:
                sleep(3)
                timer = timer + 3
                print('timer is at '+str(timer))
        print('while loop finished')
        if notfound:
            print("timed out waiting for result, returning None")
            return None
        elif not self._cmd_database[set_doc['_id']]['result'] == 'ok':
            print("dripline did not respond with okay in time, returning None")
            return None

        if check:
            newval = Get(channel, value)
            if not newval == value:
                print("Set() seems to have worked but the value is " + str(newval) + 
                        " not " + str(value) + " as requested!")
                print("returning None")
                return None
        return True

    def ChangeTimeout(self, duration):
        '''
            Change how long a get will look for changes before timeout.
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
