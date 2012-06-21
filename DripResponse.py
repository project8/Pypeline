'''
    File to contain the DripResponse class.
'''

class DripResponse:
    '''
        Class which shall be returned by any DripInterface method which involves posting a document to a dripline db and, potentially, waiting for a result.

        This class will handle keeping track of the document's _id, and looking for responses stored there by dripline etc.
    '''
