from __future__ import print_function, absolute_import
# built in
from Tkinter import DoubleVar, StringVar, Button, Entry, Label, OptionMenu
from tkFileDialog import asksaveasfile
# 3rd party
from numpy import pi
# local
from .linear_fit import linear_fit
from .fft_filter import fft_filter
methods = ['linear_fit', 'fft_filter']


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
        self.methodVar = StringVar(value=methods[0])
        self.powerVar = DoubleVar(value=-75)
        self.BuildGui()

    def DoRun(self):
        '''
        '''
        geff = 2.0036
        chargemass = 1.758e11
        freq_to_field = 4 * pi * 10 ** 7 / (geff * chargemass)
        if self.guessunits.get() == "kG":
            self.guessval.set(self.guessval.get() / freq_to_field)
            self.guessunits.set("MHz")
        if self.methodVar.get() == 'dpph_lockin':
            dpph_result, dpph_dataset = (dpph_lockin(self.pype,
                                         guess=self.guessval.get(),
                                         stop_nsigma=self.nsigmavar.get(),
                                         stop_voltage=self.nvoltsvar.get(),
                                         power=self.powerVar.get()))
        elif self.methodVar.get() == 'dpph_lockin_fft':
            dpph_result, dpph_dataset = (dpph_lockin_fft(self.pype,
                                         guess=self.guessval.get(),
                                         stop_nsigma=self.nsigmavar.get(),
                                         stop_voltage=self.nvoltsvar.get(),
                                         power=self.powerVar.get()))

        self.dpph_result = dpph_result
        self.dpph_dataset = dpph_dataset

    def BuildGui(self):
        '''
            Dpph popup window
        '''
        # user guess
        Label(self.toplevel, text="guess").grid(row=0, column=0, sticky='ew')
        Entry(self.toplevel, textvariable=self.guessval
              ).grid(row=0, column=1, sticky='ew')
        OptionMenu(self.toplevel, self.guessunits, *["MHz", "kG"]
                   ).grid(row=0, column=2, sticky='ew')
        # stop conditions
        Label(self.toplevel, text='Sigma limit').grid(row=1, column=0, sticky='ew')
        Entry(self.toplevel, textvariable=self.nsigmavar
              ).grid(row=1, column=1, sticky='ew')
        Label(self.toplevel, text='(a real)', justify='left').grid(row=1, column=2)
        Label(self.toplevel, text='Voltage limit').grid(row=2, column=0,
                                                     sticky='ew')
        Entry(self.toplevel, textvariable=self.nvoltsvar
              ).grid(row=2, column=1, sticky='ew')
        Label(self.toplevel, text='[V]', justify='left').grid(row=2, column=2)
        Label(self.toplevel, text='Input Power').grid(row=3, column=0, sticky='ew')
        Entry(self.toplevel, textvariable=self.powerVar
              ).grid(row=3, column=1, sticky='ew')
        Label(self.toplevel, text='[dBm]', justify='left').grid(row=3, column=2)
        # get hall probe guses
        Button(self.toplevel, text="Hall Probe", command=self.checkhallprobe
               ).grid(row=0, column=3)
        # buttons to do the run etc
        Button(self.toplevel, text="Start Scan", command=self.DoRun
               ).grid(row=4, column=0)
        OptionMenu(self.toplevel, self.methodVar, *methods
                   ).grid(row=4, column=1)
        Button(self.toplevel, text="Save Plot Data",
               command=self.store_dpph_data_json).grid(row=4, column=2)
        Button(self.toplevel, text="Log Result", command=self.log_dpph
               ).grid(row=4, column=3)

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


