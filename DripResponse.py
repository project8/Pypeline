'''
    File to contain the DripResponse class.
'''

class DripResponse:
    '''
        Class which shall be returned by any DripInterface method which involves posting a document to a dripline db and, potentially, waiting for a result.

        This class will handle keeping track of the document's _id, and looking for responses stored there by dripline etc.

        Will be indexable with all of the standard dripline database fields.
    '''

    def __init__(self, cmd_db):
        '''
            Initialization for a DripRespnse instance.

            Inputs:
                <cmd_db> the dripline command database. This is where DripResponse will look
                    for updates do documents
        '''
        self._cmd_db = cmd_db

    def Waiting(self):
        '''
            Check the status of a document to see if it has been updated.
        '''

    def Update(self):
        '''
            Compares the current state of self with the current state of the document in the db.
            If they differ, update self to match the document.
        '''

    def Wait():
        '''
            Actively monitor a document for updates
        '''
