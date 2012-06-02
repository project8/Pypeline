'''
    File for the pypeline class. At least for now I suspect this entire project goes in one class, if that changes it will need to be split into more files.
'''

class pypeline:
    '''
        Class to interface with dripline. Should allow for natural scripting/automation of run tasks.
    '''

    def __init__(self, dripline_url="http://127.0.0.1:5984/_utils"):
    '''
        Initializes an instance of pypeline by connecting to the server.

        Inputs:
            <dripline_url> is the url to use when connecting to the couchDB server, if none is provided then the default http://127.0.0.1:5984/_utils will be used.
    '''
