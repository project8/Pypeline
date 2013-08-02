from __future__ import print_function, absolute_import
from sys import version_info
inpy3 = not version_info[0] < 3

import matplotlib
matplotlib.use('TkAgg', warn=False)

# built in
if inpy3:
    from tkinter import (DoubleVar, StringVar, BooleanVar, IntVar,
                         Button, Checkbutton, Entry, Label, OptionMenu)
    from tkinter.filedialog import asksaveasfile, asksaveasfilename
    from tkinter.ttk import Notebook, Frame
else:
    from Tkinter import (DoubleVar, StringVar, BooleanVar, IntVar,
                         Button, Checkbutton, Entry, Label, OptionMenu)
    from tkFileDialog import asksaveasfile, asksaveasfilename
    from ttk import Notebook, Frame
from json import dump
# 3rd party
from numpy import pi, array
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# local
from .linear_fit import linear_fit
from .fft_filter import fft_filter
from .dpph_utils import _GetSweptVoltages, _FindFieldFFT


class __non_guiVar:
    def __init__(self, value=False):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class swept_dpph_measurement:
    '''
    '''

    def __init__(self, pype, toplevel=False, **runargs):
        '''
        '''
        self.pype = pype
        self.runargs = runargs
        self.toplevel = toplevel
        self.sweep_result = {}

        self.powerVar = DoubleVar(value=-75) #dBm
        self.set_power_BoolVar = BooleanVar(value=True)
        self.start_freq_Var = DoubleVar(value=25000) #MHz
        self.stop_freq_Var = DoubleVar(value=26500) #MHz
        self.start_search_freq_Var = DoubleVar(value=25000) #MHz
        self.stop_search_freq_Var = DoubleVar(value=26500) #MHz
        self.sweep_time_Var = DoubleVar(value=60) #s
        self.num_points_Var = IntVar(value=360) #ms
        self.spanVar = DoubleVar(value=100)
        self.stepVar = DoubleVar(value=4)
        self.fit_channel_Var = StringVar(value='xdata')
        self.result_str_Var = StringVar(value='')

        self.BuildGui()

    def BuildGui(self):
        '''
            Dpph popup window
        '''
        row = 0
        ##################################################################
        # Lockin Scan
        Label(self.toplevel, text='Input Power'
              ).grid(row=row, column=0, sticky='ew')
        Entry(self.toplevel, textvariable=self.powerVar
              ).grid(row=row, column=1, sticky='ew')
        Label(self.toplevel, text='[dBm]', justify='left'
              ).grid(row=row, column=2, sticky='w')
        Checkbutton(self.toplevel, text="Don't Change",
                    variable=self.set_power_BoolVar).grid(row=row, column=3)
        row += 1

        Label(self.toplevel, text='Scan Frequency Range'
              ).grid(row=row, column=0, sticky='ew')
        Entry(self.toplevel, textvariable=self.start_freq_Var
              ).grid(row=row, column=1, sticky='ew')
        Entry(self.toplevel, textvariable=self.stop_freq_Var
              ).grid(row=row, column=2, columnspan=2, sticky='ew')
        Label(self.toplevel, text='[MHz]').grid(row=row, column=4, sticky='w')
        row += 1

        Label(self.toplevel, text='Sweep Time'
              ).grid(row=row, column=0, sticky='ew')
        Entry(self.toplevel, textvariable=self.sweep_time_Var
              ).grid(row=row, column=1, sticky='ew')
        Label(self.toplevel, text='[s]').grid(row=row, column=2, sticky='w')
        row += 1

        Label(self.toplevel, text='Number of Points'
              ).grid(row=row, column=0, sticky='ew')
        Entry(self.toplevel, textvariable=self.num_points_Var
              ).grid(row=row, column=1, sticky='ew')
        row += 1

        Button(self.toplevel, text='take data', command=self._CollectSweep
               ).grid(row=row, column=0)
        row += 1

        Label(self.toplevel, text='-'*100).grid(row=row, column=0, columnspan=4, sticky='ew')
        row += 1


        ##################################################################
        # Resonance Search
        Label(self.toplevel, text='Search Frequency Range'
              ).grid(row=row, column=0, sticky='ew')
        Entry(self.toplevel, textvariable=self.start_search_freq_Var
              ).grid(row=row, column=1, sticky='ew')
        Entry(self.toplevel, textvariable=self.stop_search_freq_Var
              ).grid(row=row, column=2, columnspan=2, sticky='ew')
        Label(self.toplevel, text='[MHz]').grid(row=row, column=4, sticky='w')
        row += 1

        ch_options = ['xdata', 'ydata']
        OptionMenu(self.toplevel, self.fit_channel_Var, *ch_options
                   ).grid(row=row, column=0, rowspan=2, sticky='ew')
        Button(self.toplevel, text='find resonance', command=self._FindResonance
               ).grid(row=row, column=1, rowspan=2, sticky='ew')
        Label(self.toplevel, textvariable=self.result_str_Var
              ).grid(row=row, column=2, rowspan=2, columnspan=3, sticky='ew')
        row += 2

        Button(self.toplevel, text='Dump To json', command=self.store_dpph_data_json
               ).grid(row=row, column=0)
        Button(self.toplevel, text='Save Image', command=self.SaveFigure
               ).grid(row=row, column=1)
        Button(self.toplevel, text='Log DPPH', command=self.log_dpph
               ).grid(row=row, column=2)

        self._SetupPlot(row=0, column=5)

    def _SetupPlot(self, row, column):
        '''
            Initialize the plot in the gui
        '''
        self.figure = Figure()
        self.figure.subplots_adjust(left=0.15, bottom=0.2)
        self.subfigure = self.figure.add_subplot(1, 1, 1)
        self.subfigure.plot([0], [0])
        self.subfigure.plot([0], [0])
        self.subfigure.plot([0], [0])
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.toplevel)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=row, column=column, rowspan=10)

    def _CollectSweep(self):
        '''
        '''
        tmp_power = self.powerVar.get()
        if self.set_power_BoolVar.get():
            tmp_power = False
        sweep = _GetSweptVoltages(pype=self.pype,
                                  start_freq=self.start_freq_Var.get(),
                                  stop_freq=self.stop_freq_Var.get(),
                                  sweep_time=self.sweep_time_Var.get(),
                                  power=tmp_power,
                                  num_points=self.num_points_Var.get())
        self.sweep_result = sweep.copy()
        freqdata = sweep['frequency_curve']
        ydata = sweep['y_curve']
        xdata = sweep['x_curve']
        self.subfigure.set_xlim(left=freqdata[0], right=freqdata[-1])
        self.subfigure.set_ylim(bottom=min(ydata + xdata), top=max(ydata + xdata))
        line = self.subfigure.get_lines()[0]
        line.set_xdata(array(freqdata))
        line.set_ydata(array(xdata))
        line.set_label('x output')
        line = self.subfigure.get_lines()[1]
        line.set_xdata(array(freqdata))
        line.set_ydata(array(ydata))
        line.set_label('y output')
        self.figure.legends = []
        self.figure.legend(*self.subfigure.get_legend_handles_labels())
        self.figure.legends[0].draggable(True)
        self.canvas.draw()
        self.canvas.show()

    def _FindResonance(self):
        '''
        '''
        if self.fit_channel_Var.get() == 'xdata':
            line = self.subfigure.get_lines()[0]
        elif self.fit_channel_Var.get() == 'ydata':
            line = self.subfigure.get_lines()[1]
        else:
            raise ValueError('not a valid dataset selection')
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        fit = _FindFieldFFT(min_freq=self.start_search_freq_Var.get(),
                            max_freq=self.stop_search_freq_Var.get(),
                            freq_data=xdata,
                            volts_data=ydata)
        outline = self.subfigure.get_lines()[2]
        factor = max(ydata) / max(fit['result'])
        scaled_data = [val * factor for val in fit['result']]
        outline.set_xdata(fit['freqs'])
        outline.set_ydata(scaled_data)
        outline.set_label('filter result')
        self.figure.legends = []
        self.figure.legend(*self.subfigure.get_legend_handles_labels())
        self.figure.legends[0].draggable(True)
        self.canvas.draw()
        self.canvas.show()
        res_freq = max(zip(fit['result'], fit['freqs']))[1]
        res_unct = fit['freqs'][1] - fit['freqs'][0]
        print('resonance found at:', res_freq, 'MHz')
        print('err is:', res_unct)
        geff = 2.0036
        chargemass = 1.758e11
        freq_to_field = 4 * pi * 10 ** 7 / (geff * chargemass)
        res_field = freq_to_field * res_freq
        res_field_unct = freq_to_field * res_unct
        print('for a field of', res_field)
        print('field unct of', res_field_unct)
        self.result_str_Var.set('{:.2E} +/- {:.1E} MHz \n({:.2E} +/- {:.1E} kG)'.format(
            res_freq, res_unct, res_field, res_field_unct))
        self.sweep_result.update({'res_freq': res_freq,
                                  'res_freq_unct': res_unct,
                                  'res_field': res_field,
                                  'res_field_unct': res_field_unct})

    def store_dpph_data_json(self):
        '''
        '''
        if not self.sweep_result:
            print('no result stored')
            return
        outfile = asksaveasfile(defaultextension='.json')
        dump(self.sweep_result, outfile, indent=4)
        outfile.close()

    def SaveFigure(self):
        '''
        '''
        file_extensions = [('vectorized', '.eps'), ('adobe', '.pdf'), ('image', '.png'), ('all', '.*')]
        outfile = asksaveasfilename(defaultextension='.pdf',
                                    filetypes=file_extensions)
        self.figure.savefig(outfile)

    def log_dpph(self):
        if not self.sweep_result:
            print('no dpph_result stored')
            return
        result = {
                  'uncal': self.sweep_result['res_freq'],
                  'uncal_err': self.sweep_result['fres_freq_unct'],
                  'uncal_units': 'MHz',
                  'cal': self.sweep_result['res_field'],
                  'cal_err': self.sweep_result['res_field_unct'],
                  'cal_units': 'kG',
                 }
        self.pype.LogValue(sensor='dpph_field', **self.dpph_result)
