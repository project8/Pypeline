'''
    Class specifically for interactions with the sensor dump database
'''

# standard imports
from datetime import datetime
# 3rd party imports
# local imports


class _SensorDumpInterface:
    '''
        Class for interactions with the sensor dump database.

        This class is meant to be internal to pypeline and should NOT be used directly.
    '''

    def __init__(self, sensor_dump_database):
        '''
            <sensor_dump_database> is the sensor dump database (element of a couchdb Sever object)
        '''
        self._sensor_dump_database = sensor_dump_database

    def _StoreDump(self, dumplist, field_dict):
        '''
            <dumplist> is either a drip response, or a list there of
            <field_dict> is a dict of extra data to include in the dump doc
        '''
        if not isinstance(dumplist, list):
            dumplist = [dumplist]
        dump_doc = {'timestamp':datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        dump_doc.update(field_dict)
        for response in dumplist:
            dump_doc[response['command']['channel']] = response
        self._sensor_dump_database.save(dump_doc)

