'''
    A class for plotting and other interactions with logged data.

    This module/class has many more dependencies than the rest of pypeline.
'''

#Standard libs
from warnings import warn
from datetime import datetime, timedelta

#3rd party libs
from couchdb import Server as CouchServer
from numpy import exp, array
from scipy import optimize
from matplotlib import pyplot as plt

class LoggedDataHandler:
    '''
        Class to plot data logged on CouchDB.
    '''

    def __init__(self, couch_url="http://127.0.0.1:5984"):
        '''
            Connects to data server and looks for logged data.

            Inputs:
            <couch_url> (string) URL of CouchDB server
        '''
        self._server = CouchServer(couch_url)
        self.times = {}
        self.values = {}
        self.units = {}
        if (self._server.__contains__('dripline_logged_data')):
            self._logged_data = self._server['dripline_logged_data']
        else:
            raise UserWarning('The dripline logged data database was not found!')

    def Get(self, sensor, start, stop):
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
        '''
        timelist = []
        valuelist = []
        unitlist = []
        for row in self._logged_data.view('log_access/all_logged_data', startkey=start, endkey=stop):
            timestamp = datetime.strptime(row.value['timestamp_localstring'], "%Y-%m-%d %H:%M:%S")
            if row.value['sensor_name'] == sensor:
                timelist.append(timestamp)
                valuelist.append(float(row.value['calibrated_value'].split()[0]))
                unitlist.append(str(row.value['calibrated_value'].split()[1]))
        self.times[sensor] = timelist
        self.values[sensor] = valuelist
        self.units[sensor] = unitlist
        result = [self.times,self.values,self.units]
        return result

    def Plot(self, sensors=False, dynamupdate=False, start=datetime.today()-timedelta(hours=3), stop=datetime.today()):
        '''
            Creates a plot of logged data.

            Inputs:
                <sensors> (string or list of strings) These are
                          the names of the sensors to plot. If this is left
                          blank, a list of all sensors for which there exists
                          data will be printed.
                <start> (datetime object or string formatted the same as a
                        CouchDB timestamp) This is the start of the plotting
                        window.
                <stop> (datetime object or string formatted the same as a
                       CouchDB timestamp) This is the end of the plotting
                       window.
        '''
        if not sensors:
            self.EligibleSensors()
        else:
            if isinstance(start,datetime):
                start = start.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(stop,datetime):
                stop = stop.strftime("%Y-%m-%d %H:%M:%S")
            fig = plt.figure()
            ax = fig.add_subplot(111)

            if isinstance(sensors,str):
                sensors = [sensors]

            if isinstance(sensors,list):
                for sensor in sensors:
                    data = self.Get(sensor, start, stop)
                    line1 = ax.plot(data[0][sensor],data[1][sensor],label=sensor)
                    fig.autofmt_xdate()

            while dynamupdate:
                try:
                    for sensor in sensors:
                        ax.clear()
                        data = self.Get(sensor, start, stop)
                        line1 = ax.plot(data[0][sensor],data[1][sensor],label=sensor)
                        fig.autofmt_xdate()
                        plt.xlabel('Time (Hours)')
                        plt.ylabel('Value (' + data[2][sensor][0] + ')')
                        plt.title('Sensor Readout')
                        plt.legend()
                        fig.canvas.draw()
                except KeyboardInterrupt:
                    break
            if not dynamupdate:
                plt.xlabel('Time (Hours)')
                plt.ylabel('Value (' + data[2][sensor][0] + ')')
                plt.title('Sensor Readout')
                plt.legend()
                plt.show()

    def Save(self, filename):
        '''
            Saves all data that has been stored in object in specified file.

            Inputs:
            <filename> (string) Complete name of file where data will be saved.
        '''
        f = open(filename, 'w')
        f.write(str([self.times, self.values, self.units]))
        f.close()

    def Fit(self, sensor, fitfunc=False, p0=[0,1]):
        '''
            Fits data pulled from CouchDB to an arbitrary function using least-
            squares regression.

            Inputs:
            <sensor> (string) The sensor with data to be fitted.
            <fitfunc> (callable or string) A fitting function of the form (does
            not have to be linear):
                      fitfunc = lambda p, x: p[0] + p[1]*x
                      This variable also accept the keywords 'linear' and
                      'exponential'
            <p0> (list) A list of guess values for the fit parameters
        '''
        if not fitfunc or fitfunc == 'linear':
            fitfunc = lambda p,x: p[0]+p[1]*x
            print 'fitfunc = lambda p,x: p[0]+p[1]*x'
            p0 = [0,1]
        if fitfunc == 'exponential':
            fitfunc = lambda p,x: p[0]+p[1]*np.exp(p[2]*x)
            print 'fitfunc = lambda p,x: p[0]+p[1]*np.exp(p[2]*x)'
            p0 = [1,-1,-1]
        errfunc = lambda p,x,y: fitfunc(p,x) - y
        x = []
        temp = self.times[sensor]
        for i in range(len(self.times[sensor])):
            x.append(temp[i].hour + temp[i].minute/60.0 + temp[i].second/3600.0)
        x = np.array(x)
        y = np.array(self.values[sensor])
        p1, success = optimize.leastsq(errfunc, p0[:], args=(x,y))
        plt.plot(x, y, "bo", x, fitfunc(p1,x), "r-")
        print p1
        plt.show()

    def EligibleSensors(self):
        '''
            Print names of eligible sensors.
        '''
        sensors = []
        for row in self._logged_data.view('log_access/all_logged_data'):
            if row.value['sensor_name'] not in sensors:
                sensors.append(row.value['sensor_name'])
        print sensors