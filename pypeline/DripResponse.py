'''
    File to contain the DripResponse class which inherits from dict.
'''

# import standard libraries
from time import sleep
from .PypelineErrors import DriplineError


class DripResponse(dict):

    '''
        Class which shall be returned by any DripInterface method which
        involves posting a document to a dripline db expecting dripline to
        modify that document.

        This class will handle keeping track of the document's _id,
        and looking for responses stored there by dripline etc.

        Will have a key:value pair for each field of the document.
    '''

    def __init__(self, cmd_db, doc_id):
        '''
            Internal: Initializes the default attribute values etc.

            Inputs:
                <cmd_db> the dripline command database. This is where
                         DripResponse will look for updates do documents
                <doc_id> the value of "_id" for the document.
        '''
        dict.__init__(self)
        self._cmd_db = cmd_db
        self._delta_t = 0.1  # seconds
        self._max_timeout = 3600  # 1 hr (in sec)
        self['_id'] = doc_id

    def Update(self):
        '''
            Sets a key:value pair for each field of the couch doc.
            Existing key:values are changed and new ones are created.
            Missing keys are NOT removed.

            Changes are made to the current instance but a copy is also
            returned.
        '''
        for key in self._cmd_db[self['_id']]:
            self[key] = self._cmd_db[self['_id']][key]
        if 'result' in self:
            if self['result'] == 'error':
                msg = ''
                if isinstance(self['result'], dict):
                    msg = self['result']['error']
                else:
                    msg = self['result']
                raise DriplineError(msg)
            if self['result'] == 'ok':
                self['result'] = self['command']['value']
        return self

    def Waiting(self):
        '''
            Check a document to see if it has a 'result' field
            (ie dripline has responded to it.)

            Returns True or False if 'result' is found or not respectively.
        '''
        self.Update()
        return not 'result' in self

    def Wait(self, timeout=15):
        '''
            Actively monitor a document for updates

            Inputs:
                <timeout>=15 is max wait time in seconds
                WARNING: if <timeout>==False, the max timeout (3600 sec)
                         will be used (I'm not putting in an infinite loop)

            Changes are made to the current instance but a copy is also
            returned.
        '''
        timer = 0
        if not timeout:
            timeout = self._max_timeout
        while (self.Waiting() and timer < timeout):
            sleep(self._delta_t)
            timer = timer + self._delta_t
        self.Update()
        return self

    def Result(self):
        '''
        '''
        result = None
        self.Wait()
        if not self.Waiting():
            result = self['result'].popitem()[1]['result']
        return result
