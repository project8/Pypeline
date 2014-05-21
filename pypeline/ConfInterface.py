'''
    Class specifically for interactions with dripline's configuration database.
'''

from __future__ import print_function
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
        Class for interactions with the dripline configurations database

        This class is meant to be internal to pypeline and
        should NOT be used directly.
    '''

    def __init__(self, conf_database):
        '''
            <conf_database> is the dripline configuration database
            (element of a couchdb Server object)
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
        try:
            view_result = self._GetView('loggers')
        except:
            raise
        print(view_result)
        return [row.key for row in view_result.rows]
    
    def _GetView(self, view_name):
        '''
        '''
        return_value = False
        if '_design/type_lists' in self._conf_database:
            des_doc = self._conf_database['_design/type_lists']
            if 'views' in des_doc:
                if view_name in des_doc['views']:
                    return_value = True
        if not return_value:
            self._TryAddingView(view_name)
        return self._conf_database.view('type_lists/'+view_name)

    def _TryAddingView(self, view_name):
        '''
        '''
        # view_name specific part
        view_map = None
        if view_name == 'loggers':
            view_map = "function(doc) {\n  if(doc[\"type\"] == \"logger\") {\n\
                        emit(doc[\"channel\"], doc);\n  }\n}"
        else:
            raise KeyError('unable to add requested view')
        # grab and update the design document
        if '_design/type_lists' in self._conf_database:
            des_doc = self._conf_database['_design/type_lists']
        else:
            des_doc = {"_id":"_design/type_lists"}
        des_doc['language'] = 'javascript'
        if not 'views' in des_doc:
            des_doc['views'] = {}
        des_doc['views'][view_name] = {"map":view_map}
        self._conf_database.save(des_doc)

    def AddLoggers(self, instruments, intervals):
        '''
            Add each element of instruments to the configuration database
            as a logger
        '''
        for (instrument, interval) in zip(instruments, intervals):
            match = False
            match = sum([instrument == row.key for row in
                         self._conf_database.view('objects/loggers')])
            if match:
                print(instrument + " already added")
                continue
            add_doc = {
                '_id': uuid4().hex,
                'channel': instrument,
                'interval': str(interval),
                'type': 'logger',
            }
            self._conf_database.save(add_doc)

    def RemoveLoggers(self, instruments):
        '''
            Remove each element of instruments from the configuration database
            as a logger
        '''
        # for inst in instruments:
        for row in self._conf_database.view('objects/loggers'):
            if instruments.count(row.key):
                self._conf_database.delete(self._conf_database.get(row.id))
