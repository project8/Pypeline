from __future__ import print_function, absolute_import
# built in
from Tkinter import DoubleVar, StringVar, Button, Entry, Label, OptionMenu
from tkFileDialog import asksaveasfile
from ttk import Notebook, Frame
# 3rd party
from numpy import pi
# local
from .linear_fit import linear_fit
from .fft_filter import fft_filter


class __non_guiVar:
    def __init__(self, value=False):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class measure_dpph:
    '''
    '''

    def __init__(self, pype, toplevel=False, **runargs):
        '''
        '''
        self.pype = pype
        self.runargs = runargs
        self.toplevel = toplevel

        self.guessval = DoubleVar(value=25000)
        self.guessunits = StringVar(value="MHz")
        self.nsigmavar = DoubleVar(value=20)
        self.nvoltsvar = DoubleVar(value=9e-7)
        self.powerVar = DoubleVar(value=-75)
        self.spanVar = DoubleVar(value=100)
        self.stepVar = DoubleVar(value=4)
        self.BuildGui()

    def DoRun(self, method):
        '''
        '''
        geff = 2.0036
        chargemass = 1.758e11
        freq_to_field = 4 * pi * 10 ** 7 / (geff * chargemass)
        if self.guessunits.get() == "kG":
            self.guessval.set(self.guessval.get() / freq_to_field)
            self.guessunits.set("MHz")
        if method == 'linear_fit':
            dpph_result, dpph_dataset = (linear_fit(self.pype,
                                         guess=self.guessval.get(),
                                         stop_nsigma=self.nsigmavar.get(),
                                         stop_voltage=self.nvoltsvar.get(),
                                         power=self.powerVar.get()))
        elif method == 'fft_filter':
            dpph_result, dpph_dataset = (fft_filter(self.pype,
                                         guess=self.guessval.get(),
                                         power=self.powerVar.get(),
                                         span=self.spanVar.get(),
                                         step=self.stepVar.get()))

        self.dpph_result = dpph_result
        self.dpph_dataset = dpph_dataset

    def BuildGui(self):
        '''
            Dpph popup window
        '''
        lastrow = 6
        # user guess
        Label(self.toplevel, text="guess").grid(row=0, column=0, sticky='ew')
        Entry(self.toplevel, textvariable=self.guessval
              ).grid(row=0, column=1, sticky='ew')
        OptionMenu(self.toplevel, self.guessunits, *["MHz", "kG"]
                   ).grid(row=0, column=2, sticky='ew')
        # get hall probe guses
        Button(self.toplevel, text="Hall Probe", command=self.checkhallprobe
               ).grid(row=0, column=3)
        # input power
        Label(self.toplevel, text='Input Power').grid(row=1, column=0,
                                                      sticky='ew')
        Entry(self.toplevel, textvariable=self.powerVar
              ).grid(row=1, column=1, sticky='ew')
        Label(self.toplevel, text='[dBm]', justify='left').grid(row=1,
                                                                column=2)

        #######################
        # Tabs for different methods
        self.notebook = Notebook(self.toplevel)
        self.notebook.grid(row=2, column=0, rowspan=5, columnspan=3)
        # linear fit ############################
        # entries
        linear_frame = Frame(self.notebook)
        linear_frame.pack(side='top', fill='both', expand='y')
        Label(linear_frame, text='Sigma limit').grid(row=0, column=0,
                                                     sticky='ew')
        Entry(linear_frame, textvariable=self.nsigmavar
              ).grid(row=0, column=1, sticky='ew')
        Label(linear_frame, text='(a real)', justify='left'
              ).grid(row=0, column=2)
        Label(linear_frame, text='Voltage limit').grid(row=1, column=0,
                                                       sticky='ew')
        Entry(linear_frame, textvariable=self.nvoltsvar
              ).grid(row=1, column=1, sticky='ew')
        Label(linear_frame, text='[V]', justify='left').grid(row=1, column=2)
        # actions
        Button(linear_frame, text="Start Scan",
               command=lambda: self.DoRun('linear_fit')).grid(row=2, column=0)
        Button(linear_frame, text="Save Plot Data",
               command=self.store_dpph_data_json).grid(row=2, column=1)
        Button(linear_frame, text="Log Result", command=self.log_dpph
               ).grid(row=2, column=2)
        self.notebook.add(linear_frame, text='linear fit')
        # fft filter #################################
        # entries
        fft_frame = Frame(self.notebook)
        fft_frame.pack(side='top', fill='both', expand='y')
        Label(fft_frame, text='Search Span').grid(row=0, column=0, sticky='ew')
        Entry(fft_frame, textvariable=self.spanVar
              ).grid(row=0, column=1, sticky='ew')
        Label(fft_frame, text='MHz', justify='left').grid(row=0, column=2)

        Label(fft_frame, text='Step Size').grid(row=1, column=0, sticky='ew')
        Entry(fft_frame, textvariable=self.stepVar
              ).grid(row=1, column=1, sticky='ew')
        Label(fft_frame, text='MHz', justify='left').grid(row=1, column=2)
        # actions
        Button(fft_frame, text="Start Scan",
               command=lambda: self.DoRun('fft_filter')).grid(row=2, column=0)
        Button(fft_frame, text="Log Result", command=self.log_dpph
               ).grid(row=2, column=2)
        self.notebook.add(fft_frame, text='fft filter')

    def checkhallprobe(self):
        halldoc = self.pype.Get('hall_probe_voltage').Wait()
        self.guessval.set(abs(float(halldoc['final'].split()[0])))
        self.guessunits.set('kG')

    def store_dpph_data_json(self):
        if not self.dpph_dataset:
            print('no dpph_dataset stored')
            return
        outfile = asksaveasfile(defaultextension='.json')
        dump({"frequencies": self.dpph_dataset[0],
              "voltages": self.dpph_dataset[1]},
             outfile, indent=4)
        outfile.close()

    def log_dpph(self):
        if not self.dpph_result:
            print('no dpph_result stored')
            return
        self.pype.LogValue(sensor='dpph_field', **self.dpph_result)
