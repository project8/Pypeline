'''
    Class specifically for interactions with dripline's configuration database.
'''

# standard imports
from time import sleep
from uuid import uuid4
from datetime import datetime

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

    def GetTimeSeries(self, sensor, start, stop):
        '''
            Retrieve data logged on CouchDB in a specified window and return it
            as a numpy array.

            Inputs:
                <sensor> (string) is the sensor whose logged data you would
                         like to retrieve
                <start> (string) is the timestamp of the beginning of the log
                        you would like to retrieve
                <stop> (string) is the timestamp of the end of the log you
                       would like to retrieve
            Returns:
                (timelist, valuelist, unitlist)
        '''
        timelist = []
        valuelist = []
        unitlist = []
        for row in self._log_database.view('log_access/all_logged_data',
                                          startkey=start, endkey=stop):
            timestamp = datetime.strptime(row.value['timestamp_localstring'],
                                          "%Y-%m-%d %H:%M:%S")
            if row.value['sensor_name'] == sensor:
                timelist.append(timestamp)
                valuelist.append(float(row.value[
                                 'calibrated_value'].split()[0]))
                unitlist.append(str(row.value['calibrated_value'].split()[1]))
        return (timelist, valuelist, unitlist)

    def GetLatestValues(self):
        '''
        '''
        loggers_dict = {}
        latest = self._log_database.view('pypeline_view/latest_values')
        for channel in self.ListWithProperty('logging'):
            ch_val = latest[channel].rows[0]['value']['cal_val']
            ch_time = latest[channel].rows[0]['value']['timestamp']
            if ch_val:
                entrylist = ch_val.split()
                update = []
                for snip in entrylist:
                    try:
                        update.append('%.4E' % float(snip))
                    except ValueError:
                        update.append(snip)
                loggers_dict[channel]={'value':" ".join(update),
                                       'time':ch_time}
        return loggers_dict

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
