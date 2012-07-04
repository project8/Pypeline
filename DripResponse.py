'''
    File to contain the DripResponse class which inherits from dict.
'''

from time import sleep

class DripResponse(dict):
    '''
        Class which shall be returned by any DripInterface method which involves posting a document to a dripline db and, potentially, waiting for a result.

        This class will handle keeping track of the document's _id, and looking for responses stored there by dripline etc.

        Will be indexable with all of the standard dripline database fields.
    '''

    def __init__(self, cmd_db, doc_id):
        '''
            Initialization for a DripRespnse instance.

            Inputs:
                <cmd_db> the dripline command database. This is where DripResponse will look
                    for updates do documents
        '''
        dict.__init__(self)
        self._cmd_db = cmd_db
        self._delta_t = 0.1 #seconds
        self._max_timeout = 3600 #1 hr (in sec)
        self['_id'] = doc_id
    
    def __repr__(self):
        '''
            Defines the string representation of a DripResponse object.
        '''
        rval = "<" + str(self['final']) + ">"
        return rval

    def Waiting(self):
        '''
            Check a document to see if it has a 'result' field
            (ie dripline has responded to it.)
        '''
        self.Update()
        return not 'result' in self

    def Update(self):
        '''
            Checks a doc for updates and updates local attributes if they differ.
            If they differ, update self to match the document.
        '''
        for key in self._cmd_db[self['_id']]:
            self[key] = self._cmd_db[self['_id']][key]
        return self

    def Wait(self, timeout=15):
        '''
            Actively monitor a document for updates

            Inputs:
                <timeout>=15 is max wait time in seconds
                WARNING: if <timeout>==False, the max timeout (3600 sec) will be used
                         (I'm not putting in an infinite loop)
        '''
        timer = 0
        if not timeout:
            timeout = self._max_timeout
        while (self.Waiting() and timer < timeout):
            sleep(self._delta_t)
            timer = timer + self._delta_t
        self.Update()
        return self
