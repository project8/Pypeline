'''
    File to contain the DripResponse class.
'''

class DripResponse:
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
        self._cmd_db = cmd_db
        self._id = doc_id

    def Waiting(self):
        '''
            Check a document to see if it has a 'result' field
            (ie dipline has responded to it.)
        '''
        return 'result' in self._cmd_db[self._id]


    def Update(self):
        '''
            Checks a doc for updates and updates local attributes if they differ.
            If they differ, update self to match the document.
        '''

    def Wait(self):
        '''
            Actively monitor a document for updates
        '''
