'''
    Any custom errors will be defined here.

    In particular, the error for dripline not resonding is going in now.
    Errors returned by dripline would also go here.
'''

from __future__ import print_function


class DriplineError(Exception):
    '''
        Base class for exceptions from caused by dripline.
    '''

    def __init__(self, msg):
        '''
        '''
        print('', '*'*60, '\nA Dripline Error occured\n', '*'*60)
        Exception.__init__(self, msg)


class NoResponseError(DriplineError, IndexError):
    '''
        Exception raised when dripline fails to respond.
    '''

    def __init__(self, msg):
        '''
        '''
        self.msg = msg
        DriplineError.__init__(self, msg)


class RunTagNotUnique(Exception):
    '''
    '''

    def __init__(self, msg):
        '''
        '''
        self.msg = msg
        Exception.__init__(self, msg)

class TimeFormatError(Exception):
    '''
    '''

    def __init(self, msg):
        '''
        '''
        self.msg = msg
        Exception.__init__(self, msg)

class TimeOrderError(Exception):
    '''
    '''

    def __init(self, msg):
        '''
        '''
        self.msg = msg
        Exception.__init__(self, msg)
