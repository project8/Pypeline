from __future__ import print_function

import matplotlib
matplotlib.use('TkAgg')

#standard libs
from sys import version_info, exit
if version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import StringVar, IntVar, Label, OptionMenu, Entry, Button
    from tkFileDialog import asksaveasfilename
else:
    import tkinter as Tk
    from tkinter import StringVar, IntVar, Label, OptionMenu, Entry, Button
    from tkFileDialog import asksaveasfilename
from ttk import Notebook, Frame
from tkMessageBox import showwarning
from datetime import datetime, timedelta

#3rd party libs
from numpy import arange, sin, cos, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import dates

#local libs

class channel_plot:
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
        self.plot_dicts = {}
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
        self.time_interval=[self.start_t.get(), self.stop_t.get()]
        if toplevel:
            self.toplevel = toplevel
        else:
            self.toplevel = Tk.Tk()
        self.status_var = StringVar(value='initializing')
        self._SetupCanvas()
        self.BuildGui()
        if not toplevel:
            Tk.mainloop()

    def _SetupCanvas(self):
        '''
        '''
        self.figure = Figure()
        self.figure.subplots_adjust(left=0.15, bottom=0.2)
        self.subfigure = []
        self.notebook = Notebook(self.toplevel)
        self.notebook.grid(row=1, column=1, rowspan=3, columnspan=3,
                           sticky='nsew')
        #self._AddSubplot()

    def _AddSubplot(self):
        '''
        '''
        plotnum = len(self.notebook.tabs())
        self.plot_dicts[plotnum]={}
        frame = Frame(self.notebook)
        frame.pack(side='top', fill='both', expand='y')
        self.plot_dicts[plotnum]['xname']=StringVar(value='None')
        self.plot_dicts['xunits'] = False
        self.plot_dicts[plotnum]['yname']=StringVar(value='None')
        self.plot_dicts['yunits'] = False
        self.subfigure.append(self.figure.add_subplot(1,1,1))
        Label(frame, text='X Channel').grid(row=0, column=0)
        Label(frame, text='Y Channel').grid(row=1, column=0)
        OptionMenu(frame, self.plot_dicts[plotnum]['xname'],
                   "None", "time", *self.pype.ListWithProperty('logging')
                   ).grid(row=0, column=1, sticky='ew')
        OptionMenu(frame, self.plot_dicts[plotnum]['yname'],
                   "None", *self.pype.ListWithProperty('logging')
                   ).grid(row=1, column=1, sticky='ew')
        self.notebook.add(frame, text='line:'+str(plotnum))

    def _SetStart(self, event, isFirst=True):
        '''
            Note: event is automatically passed in by the binding, but unused
        '''
        try:
            start_time = datetime.strptime(self.start_t.get(), self.formatstr)
            stop = datetime.strptime(self.stop_t.get(), self.formatstr)
            assert (start_time < stop)
            self.time_interval[0] = self.start_t.get()
            if isFirst:
                self._SetStop(event, isFirst=False)
            self.Update()
        except ValueError:
            showwarning('Warning', 'Format must match YYYY-MM-DD HH:MM:SS')
            self.start_t.set(self.time_interval[0])
        except AssertionError:
            if isFirst:
                self._SetStop(event=None, isFirst=False)
            else:
                showwarning('Warning', 'Start time must be before stop time')
                self.start_t.set(self.time_interval[0])

        except:
            raise

    def _SetStop(self, event, isFirst=True):
        '''
            Note: event is automatically passed in by the binding, but unused
        '''
        try:
            stop_time = datetime.strptime(self.stop_t.get(), self.formatstr)
            start = datetime.strptime(self.start_t.get(), self.formatstr)
            assert (start < stop_time)
            self.time_interval[1] = self.stop_t.get()
            if isFirst:
                self._SetStart(event, isFirst=False)
            self.Update()
        except ValueError:
            showwarning('Warning', 'Format must match YYYY-MM-DD HH:MM:SS')
            self.stop_t.set(self.time_interval[1])
        except AssertionError:
            if isFirst:
                self._SetStart(event=None, isFirst=False)
            else:
                showwarning('Warning', 'Start time must be before stop time')
                self.stop_t.set(self.time_interval[1])
        except:
            raise

    def BuildGui(self):
        '''
        '''
        self.removei = IntVar(value=0)
        Button(self.toplevel, text="Add Line", command=self._AddSubplot
               ).grid(row=0, column=1)
        self._AddSubplot()

        Label(self.toplevel, text='Start Time').grid(row=4, column =1)
        start_entry = Entry(self.toplevel, textvariable=self.start_t)
        start_entry.bind('<Return>', self._SetStart)
        start_entry.bind('<KP_Enter>', self._SetStart)
        start_entry.grid(row=4, column=2, columnspan=2)

        Label(self.toplevel, text='Stop Time').grid(row=5, column =1)
        stop_entry = Entry(self.toplevel, textvariable=self.stop_t)
        stop_entry.bind('<Return>', self._SetStop)
        stop_entry.bind('<KP_Enter>', self._SetStop)
        stop_entry.grid(row=5, column=2, columnspan=2)


        Button(self.toplevel, text="Update All", command=lambda: self.Update(tab='All')
               ).grid(row=6, column=1)
        Button(self.toplevel, text="Save", command=self.SaveFigure
               ).grid(row=6, column=2)
        self.status_var.set('done')

        Label(self.toplevel, textvariable=self.status_var).grid(row=11, column=2)

    def Update(self, tab='All'):
        '''
            Call whatever sequence is needed to update local data and redraw the plot
        '''
        self.status_var.set('updating')
        if tab == 'All':
            tab = range(len(self.notebook.tabs()))
            self.subfigure[0].cla()
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
        if self.plot_dicts[tab]['xname'].get() == 'time':
            self.subfigure[tab].plot_date(self.xdata, self.ydata, fmt='o-')
            self.subfigure[tab].set_xticklabels(self.subfigure[tab].get_xticklabels(), rotation=-45)
            self.subfigure[tab].xaxis.set_major_formatter(dates.DateFormatter(
                "%m/%d %H:%M"))
        else:
            self.subfigure[tab].plot(self.xdata, self.ydata)
        self.subfigure[tab].set_title(self.plot_dicts[tab]['yname'].get() + ' vs ' +
                                 self.plot_dicts[tab]['xname'].get() +
                                 '\n from ' + self.time_interval[0] +
                                 ' to ' + self.time_interval[1])
        self.subfigure[tab].set_xlabel(self.plot_dicts[tab]['xname'].get().replace('_',' '))
        self.subfigure[tab].set_ylabel(self.plot_dicts[tab]['yname'].get().replace('_',' '))

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.toplevel)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=10)

    def _UpdateData(self, tab=0):
        '''
        '''
        try:
            ychdat = self.pype.GetTimeSeries(self.plot_dicts[tab]['yname'].get(),
                                             self.time_interval[0],
                                             self.time_interval[1])
            if self.plot_dicts[tab]['xname'].get() == 'time':
                xchdat = (ychdat[0], ychdat[0], 'time' * len(ychdat[0]))
            else:
                xchdat = self.pype.GetTimeSeries(self.plot_dicts[tab]['xname'].get(),
                                                 self.time_interval[0],
                                                 self.time_interval[1])
            if tab > 0 and ychdat[0]:
                assert xchdat[2][0] == self.plot_dicts['xunit'], 'x units'
                assert ychdat[2][0] == self.plot_dicts['yunit'], 'y units'
           
            self.xdata = []
            self.ydata = []
            if ychdat[0]:
                for tx, x in zip(xchdat[0], xchdat[1]):
                    xtmp = False
                    ytmp = False
                    dt = timedelta(seconds=60)
                    for ty, y in zip(ychdat[0], ychdat[1]):
                        if abs(ty - tx) < dt:
                            dt = abs(ty - tx)
                            xtmp = x
                            ytmp = y
                    if xtmp and ytmp:
                        self.xdata.append(xtmp)
                        self.ydata.append(ytmp)
                [self.xdata, self.ydata] = zip(*sorted(zip(self.xdata, self.ydata)))
                self.plot_dicts['xunit'] = xchdat[2][0]
                self.plot_dicts['yunit'] = ychdat[2][0]
        except AssertionError as e:
            print('*'*60, '\n the', e[0], 'do not match the 0th line', '*'*60)

    def SaveFigure(self):
        '''
        '''
        file_extensions = [('vectorized','.eps'),('adobe','.pdf'),('image','.png'),('all','.*')]
        outfile = asksaveasfilename(defaultextension='.pdf', filetypes=file_extensions)
        self.figure.savefig(outfile)
