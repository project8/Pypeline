from __future__ import print_function

import matplotlib
matplotlib.use('TkAgg', warn=False)

#standard libs
from sys import version_info, exit
if version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import (StringVar, BooleanVar, IntVar, DoubleVar, Label,
                         OptionMenu, Entry, Button, Checkbutton)
    from tkFileDialog import asksaveasfilename
    from ttk import Notebook, Frame
    from tkMessageBox import showwarning
else:
    import tkinter as Tk
    from tkinter import (StringVar, BooleanVar, IntVar, DoubleVar, Label,
                         OptionMenu, Entry, Button, Checkbutton)
    from tkinter.filedialog import asksaveasfilename
    from tkinter.ttk import Notebook, Frame
    from tkinter.messagebox import showwarning
from datetime import datetime, timedelta

#3rd party libs
from numpy import arange, sin, cos, pi, array
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2TkAgg)
from matplotlib.figure import Figure
from matplotlib import dates, ticker

#local libs


class channel_plot:
    '''
    '''

    def __init__(self, interface, toplevel=False, start_t=False, stop_t=False):
        '''
        '''
        if not start_t:
            start_t = datetime.now() - timedelta(hours=2)
        if not stop_t:
            stop_t = datetime.now()
        self.update_pending = False
        self.pype = interface
        self._formatstr = '%Y-%m-%d %H:%M:%S'
        self.plot_dicts = {}
        if isinstance(start_t, datetime):
            self.start_t = StringVar(value=start_t.strftime(self._formatstr))
        elif isinstance(start_t, str):
            self.start_t = StringVar(value=start_t)
        else:
            raise TypeError('start_t must be string or datetime')
        if isinstance(stop_t, datetime):
            self.stop_t = StringVar(value=stop_t.strftime(self._formatstr))
        elif isinstance(stop_t, str):
            self.stop_t = StringVar(value=stop_t)
        else:
            raise TypeError('stop_t must be string or datetime')
        self.time_interval = [self.start_t.get(), self.stop_t.get()]
        self.ymin = DoubleVar()
        self.ymax = DoubleVar()
        if toplevel:
            self.toplevel = toplevel
        else:
            self.toplevel = Tk.Tk()
        self.status_var = StringVar(value='initializing')
        self._SetupCanvas()
        self._BuildGui()
        if not toplevel:
            Tk.mainloop()

    def _BuildGui(self):
        '''
        '''
        self.removei = IntVar(value=0)
        self.relative_start_time = BooleanVar(value=False)
        self.relative_stop_time = BooleanVar(value=False)
        self.continuous_updates = BooleanVar(value=False)
        self.ManualLimits = BooleanVar(value=False)
        self.ConnectedPts = BooleanVar(value=True)
        Button(self.toplevel, text="Add Line", command=self._AddSubplot
               ).grid(row=0, column=1)
        self._AddSubplot()
        Button(self.toplevel, text="Gas Line Temps", command=self._PlotGasLines
               ).grid(row=0, column=2)
        Button(self.toplevel, text="Amps+Cell Temps", command=self._PlotCell
               ).grid(row=0, column=3)

        Label(self.toplevel, text='Start Time').grid(row=4, column=1)
        start_entry = Entry(self.toplevel, textvariable=self.start_t)
        start_entry.bind('<Return>', self.Update)
        start_entry.bind('<KP_Enter>', self.Update, '+')
        start_entry.grid(row=4, column=2, columnspan=2)
        Checkbutton(self.toplevel, text='Hours ago',
                    variable=self.relative_start_time).grid(row=4, column=4,
                                                            sticky='W')

        Label(self.toplevel, text='Stop Time').grid(row=6, column=1)
        stop_entry = Entry(self.toplevel, textvariable=self.stop_t)
        stop_entry.bind('<Return>', self.Update)
        stop_entry.bind('<KP_Enter>', self.Update, '+')
        stop_entry.grid(row=6, column=2, columnspan=2)
        Checkbutton(self.toplevel, text='Now',
                    variable=self.relative_stop_time).grid(row=6, column=4,
                                                           sticky='W')

        Label(self.toplevel, text='Y limits (min-max)').grid(row=8, column=1)
        ymin = Entry(self.toplevel, textvariable=self.ymin)
        ymin.grid(row=8, column=2)
        ymin.bind('<Return>', self.Update)
        ymin.bind('<KP_Enter>', self.Update, '+')
        ymax = Entry(self.toplevel, textvariable=self.ymax)
        ymax.grid(row=8, column=3)
        ymax.bind('<Return>', self.Update)
        ymax.bind('<KP_Enter>', self.Update, '+')
        Checkbutton(self.toplevel, text='Manual Y-limits', variable=self.ManualLimits
                    ).grid(row=9, column=1)
        Checkbutton(self.toplevel, text='Connected Points', variable=self.ConnectedPts
                    ).grid(row=9, column=2)

        Button(self.toplevel, text="Update All", command=self.Update
               ).grid(row=10, column=1)
        Button(self.toplevel, text="Save", command=self.SaveFigure
               ).grid(row=10, column=2)
        Checkbutton(self.toplevel, text='Continuous (Button above to start)',
                    variable=self.continuous_updates
                    ).grid(row=11, column=1, columnspan=2)
        self.status_var.set('done')

        Label(self.toplevel, textvariable=self.status_var).grid(row=20,
                                                                column=1,
                                                                columnspan=2)

    def _SetupCanvas(self):
        '''
        '''
        self.figure = Figure()
        #self.figure.set_size_inches((4, 3), forward=True)
        self.figure.subplots_adjust(left=0.15, bottom=0.2)
        #self.subfigure = []
        self.subfigure = self.figure.add_subplot(1,1,1)
        self.notebook = Notebook(self.toplevel)
        self.notebook.grid(row=1, column=1, rowspan=3, columnspan=3, sticky='nsew')
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.toplevel)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=10)

    def _AddSubplot(self):
        '''
        '''
        plotnum = len(self.notebook.tabs())
        self.plot_dicts[plotnum] = {}
        frame = Frame(self.notebook)
        frame.pack(side='top', fill='both', expand='y')
        self.plot_dicts[plotnum]['xname'] = StringVar(value='None')
        self.plot_dicts['xunit'] = False
        self.plot_dicts[plotnum]['yname'] = StringVar(value='None')
        self.plot_dicts['yunit'] = False
        #self.subfigure.append(self.figure.add_subplot(1, 1, 1))
        Label(frame, text='X Channel').grid(row=0, column=0)
        Label(frame, text='Y Channel').grid(row=1, column=0)
        OptionMenu(frame, self.plot_dicts[plotnum]['xname'],
                   "None", "time", *self.pype.ListWithProperty('logging')
                   ).grid(row=0, column=1, sticky='ew')
        OptionMenu(frame, self.plot_dicts[plotnum]['yname'],
                   "None", *self.pype.ListWithProperty('logging')
                   ).grid(row=1, column=1, sticky='ew')
        self.notebook.add(frame, text='line:'+str(plotnum))

    def _SetStart(self, event=None, isFirst=True):
        '''
            Note: event is automatically passed in by the binding, but unused
        '''
        try:
            if self.relative_start_time.get():
                hours = float(self.start_t.get())
                start_time = datetime.now() - timedelta(hours=hours)
            else:
                start_time = datetime.strptime(self.start_t.get(),
                                               self._formatstr)
            stop = datetime.strptime(self.stop_t.get(), self._formatstr)
            assert (start_time < stop)
            self.time_interval[0] = start_time.strftime(self._formatstr)
            if isFirst:
                self._SetStop(event, isFirst=False)
            #self.Update() -- yikes, my tibbs, leads to infinite loops if you call set stop in update
        except ValueError:
            if self.relative_start_time.get():
                showwarning('Warning', 'Hours ago must be a float')
            else:
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

    def _SetStop(self, event=None, isFirst=True):
        '''
            Note: event is automatically passed in by the binding, but unused
        '''
        try:
            if self.relative_stop_time.get():
                stop_time = datetime.now()
            else:
                stop_time = datetime.strptime(self.stop_t.get(),
                                              self._formatstr)
            if self.relative_start_time.get():
                hours = float(self.start_t.get())
                start = datetime.now() - timedelta(hours=hours)
            else:
                start = datetime.strptime(self.start_t.get(), self._formatstr)
            assert (start < stop_time)
            self.time_interval[1] = stop_time.strftime(self._formatstr)
            if isFirst:
                self._SetStart(event, isFirst=False)
            #self.Update() -- yikes, my tibbs, leads to infinite loops if you call set stop in update
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

    def Update(self, event=None, tab='All', unpend=False):
        '''
            Call whatever sequence is needed to update local data and redraw
            the plot
        '''
        if unpend:
            self.update_pending = False
        self.status_var.set('updating')
        if tab == 'All':
            tab = range(len(self.notebook.tabs()))
            #self.subfigure.cla()
        elif isinstance(tab, int):
            tab = [tab]
        else:
            raise ValueError('tab should be "All" or an int')
        self._SetStart(event=None, isFirst=False)
        self._SetStop(event=None, isFirst=False)
        self.subfigure.clear()
        #git dat gibblit grayvy
        for tabi in tab:
            if tabi > len(self.subfigure.get_lines()):
                print('wtf')
            elif tabi == len(self.subfigure.get_lines()):
                self._UpdateData(tab=tabi)
                self._MakePlot(tab=tabi)
            else:
                self._UpdateExisting(tab=tabi)
                #this is where I just update the line
        #dont stop git it git it
        self.figure.legends = []
        self.figure.legend(*self.subfigure.get_legend_handles_labels())
        self.figure.legends[0].draggable(True)
        self.canvas.draw()
        self.status_var.set('updated at: ' +
                            datetime.now().strftime(self._formatstr))
        if (self.continuous_updates.get() and self.relative_stop_time.get() and
                not self.update_pending):
            self.update_pending = True
            self.toplevel.after(10000, lambda: self.Update(unpend=True))

    def _UpdateData(self, tab=0):
        '''
        '''
        try:
            yname = self.plot_dicts[tab]['yname'].get()
            ychdat = self.pype.GetTimeSeries(yname, self.time_interval[0],
                                             self.time_interval[1])
            if self.plot_dicts[tab]['xname'].get() == 'time':
                xchdat = (ychdat[0], ychdat[0], 'time' * len(ychdat[0]))
            else:
                xname = self.plot_dicts[tab]['xname'].get()
                xchdat = self.pype.GetTimeSeries(xname, self.time_interval[0],
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
                [self.xdata, self.ydata] = zip(*sorted(zip(self.xdata,
                                                           self.ydata)))
                self.plot_dicts['xunit'] = xchdat[2][0]
                self.plot_dicts['yunit'] = ychdat[2][0]
        except AssertionError as e:
            print('*'*60, '\n the', e[0], 'do not match the 0th line', '*'*60)

    def _UpdateExisting(self, tab=0):
        '''
        '''
        try:
            yname = self.plot_dicts[tab]['yname'].get()
            ychdat = self.pype.GetTimeSeries(yname, self.time_interval[0],
                                             self.time_interval[1])
            if self.plot_dicts[tab]['xname'].get() == 'time':
                xchdat = (ychdat[0], ychdat[0], 'time' * len(ychdat[0]))
            else:
                xname = self.plot_dicts[tab]['xname'].get()
                xchdat = self.pype.GetTimeSeries(xname, self.time_interval[0],
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
                [self.xdata, self.ydata] = zip(*sorted(zip(self.xdata,
                                                           self.ydata)))
                self.plot_dicts['xunit'] = xchdat[2][0]
                self.plot_dicts['yunit'] = ychdat[2][0]
            this_line = self.subfigure.get_lines()[tab]
            this_line.set_xdata(array(self.xdata))
            this_line.set_ydata(array(self.ydata))

        except AssertionError as e:
            print('*'*60, '\n the', e[0], 'do not match the 0th line', '*'*60)

    def _MakePlot(self, tab=0):
        '''
        '''
        if self.ConnectedPts.get():
            plotformat='o-'
        else:
            plotformat='o'
        #self.figure.get_axes()[0].clear()
        if self.plot_dicts[tab]['xname'].get() == 'time':
            self.subfigure.plot_date(self.xdata, self.ydata, plotformat,
                                          label=self.plot_dicts[tab]['yname'].get())
            self.subfigure.set_xticklabels(self.subfigure.get_xticklabels(),
                                           rotation=-45)
            self.subfigure.xaxis.set_major_formatter(dates.DateFormatter(
                "%m/%d %H:%M"))
            self.subfigure.yaxis.set_major_formatter(ticker.ScalarFormatter(
                useOffset=False))
        else:
            self.subfigure.plot(self.xdata, self.ydata, plotformat,
                                label=self.plot_dicts[tab]['yname'].get())
        self.subfigure.set_title(self.plot_dicts[tab]['yname'].get() +
                                 ' vs ' +
                                 self.plot_dicts[tab]['xname'].get() +
                                 '\n from ' + self.time_interval[0] +
                                 ' to ' + self.time_interval[1])
        xname = self.plot_dicts[tab]['xname'].get().replace('_', ' ')
        xunit = '[' + str(self.plot_dicts['xunit']) + ']'
        self.subfigure.set_xlabel(xname + ' ' + xunit)
        yname = self.plot_dicts[tab]['yname'].get().replace('_', ' ')
        yunit = '[' + str(self.plot_dicts['yunit']) + ']'
        self.subfigure.set_ylabel(yname + ' ' + yunit)
        #self.subfigure[tab].ticklabel_format(useOffset=False)
        tickformat = ticker.ScalarFormatter(useOffset=False)
        if self.ManualLimits.get():
            self.subfigure.set_ylim(bottom=self.ymin.get(), top=self.ymax.get())

        #self.canvas.draw()

    def _PlotGasLines(self):
        '''
        '''
        gas_lines = ['left_gas_line_lower_t',
                     'left_gas_line_upper_t',
                     'right_gas_line_lower_t',
                     'right_gas_line_upper_t']
        self._PlotSet(gas_lines)

    def _PlotCell(self):
        '''
        '''
        sensors = ['kh2_temp', 'kh3_temp', 'waveguide_cell_body_temp',
                   'coldhead_temp']
        self._PlotSet(sensors)

    def _PlotSet(self, channels):
        '''
            Plots a set of channels on common axes
        '''
        for plotn, channel in enumerate(channels):
            if (len(self.plot_dicts)-2) <= plotn:
                self._AddSubplot()
            self.plot_dicts[plotn]['xname'].set('time')
            self.plot_dicts[plotn]['yname'].set(channel)
        self.start_t.set('3')
        self.relative_start_time.set(True)
        self.relative_stop_time.set(True)
        self.continuous_updates.set(True)
        self.Update()

    def SaveFigure(self):
        '''
        '''
        file_extensions = [('vectorized', '.eps'), ('adobe', '.pdf'),
                           ('image', '.png'), ('all', '.*')]
        outfile = asksaveasfilename(defaultextension='.pdf',
                                    filetypes=file_extensions)
        self.figure.savefig(outfile)
