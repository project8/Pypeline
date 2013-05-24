import matplotlib
matplotlib.use('TkAgg')

#standard libs
from sys import version_info, exit
if version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk
from datetime import datetime, timedelta

#3rd party libs
from numpy import arange, sin, cos, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure

#local libs

class channel_vs_channel:
    '''
    '''

    def __init__(self, interface, toplevel=False, channelx='linear_encoder',
                 channely='hall_probe_voltage',
                 start_t=datetime(2013, 5, 13, 12, 10, 0),#default should become false
                 stop_t=datetime(2013, 5, 13, 12, 20, 0)):#default should become false
        '''
        '''
        self.pype = interface
        self.formatstr = '%Y-%m-%d %H:%M:%S'
        self.channelx = channelx
        self.channely = channely
        self.start_t = start_t
        self.stop_t = stop_t
        if toplevel:
            self.toplevel = toplevel
        else:
            self.toplevel = Tk.Tk()
        self.SetupCanvas()
        self.MakePlot()
        if not toplevel:
            Tk.mainloop()

    def SetStart(self, start_time=False):
        '''
        '''
        if not start_time:
            start_time = datetime.now() - timedelta(hours=3)
        self.start_t = start_time

    def SetStop(self, stop_time=False):
        '''
        '''
        if not stop_time:
            stop_time = datetime.now()
        self.stop_t = stop_time

    def SetupCanvas(self):
        '''
        '''
        self.figure = Figure()
        self.subfigure = self.figure.add_subplot(1,1,1)

    def MakePlot(self):
        '''
        '''
        self.subfigure.cla()
        xdata = arange(0,1,.1)
        ydata = [sin(2*pi*x) for x in xdata]
        y2data = [cos(2*pi*x) for x in xdata]

        self.subfigure.plot(xdata, ydata)
        self.subfigure.set_title(self.channely + ' vs ' + self.channelx +
                                 '\n from ' +
                                 self.start_t.strftime(self.formatstr) +
                                 ' to ' +
                                 self.stop_t.strftime(self.formatstr))
        self.subfigure.set_xlabel(self.channelx.replace('_',' '))
        self.subfigure.set_ylabel(self.channely.replace('_',' '))
        self.subfigure.plot(xdata, y2data)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.toplevel)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0, column=0)

    def Update(self):
        '''
        '''
        self.subfigure.cla()
        self.xdat = pype.GetTimeSeries(self.channelx,
                                       self.start_t.strftime(self.formatstr),
                                       self.stop_t.strftime(self.formatstr))
        self.ydat = pype.GetTimeSeries(self.channely,
                                       self.start_t.strftime(self.formatstr),
                                       self.stop_t.strftime(self.formatstr))
