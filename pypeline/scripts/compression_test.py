from __future__ import print_function, absolute_import

import matplotlib
matplotlib.use('TkAgg')

from sys import version_info
inpy3 = not version_info[0] <3

# Standard
import ast
if inpy3:
    from tkinter import (DoubleVar, Label, Entry, Button)
    from tkinter.ttk import Frame
else:
    from Tkinter import (DoubleVar, Label, Entry, Button)
    from ttk import Frame
# 3rd Party
from numpy import arange
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# Local
from ..PypelineErrors import DriplineError
from .script_helpers import _fake_DoubleVar


class compression_test:
    '''
    '''

    def __init__(self, pype, toplevel=False, power_start=-80, power_stop=-10,
                 power_step=5, lo_frequency=50, digitization_time=50):
        '''
        '''
        self.pype = pype
        self.toplevel = toplevel
        if toplevel:
            self.DoubleV = DoubleVar
        else:
            self.DoubleV = _fake_DoubleVar
        self.kwargs_dict = {
                            'power_start': self.DoubleV(value=power_start),
                            'power_start_units': 'dBm',
                            'power_stop': self.DoubleV(value=power_stop),
                            'power_stop_units': 'dBm',
                            'power_step': self.DoubleV(value=power_step),
                            'power_step_units': 'dBm',
                            'lo_frequency': self.DoubleV(value=lo_frequency),
                            'lo_frequency_units': 'MHz',
                           }
        if not toplevel:
            self.run_compression_test()
        else:
            self.BuildGui()

    def BuildGui(self):
        '''
        '''
        rowi = 0
        for kwarg in self.kwargs_dict.keys():
            if kwarg.endswith('_units'):
                continue
            Label(self.toplevel, text=kwarg).grid(row=rowi, column=0)
            Entry(self.toplevel, textvariable=self.kwargs_dict[kwarg]
                  ).grid(row=rowi, column=1)
            unit_string = '[' + self.kwargs_dict[kwarg+'_units'] + ']'
            Label(self.toplevel, text=unit_string).grid(row=rowi, column=2)
            rowi += 1
        Button(self.toplevel, text='Start Test', command=self._DoRun
               ).grid(row=rowi, column=0)
        Button(self.toplevel, text='Save', command=self._SaveData
               ).grid(row=rowi, column=1)

    def _DoRun(self):
        '''
        '''
        self.RunCompressionTest()
        self._PlotResult()

    def RunCompressionTest(self):
        '''
            Execute a compression test
    
            Inputs:
                <pype>: pypeline.DripInterface instance
                <power_start>: low power for scan (in dBm)
                <power_stop>: high power for scan (in dBm)
                <power_step>: power step size (in dBm)
                <lo_frequency>: frequency at which to scan (in MHz)
                <digitization_time>: duration of mantis run (in ms)
        '''
        power_start = self.kwargs_dict['power_start'].get()
        power_stop = self.kwargs_dict['power_stop'].get()
        power_step = self.kwargs_dict['power_step'].get()
        lo_frequency = self.kwargs_dict['lo_frequency'].get()
        digitization_time = 50

        sweep_frequency = lo_frequency + 24250
        self.pype.Set('hf_cw_freq', sweep_frequency)
        self.pype.Set('lo_cw_freq', lo_frequency)
        tempfile = '/data/thisisatempfileforcompressiontests.egg'
        descrip = {'lo_frequency': lo_frequency}
        rate = 200
        mode = 1
        power_out = []
        powers = arange(power_start, power_stop, power_step)
        for power in powers:
            print('doing power:', power, 'dBm')
            self.pype.Set('hf_sweeper_power', power)
            mantis_out = self.pype.RunMantis(output=tempfile, mode=mode,
                                             rate=rate,
                                             duration=digitization_time,
                                             description=descrip)
            mantis_out.Wait(digitization_time / 1000. + 20)
            if mantis_out.Waiting():
                raise DriplineError('failed to digitize')
            powerline_out = self.pype.RunPowerline(input_file=tempfile)
            powerline_out.Wait(60)
            power_out.append(max(ast.literal_eval(powerline_out['final'])['data']))
        self.result = {'power_in': powers, 'power_out': power_out}

    def _PlotResult(self):
        '''
        '''
        self.figure = Figure()
        self.figure.subplots_adjust(left=0.15, bottom=0.2)
        self.subfigure = []
        frame = Frame(self.toplevel)
        frame.grid(row=0, column=3, rowspan=5)
        self.subfigure.append(self.figure.add_subplot(1,1,1))
        print('x',self.result['power_in'])
        print('of type',type(self.result['power_in']))
        print('len(x)',len(self.result['power_in']))
        print('len(y)',len(self.result['power_out']))
        self.subfigure[0].plot(self.result['power_in'], self.result['power_out'])
        titlestr = ('Compression Test at ' +
                   str(self.kwargs_dict['lo_frequency'].get()) + ' ' +
                   self.kwargs_dict['lo_frequency_units'] + ' LO')
        self.subfigure[0].set_title(titlestr)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.toplevel)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0, column=3, rowspan=10)

    def _SaveData(self):
        '''
        '''
        file_extensions = [('vectorized', '.eps'), ('adobe', '.pdf'),
                           ('image', '.png'), ('all', '.*')]
        outfile = asksaveasfilename(defaultextension='.pdf',
                                    filetypes=file_extensions)
        self.figure.savefig(outfile)
