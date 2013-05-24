import matplotlib
matplotlib.use('TkAgg')

#standard libs
from sys import version_info, exit
if version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import StringVar, Label, OptionMenu, Entry, Button
    from tkFileDialog import asksaveasfilename
else:
    import tkinter as Tk
    from tkinter import StringVar, Label, OptionMenu, Entry, Button
    from tkFileDialog import asksaveasfilename
from datetime import datetime, timedelta

#3rd party libs
from numpy import arange, sin, cos, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure

#local libs

class channel_vs_channel:
    '''
    '''

    def __init__(self, interface, toplevel=False,
                 channelx='hall_probe_voltage',#default should become ''
                 channely='hall_probe_voltage',#default should become ''
                 start_t=datetime(2013, 5, 13, 12, 10, 0),#default should become false
                 stop_t=datetime(2013, 5, 13, 12, 20, 0)):#default should become false
        '''
        '''
        self.pype = interface
        self.formatstr = '%Y-%m-%d %H:%M:%S'
        self.channelx = [StringVar(value=channelx)]
        self.channely = [StringVar(value=channely)]
        if isinstance(start_t, datetime):
            self.start_t = StringVar(value=start_t.strftime(self.formatstr))
        elif isinstance(start_t, str):
            self.start_t = StringVar(value=start_t)
        else:
            raise TypeError('start_t must be string or datetime')
        if isinstance(stop_t, datetime):
            self.stop_t = StringVar(value=stop_t.strftime(self.formatstr))
        elif isinstance(stop_t, str):
            self.stop_t = StringVar(value=stop_t)
        else:
            raise TypeError('stop_t must be string or datetime')
        #self.start_t = start_t
        #self.stop_t = stop_t
        if toplevel:
            self.toplevel = toplevel
        else:
            self.toplevel = Tk.Tk()
        self.status_var = StringVar(value='initializing')
        self.SetupCanvas()
        self.UpdateData()
        self.BuildGui()
        if not toplevel:
            Tk.mainloop()

    def SetStart(self, start_time=False):
        '''
        '''
        if not start_time:
            start_time = datetime.now() - timedelta(hours=3)
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, self.formatstr)
        stop = datetime.strptime(self.stop_t.get(), self.formatstr)
        if start_time > stop:
            print('start time must be before stop time')
            return
        self.start_t.set(start_time.strftime(self.formatstr))
        self.UpdateData()

    def SetStop(self, stop_time=False):
        '''
        '''
        if not stop_time:
            stop_time = datetime.now()
        if isinstance(stop_time, str):
            stop_time = datetime.strptime(stop_time, self.formatstr)
        start = datetime.strptime(self.start_t.get(), self.formatstr)
        if stop_time < start:
            print('stop time must be after start time')
            return
        self.stop_t.set(stop_time.strftime(self.formatstr))
        self.UpdateData()

    def BuildGui(self):
        '''
        '''
        Label(self.toplevel, text='X Channel').grid(row=0, column =1)
        OptionMenu(self.toplevel, self.channelx[0],
                   *self.pype.ListWithProperty('logging')
                   ).grid(row=0, column=2, sticky='ew')

        Label(self.toplevel, text='Y Channel').grid(row=1, column =1)
        OptionMenu(self.toplevel, self.channely[0],
                   *self.pype.ListWithProperty('logging')
                   ).grid(row=1, column=2, sticky='ew')

        Label(self.toplevel, text='Start Time').grid(row=2, column =1)
        Entry(self.toplevel, textvariable=self.start_t).grid(row=2, column=2)

        Label(self.toplevel, text='Stop Time').grid(row=3, column =1)
        Entry(self.toplevel, textvariable=self.stop_t).grid(row=3, column=2)

        Label(self.toplevel, textvariable=self.status_var).grid(row=11, column=2)

        Button(self.toplevel, text="Update", command=self.Update
               ).grid(row=4, column=1)
        Button(self.toplevel, text="Save", command=self.SaveFigure
               ).grid(row=4, column=2)
        self.status_var.set('done')

    def SetupCanvas(self):
        '''
        '''
        self.figure = Figure()
        self.subfigure = self.figure.add_subplot(1,1,1)

    def Update(self):
        '''
            Call whatever sequence is needed to update local data and redraw the plot
        '''
        self.status_var.set('updating')
        self.UpdateData()
        self.MakePlot()
        self.status_var.set('done')

    def MakePlot(self):
        '''
        '''
        self.subfigure.cla()

        self.subfigure.plot(self.xdata, self.ydata)
        self.subfigure.set_title(self.channely[0].get() + ' vs ' + self.channelx[0].get() +
                                 '\n from ' + self.start_t.get() +
                                 ' to ' + self.stop_t.get())
        self.subfigure.set_xlabel(self.channelx[0].get().replace('_',' '))
        self.subfigure.set_ylabel(self.channely[0].get().replace('_',' '))

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.toplevel)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=10)

    def UpdateData(self):
        '''
        '''
        self.subfigure.cla()
        self.xchdat = self.pype.GetTimeSeries(self.channelx[0].get(),
                                         self.start_t.get(),
                                         self.stop_t.get())
        self.ychdat = self.pype.GetTimeSeries(self.channely[0].get(),
                                         self.start_t.get(),
                                         self.stop_t.get())
        self.xdata = []
        self.ydata = []
        for tx, x in zip(self.xchdat[0], self.xchdat[1]):
            xtmp = False
            ytmp = False
            dt = timedelta(seconds=60)
            for ty, y in zip(self.ychdat[0], self.ychdat[1]):
                if abs(ty - tx) < dt:
                    dt = abs(ty - tx)
                    xtmp = x
                    ytmp = y
            if xtmp and ytmp:
                self.xdata.append(xtmp)
                self.ydata.append(ytmp)
        if self.xdata and self.ydata:
            [self.xdata, self.ydata] = zip(*sorted(zip(self.xdata, self.ydata)))

    def SaveFigure(self):
        '''
        '''
        file_extensions = [('vectorized','.eps'),('adobe','.pdf'),('image','.png'),('all','.*')]
        outfile = asksaveasfilename(defaultextension='.pdf', filetypes=file_extensions)
        self.figure.savefig(outfile)
