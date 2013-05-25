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
from ttk import Notebook, Frame
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
        self.channelx = []
        self.channely = []
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
        self._SetupCanvas()
        self._UpdateData()
        self.BuildGui()
        if not toplevel:
            Tk.mainloop()

    def _SetupCanvas(self):
        '''
        '''
        self.figure = Figure()
        self.subfigure = self.figure.add_subplot(1,1,1)
        self.notebook = Notebook(self.toplevel)
        self.notebook.grid(row=0, column=1, rowspan=3, columnspan=3,
                           sticky='nsew')
        self._AddSubplot()

    def _AddSubplot(self):
        '''
        '''
        plotnum = len(self.notebook.tabs())
        frame = Frame(self.notebook)
        frame.pack(side='top', fill='both', expand='y')
        self.channelx.append(StringVar(value='hall_probe_voltage'))
        self.channely.append(StringVar(value='hall_probe_voltage'))
        Label(frame, text='X Channel').grid(row=0, column=0)
        Label(frame, text='Y Channel').grid(row=1, column=0)
        OptionMenu(frame, self.channelx[plotnum],
                   *self.pype.ListWithProperty('logging')
                   ).grid(row=0, column=1, sticky='ew')
        OptionMenu(frame, self.channely[plotnum],
                   *self.pype.ListWithProperty('logging')
                   ).grid(row=1, column=1, sticky='ew')
        Button(frame, text='Update', command=lambda: self.Update(tab=plotnum)
               ).grid(row=2, column=0, sticky='ew')
        self.notebook.add(frame, text='line:'+str(plotnum))

    def _SetStart(self, start_time=False):
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
        self._UpdateData()

    def _SetStop(self, stop_time=False):
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
        self._UpdateData()

    def BuildGui(self):
        '''
        '''
        Label(self.toplevel, text='Start Time').grid(row=3, column =1)
        start_entry = Entry(self.toplevel, textvariable=self.start_t)
        #start_entry.bind('<Return>', self.Update)
        start_entry.grid(row=3, column=2, columnspan=2)

        Label(self.toplevel, text='Stop Time').grid(row=4, column =1)
        stop_entry = Entry(self.toplevel, textvariable=self.stop_t)
        #stop_entry.bind('<Return>', self.Update)
        stop_entry.grid(row=4, column=2, columnspan=2)

        Label(self.toplevel, textvariable=self.status_var).grid(row=11, column=2)

        Button(self.toplevel, text="Update All", command=lambda: self.Update(tab='All')
               ).grid(row=5, column=1)
        Button(self.toplevel, text="Save", command=self.SaveFigure
               ).grid(row=5, column=2)
        Button(self.toplevel, text="Add Line", command=self._AddSubplot
               ).grid(row=5, column=3)
        self.status_var.set('done')

    def Update(self, tab='All'):
        '''
            Call whatever sequence is needed to update local data and redraw the plot
        '''
        self.status_var.set('updating')
        if tab == 'All':
            self.subfigure.cla()
            tab = range(len(self.notebook.tabs()))
        elif isinstance(tab, int):
            tab = [tab]
        else:
            raise ValueError('tab should be "All" or an int')
        for tabi in tab:
            self._UpdateData(tab=tabi)
            self._MakePlot(tab=tabi)
        self.status_var.set('done')

    def _MakePlot(self, tab=0):
        '''
        '''
        self.subfigure.plot(self.xdata, self.ydata)
        self.subfigure.set_title(self.channely[tab].get() + ' vs ' + self.channelx[tab].get() +
                                 '\n from ' + self.start_t.get() +
                                 ' to ' + self.stop_t.get())
        self.subfigure.set_xlabel(self.channelx[tab].get().replace('_',' '))
        self.subfigure.set_ylabel(self.channely[tab].get().replace('_',' '))

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.toplevel)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=10)

    def _UpdateData(self, tab=0):
        '''
        '''
        self.xchdat = self.pype.GetTimeSeries(self.channelx[tab].get(),
                                         self.start_t.get(),
                                         self.stop_t.get())
        self.ychdat = self.pype.GetTimeSeries(self.channely[tab].get(),
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
