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
    from tkinter.messagebox import showwarning
else:
    from Tkinter import (DoubleVar, StringVar, BooleanVar, IntVar,
                         Button, Checkbutton, Entry, Label, OptionMenu)
    from tkFileDialog import asksaveasfile, asksaveasfilename
    from ttk import Notebook, Frame
    from tkMessageBox import showwarning
from json import dump
from datetime import datetime
# 3rd party
from numpy import pi, array, mean
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# local
#from .linear_fit import linear_fit
#from .fft_filter import fft_filter
from .dpph_utils import _GetSweptVoltages, _FindFieldFFT


class _non_guiVar:

    def __init__(self, value=False):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

class dpph_measurement:
    '''
    '''

    def __init__(self, pype, toplevel=False, **runargs):
        '''
        '''
        self.pype = pype
        self.runargs = runargs
        self.toplevel = toplevel
        self.sweep_result = {}

        if not toplevel:
            DV = _non_guiVar
            BV = _non_guiVar
            IV = _non_guiVar
            SV = _non_guiVar
        else:
            DV = DoubleVar
            BV = BooleanVar
            IV = IntVar
            SV = StringVar
        self.powerVar = DV(value=-75) #dBm
        self.set_power_BoolVar = BV(value=True)
        self.start_freq_Var = DV(value=26500) #MHz
        self.stop_freq_Var = DV(value=26950) #MHz
        self.start_search_freq_Var = DV(value=26500) #MHz
        self.stop_search_freq_Var = DV(value=26950) #MHz
        self.expected_width_Var = DV(value=3) #???
        self.sweep_time_Var = DV(value=30) #s
        self.num_points_Var = IV(value=400) #ms
        self.spanVar = DV(value=100)
        self.stepVar = DV(value=4)
        #self.fit_channel_Var = StringVar(value='xdata')
        self.result_str_Var = SV(value='')
            

        if self.toplevel:
            self._BuildGui()

    def _BuildGui(self):
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

        Label(self.toplevel, text='-'*50).grid(row=row, column=0, columnspan=4, sticky='ew')
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
        
        Label(self.toplevel, text='Filter Target Width').grid(row=row, column=0)
        Entry(self.toplevel, textvariable=self.expected_width_Var
              ).grid(row=row, column=1, sticky='ew')
        row += 1

        #ch_options = ['xdata', 'ydata']
        #OptionMenu(self.toplevel, self.fit_channel_Var, *ch_options
        #           ).grid(row=row, column=0, rowspan=2, sticky='ew')
        Button(self.toplevel, text='find resonance', command=self._FindResonance
               ).grid(row=row, column=1, rowspan=2, sticky='ew')
        Label(self.toplevel, textvariable=self.result_str_Var
              ).grid(row=row, column=2, rowspan=2, columnspan=3, sticky='ew')
        row += 2

        Button(self.toplevel, text='Dump To json', command=self._SaveJson
               ).grid(row=row, column=0)
        Button(self.toplevel, text='Save Image', command=self._SaveFigure
               ).grid(row=row, column=1)
        Button(self.toplevel, text='Log DPPH', command=self._LogDPPH
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
        self.subfigure.set_xlabel('Freq [MHz]')
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.toplevel)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=row, column=column, rowspan=10)

    def _CollectSweep(self):
        '''
        '''
        tmp_power = self.powerVar.get()
        if self.set_power_BoolVar.get():
            tmp_power = False
        while True:
            sweep = _GetSweptVoltages(pype=self.pype,
                                  start_freq=self.start_freq_Var.get(),
                                  stop_freq=self.stop_freq_Var.get(),
                                  sweep_time=self.sweep_time_Var.get(),
                                  power=tmp_power,
                                  num_points=self.num_points_Var.get())
            self.sweep_result = sweep.copy()
            self.freqdata = array(sweep['frequency_curve'])
            self.magdata = sweep['amplitude_curve']
            if type(self.magdata[0]) is unicode:
                print('Warning: _GetSweptVoltages failed;')
                print('magdata:')
                print(self.magdata)
                print('Acquiring data again...')
            elif type(self.magdata[0]) is int:
                break
        if (not sweep['frequencies_confirmed'] and self.toplevel):
            showwarning('Warning', 'Communication with lockin amp failed. Frequencies data may be wrong')
        self.magdata = self.magdata - mean(self.magdata)
        print('freq range is ', min(self.freqdata), ' to ', max(self.freqdata))
        y_del = max((max(self.magdata) - min(self.magdata)) * .05, 1)
        if self.toplevel:
            self.subfigure.set_xlim(left=self.freqdata[0], right=self.freqdata[-1])
            self.subfigure.set_ylim(bottom=(min(self.magdata) - y_del), top=(max(self.magdata) + y_del))
            line = self.subfigure.get_lines()[0]
            line.set_xdata(array(self.freqdata))
            line.set_ydata(array(self.magdata))
            line.set_label('lockin output "X"')
            self.figure.legends = []
            self.figure.legend(*self.subfigure.get_legend_handles_labels())
            self.figure.legends[0].draggable(True)
            self.canvas.draw()
            self.canvas.show()
        print('Searching for resonance...')
        self._FindResonance()

    def _FindResonance(self):
        '''
        '''
        #line = self.subfigure.get_lines()[0]
        #xdata = line.get_xdata()
        #ydata = line.get_ydata()

        xdata = array(self.freqdata)
        ydata = array(self.magdata)

        fit = _FindFieldFFT(min_freq=self.start_search_freq_Var.get(),
                            max_freq=self.stop_search_freq_Var.get(),
                            freq_data=xdata,
                            volts_data=ydata,
                            width=self.expected_width_Var.get())
        #compute and calibrate resonance
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
        
        if self.toplevel:
        # update a line for the filter result
            outline = self.subfigure.get_lines()[1]
            factor = max(ydata) / max(fit['result'])
            scaled_data = [val * factor for val in fit['result']]
            scaled_data = scaled_data - mean(scaled_data)
            outline.set_xdata(fit['freqs'])
            outline.set_ydata(scaled_data)
            outline.set_label('filter result')
            # and a line showing the filter shape
            filterline = self.subfigure.get_lines()[2]
            filter_factor = max(ydata)/max(fit['filter'])
            scaled_filter_data = [val * -1*filter_factor for val in fit['filter']]
            scaled_filter_data = scaled_filter_data - mean(scaled_data)
            print("len of result:", len(fit['result']))
            print("len of filter:", len(scaled_filter_data))
            shift = -1*abs(fit['result']).argmax()#list(fit['result']).index(max(abs(fit['result'])))
            print("shift is:", shift)
            scaled_filter_data = list(scaled_filter_data)[shift:]+list(scaled_filter_data)[:shift]
            filterline.set_xdata(fit['freqs'])
            filterline.set_ydata(array(scaled_filter_data))
            filterline.set_label('filter shape')
            print('filter shape done')
            # then some legend stuff
            self.figure.legends = []
            self.figure.legend(*self.subfigure.get_legend_handles_labels())
            self.figure.legends[0].draggable(True)
            self.canvas.draw()
            self.canvas.show()

        self.result_str_Var.set('{:.4E} +/- {:.1E} MHz \n({:.4E} +/- {:.1E} kG)'.format(
            res_freq, res_unct, res_field, res_field_unct))
        self.sweep_result.update({'res_freq': res_freq,
                                  'res_freq_unct': res_unct,
                                  'res_field': res_field,
                                  'res_field_unct': res_field_unct})

    def _SaveJson(self):
        '''
        '''
        if not self.sweep_result:
            print('no result stored')
            return
        outfile = asksaveasfile(defaultextension='.json')
        dump(self.sweep_result, outfile, indent=4)
        outfile.close()

    def _SaveFigure(self):
        '''
        '''
        file_extensions = [('vectorized', '.eps'), ('adobe', '.pdf'), ('image', '.png'), ('all', '.*')]
        outfile = asksaveasfilename(defaultextension='.pdf',
                                    filetypes=file_extensions)
        self.figure.savefig(outfile)

    def _LogDPPH(self):
        if not self.sweep_result:
            print('no dpph_result stored')
            return
        result = {
                  'uncal': self.sweep_result['res_freq'],
                  'uncal_err': self.sweep_result['res_freq_unct'],
                  'uncal_units': 'MHz',
                  'cal': self.sweep_result['res_field'],
                  'cal_err': self.sweep_result['res_field_unct'],
                  'cal_units': 'kG',
                 }
        dpph_result = {'uncal_val': ' '.join([str(result['uncal']), '+/-', str(result['uncal_err']), result['uncal_units']]),
                       'cal_val': ' '.join([str(result['cal']), '+/-', str(result['cal_err']), result['cal_units']]),
                       'timestamp': datetime.utcnow()}
        self.pype.LogValue(sensor='dpph_field', **dpph_result)
        print('dpph_result stored')


