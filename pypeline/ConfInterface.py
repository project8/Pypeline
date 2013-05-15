'''
    Class specifically for interactions with dripline's configuration database.
'''

# standard imports
from time import sleep
from uuid import uuid4

# 3rd party imports

# local imports
try:
    from .DripResponse import DripResponse
except ImportError:
    from DripResponse import DripResponse


class _ConfInterface:

    '''
        Class for interactions with the configurations database

        This class is meant to be internal to pypeline and should NOT be used directly.
    '''

    def __init__(self, conf_database):
        '''
            <conf_database> is the dripline configuration database (element of a couchdb Server object)
        '''
        self._conf_database = conf_database

    def EligibleChannels(self):
        '''
            Creates a list of all possible channels to query or set.
        '''
        rows = []
        for row in self._conf_database.view('objects/channels'):
            rows.append(row.key)
        return rows

    def EligibleLoggers(self):
        '''
            Creates a list of all possible channels to log.
        '''
        rows = []
        for row in self._conf_database.view('objects/loggers'):
            rows.append(row.key)
        return rows

    def AddLoggers(self, instruments, intervals):
        '''
            Add each element of instruments to the configuration database as a logger
        '''
        for (instrument, interval) in zip(instruments, intervals):
            match = False
            match = sum([instrument == row.key for row in self._conf_database.view(
                'objects/loggers')])
            if match:
                print(instruments[i] + " already added")
                continue
            add_doc = {
                '_id': uuid4().hex,
                'channel': instruments[i],
                'interval': intervals[i],
                'type': 'logger',
            }
            self._conf_database.save(add_doc)

    def RemoveLoggers(self, instruments):
        '''
            Remove each element of instruments from the configuration database as a logger
        '''
        # for inst in instruments:
        for row in self._conf_database.view('objects/loggers'):
            if instruments.count(row.key):
                self._conf_database.delete(self._conf_database.get(row.id))
