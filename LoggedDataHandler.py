from datetime import datetime, timedelta
from couchdb import Server as CouchServer
import numpy as np
import matplotlib.pyplot as plt

class LoggedDataHandler:
    '''
        Class to plot data logged on CouchDB.
    '''

    def __init__(self, dripline_url="http://127.0.0.1:5984"):
        '''
            Connects to data server and looks for logged data.
        '''
        self._server = CouchServer(dripline_url)
        self.times = []
        self.values = []
        self.units = []
        if (self._server.__contains__('dripline_logged_data')):
            self._logged_data = self._server['dripline_logged_data']
        else:
            raise UserWarning('The dripline logged data database was not found!')

    def Get(self, sensor, start, stop):
        '''
            Retrieve data logged on CouchDB in a specified window and return it
            as a numpy array.

            Inputs:
                <sensor> is the sensor whose logged data you would like to
                         retrieve
                <start> is the timestamp of the beginning of the log you would
                        like to retrieve
                <stop> is the timestamp of the end of the log you would like to
                       retrieve
        '''
        timelist = []
        valuelist = []
        unitlist = []
        for row in self._logged_data.view('log_access/all_logged_data'):
            timestamp = datetime.strptime(row.value['timestamp_localstring'], "%Y-%m-%d %H:%M:%S")
            if row.value['sensor_name'] == sensor:
                if timestamp >= start and timestamp <= stop:
                    timelist.append(timestamp)
                    valuelist.append(float(row.value['calibrated_value'].split()[0]))
                    unitlist.append(str(row.value['calibrated_value'].split()[1]))
        self.times.append(timelist)
        self.values.append(valuelist)
        self.units.append(unitlist)
        result = [self.times,self.values,self.units]
        return result

    def Plot(self, sensors=False, start=datetime.today()-timedelta(hours=3), stop=datetime.today()):
        '''
            Creates a plot of logged data.

            Inputs:
                <sensors> is either a string or a list of strings. These are
                          the names of the sensors to plot. If this is left
                          blank, a list of all sensors for which there exists
                          data will be printed.
                <start> is either a datetime object or a string formatted the
                        same as a CouchDB timestamp. This is the start of the
                        plotting window.
                <stop> is either a datetime object or a string formatted the
                       same as a CouchDB timestamp. This is the end of the
                       plotting window.
        '''

        if not sensors:
            self.EligibleSensors()
        else:    
            if isinstance(start,str):
                start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            if isinstance(stop,str):
                stop = datetime.strptime(stop, "%Y-%m-%d %H:%M:%S")
            fig = plt.figure()
            ax = fig.add_subplot(111)

            if isinstance(sensors,str):
                sensors = [sensors]

            if isinstance(sensors,list):
                for sensor in sensors:
                    data = self.Get(sensor, start, stop)
                    ax.plot(data[-1][0],data[-1][1],label=sensor)
                    fig.autofmt_xdate()

            plt.xlabel('Time (Hours)')
            plt.ylabel('Value (' + data[-1][2][0] + ')')
            plt.title('Sensor Readout')
            plt.legend()
            plt.show()

    def Save(self, filename):
        f = open(filename, 'w')
        f.write(str([self.times, self.values, self.units]))
        f.close()

    def EligibleSensors(self):
        '''
            Print names of eligible sensors.
        '''
        sensors = []
        for row in self._logged_data.view('log_access/all_logged_data'):
            if row.value['sensor_name'] not in sensors:
                sensors.append(row.value['sensor_name'])
        print sensors
