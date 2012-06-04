'''
    File for the pypeline class. At least for now I suspect this entire project goes in one class, if that changes it will need to be split into more files.
'''

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
        if (self._server.__contains__('dripline_cmd')):
            self._cmd_database = self._server['dripline_cmd']
        else:
            raise UserWarning('The dripline command database was not found!')
        self.CheckHeartbeat()

    def CheckHeartbeat(self):
        '''
            Checks dripline's heartbeat to be sure it is running.
        '''
        heartbeat_doc = {
            'type':'command',
            'command':{
                "do":"get",
                "channel":"heartbeat",
            },
        }
        self._cmd_database.save(heartbeat_doc)
        if not self._cmd_database[heartbeat_doc['_id']]['result'] == "thump":
            raise UserWarning('could not find dripline pulse, be sure it is running.')
