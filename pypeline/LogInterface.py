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


class _LogInterface:

    '''
        Class for interactions with the logged data database

        This class is meant to be internal to pypeline and should NOT be used directly.
    '''

    def __init__(self, log_database):
        '''
            <conf_database> is the dripline configuration database (element of a couchdb Server object)
        '''
        self._log_database = log_database

    def LogValue(self, sensor, uncal_val, cal_val, timestamp):
        '''
            <sensor> is the atom for the sensor being logged
            <uncal_val> is the uncalibrated value string
            <cal_val> is the calibrated value string
            <timestamp> is a datetime object
        '''
        result = DripResponse(self._log_database, uuid4().hex)
        log_doc = {
            '_id': result['_id'],
            'sensor_name': sensor,
            'timestamp_localstring': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'uncalibrated_value': str(uncal_val),
            'calibrated_value': str(cal_val),
        }
        self._log_database.save(log_doc)
        return result
