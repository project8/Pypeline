'''
    Class specifically for interactions with dripline's configuration database.
'''

from __future__ import print_function, absolute_import

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
from .PypelineConsts import time_format


class _LogInterface:

    '''
        Class for interactions with the logged data database

        This class is meant to be internal to pypeline and should
        NOT be used directly.
    '''

    def __init__(self, log_database):
        '''
            <conf_database> is the dripline configuration database
                            (element of a couchdb Server object)
        '''
        self._log_database = log_database

    def GetTimeSeries(self, sensor, start, stop, max_len=False):
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
                <max_len> (int) drops enough data to have a series of this length
            Returns:
                (timelist, valuelist, unitlist)
        '''
        timelist = []
        valuelist = []
        unitlist = []
        for row in self._log_database.view('log_access/all_logged_data',
                                           startkey=start, endkey=stop):
            timestamp = datetime.strptime(row.value['timestamp_localstring'],
                                          time_format)
            if row.value['sensor_name'] == sensor:
                timelist.append(timestamp)
                valuelist.append(float(row.value[
                                 'calibrated_value'].split()[0]))
                unitlist.append(str(row.value['calibrated_value'].split()[-1]))
        if max_len and (len(valuelist) > max_len):
            timelist = [val for n,val in enumerate(timelist) if not n % len(timelist)/max_len]
            valuelist = [val for n,val in enumerate(valuelist) if not n % len(valuelist)/max_len]
            unitlist = [val for n,val in enumerate(unitlist) if not n % len(unitlist)/max_len]
        return (timelist, valuelist, unitlist)

    def GetLatestValues(self, channels):
        '''
            <channels> is a list of channel names for which the lastest value
                       is being requested
        '''
        loggers_dict = {}
        latest = self._log_database.view('pypeline_view/latest_values',
                                         group_level=2)

        for reading in latest:
            channel = reading['key']
            if not channel in channels:
                continue
            ch_val = reading['value']['cal_val']
            ch_time = reading['value']['timestamp']
            entrylist = ch_val.split()
            update = []
            for snip in entrylist:
                try:
                    update.append('%.4E' % float(snip))
                except ValueError:
                    update.append(snip)
            loggers_dict[channel] = {'value': " ".join(update),
                                     'time': ch_time}

        return loggers_dict

    def LogValue(self, sensor, uncal_val, cal_val, timestamp):
        '''
            <sensor> is the atom for the sensor being logged
            <uncal_val> is the uncalibrated value string
            <cal_val> is the calibrated value string
            <timestamp> is a datetime object
        '''
        result = DripResponse(self._log_database, uuid4().hex)
        if isinstance(timestamp, datetime):
            timestamp = timestamp.strftime(time_format)
        log_doc = {
            '_id': result['_id'],
            'sensor_name': sensor,
            'timestamp_localstring': timestamp,
            'uncalibrated_value': str(uncal_val),
            'calibrated_value': str(cal_val),
        }
        self._log_database.save(log_doc)
        return result
