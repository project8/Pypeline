'''
    A class for plotting and other interactions with logged data.

    This module/class has many more dependencies than the rest of pypeline.
'''

#Standard libs
from warnings import warn
from datetime import datetime, timedelta
import time

#3rd party libs
from couchdb import Server as CouchServer
import numpy as np
from scipy import optimize
#import Gnuplot
import usegnuplot

class LoggedDataHandler_Gnuplot:
    '''
        Class to plot data logged on CouchDB. The constructor requires the URL
        of the CouchDB server. See plotting_example.py in scripts/examples for
        more help.
    '''
            

    def __init__(self, couch_url="http://127.0.0.1:5984"):
        '''
            Connects to data server and looks for logged data.

            Inputs:
            <couch_url> (string) URL of CouchDB server
        '''
        self.g=usegnuplot.Gnuplot()
        self._server = CouchServer(couch_url)
        self.times = {}
        self.values = {}
        self.units = {}
        if (self._server.__contains__('dripline_logged_data')):
            self._logged_data = self._server['dripline_logged_data']
        else:
            raise UserWarning('The dripline logged data database was not found!')

    def Get(self, start, stop):
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
        times = {}
        values = {}
        units = {}
        for row in self._logged_data.view('log_access/all_logged_data', startkey=start, endkey=stop):
            sensor=row.value['sensor_name']
            if times.get(sensor)==None:
                times[sensor]=[]
                values[sensor]=[]
                units[sensor]=[]
            #timestamp = datetime.strptime(row.value['timestamp_localstring'], "%Y-%m-%d %H:%M:%S")
            #times[sensor].append(time.mktime(timestamp.timetuple()))
            times[sensor].append(row.value['timestamp_localstring'])
            values[sensor].append(float(row.value['calibrated_value'].split()[0]))
            units[sensor].append(str(row.value['calibrated_value'].split()[1]))
        result = [times, values, units]
        return result

    def Plot(self, sensors=False, dynamupdate=True, start=datetime.today()-timedelta(hours=3), stop=False):
        '''
            Creates a plot of logged data.

            Inputs:
                <sensors> (string or list of strings) These are
                          the names of the sensors to plot. If this is left
                          blank, a list of all sensors for which there exists
                          data from the past 3 hours will be printed.
                <dynamupdate> (Boolean) Turns on or off dynamic updating of
                              plots.
                <start> (datetime object or string formatted the same as a
                        CouchDB timestamp) This is the start of the plotting
                        window.
                <stop> (datetime object or string formatted the same as a
                       CouchDB timestamp) This is the end of the plotting
                       window. If this is changed from its default, dynamic
                       updating cannot be enabled.
        '''
        if not sensors:
            return self.EligibleLoggers()
        else:
            if not stop:
                stop = datetime.today()
            else:
                dynamupdate = False
            if isinstance(start, datetime):
                start = start.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(stop, datetime):
                stop = stop.strftime("%Y-%m-%d %H:%M:%S")

            if isinstance(sensors, str):
                sensors = [sensors]

            data = self.Get(start, stop)
            plotsets = []
            argsets = []
            for sensor in sensors:
                plotsets.append(zip(data[0][sensor],data[1][sensor]))
                argsets.append("using 1:3 with lines title \""+sensor+"\"")

            self.g.gp("set xdata time")
            self.g.gp("set timefmt \"%Y-%m-%d %H:%M:%S\"")
            self.g.gp("set format x \"%H:%M\"")
            self.g.gp("set ylabel \""+data[2][sensors[0]][0]+"\"")
#           self.g.gp("set xlabel \"Time\"")
#			self.g.plotMany(plotsets,argsets)

#                self.FormatPlots(sensor,fig,ax)
#                plt.show()

    def Save(self, filename):
        '''
            Saves all data that has been stored in object in specified file.

            Inputs:
            <filename> (string) Complete name of file where data will be saved.
        '''
        f = open(filename, 'w')
        f.write(str([self.times, self.values, self.units]))
        f.close()

    def Fit(self, sensor, fitfunc=False, p0=[0, 1]):
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
            print('fitfunc = lambda p,x: p[0]+p[1]*x')
            p0 = [0,1]
        if fitfunc == 'exponential':
            fitfunc = lambda p,x: p[0]+p[1]*np.exp(p[2]*x)
            print('fitfunc = lambda p,x: p[0]+p[1]*np.exp(p[2]*x)')
            p0 = [1, -1, -1]
        errfunc = lambda p,x,y: fitfunc(p, x) - y
        x = []
        temp = self.times[sensor]
        for i in range(len(self.times[sensor])):
            x.append(temp[i].hour + temp[i].minute/60.0 + temp[i].second/3600.0)
        x = np.array(x)
        y = np.array(self.values[sensor])
        p1, success = optimize.leastsq(errfunc, p0[:], args=(x, y))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        points = plt.plot(x, y, "bo", label=sensor)
        fit = plt.plot(x, fitfunc(p1, x), "r-", label='fit')
        self.FormatPlots(sensor,fig,ax)
        print(p1)
        plt.show()

    def EligibleLoggers(self, start=datetime.today()-timedelta(hours=3), stop=datetime.today()):
        '''
            Print names of sensors with logged data in a certain timeframe.
            Searches the last three hours by default.

            Inputs:
            <start> (datetime object or a CouchDB formatted timestamp) Sets the
                    beginning of the search window. If set to False, this method
                    will print out all loggers which have logged data.
            <stop> (datetime object or a CouchDB formatted timestamp) Sets the
                   end of the search window. 
        '''
        if not start:
            sensors = []
            for row in self._logged_data.view('log_access/logger_list', reduce=True, group_level=2):
                sensors.append(row.key)
            return sensors
        else:
            sensors = []
            if isinstance(start, datetime):
                start = start.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(stop, datetime):
                stop = stop.strftime("%Y-%m-%d %H:%M:%S")
            for row in self._logged_data.view('log_access/all_logged_data', startkey=start, endkey=stop):
                if row.value['sensor_name'] not in sensors:
                    sensors.append(row.value['sensor_name'])
            return sensors

    def FormatPlots(self,sensor,fig,ax):
        '''
            Internal
        '''
        fig.autofmt_xdate()
        plt.xlabel('Time (Hours)')
        plt.ylabel('Value (' + self.units[sensor][0] + ')')
        plt.title('Sensor Readout')
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
                  fancybox=True, shadow=True, ncol=2)

    def BeginDataMonitoring(self):
        '''
        	start getting data so I can update plots
        '''
        #get the last update sequence
        self.recent=self._logged_data.info()['update_seq']

    def UpdatePlots(self):
        changes=self._logged_data.changes(since=self.recent)
        self.recent=changes['last_seq']
        for changeset in changes['results']:
            doc=self._logged_data[changeset['id']]


