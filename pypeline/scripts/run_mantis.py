#standard libs
from Tkinter import (IntVar, StringVar, Label, Entry, Button, Checkbutton,
                     OptionMenu, Spinbox)
from inspect import getargspec
from time import sleep
#3rd party libs
#local libs
try:
    from ..PypelineErrors import NoResponseError
except ImportError:
    from PypelineErrors import NoResponseError


class __fake_bool:
    def __init__(self, value=False):
        self.value = value

    def get(self):
        return (self.value is True)

    def set(self, value):
        self.value = (value is True)


class run_mantis:
    '''
    '''

    def __init__(self, pype, toplevel=False, dodump=False, **runargs):
        '''
            Script to run mantis, if called from within gpypeline, provides
            gui interface.

            Inputs:
                <pype>  A DripInterface object
                <toplevel> A tkinter Toplevel instance (should only be used
                           internally by gpypeline)
                <dodump> Is a bool, if True, run SensorDump() before mantis
                <**runargs> any keword arguments for DripInterface.RunMantis
                            method
        '''
        self.pype = pype
        self.runargs = runargs
        self.status = StringVar(value='Ready')

        if not toplevel:
            self.dodump = __fake_bool(value=(dodump is True))
            self.DoRun()
        else:
            self.dodump = IntVar(value=(dodump is True))
            self.toplevel = toplevel
            self.BuildGui()

    def DoRun(self):
        '''
            Executes the mantis run
        '''
        self.status.set('run failed!')
        try:
            for key in self.gui_input_dict.keys():
                self.runargs[key] = self.gui_input_dict[key].get()
        except:
            pass
        response = self.pype.RunMantis(**self.runargs)
        if self.dodump.get():
            sensor_dump = self.pype.DumpSensors(runresponse=response)
        sleeptime = 60
        if 'duration' in self.runargs:
            sleeptime = float(self.runargs['duration'])/1000.
        sleep(sleeptime)
        response.Wait()
        if response.Waiting():
            raise NoResponseError('')
        filename = [line.split()[-1] for line in response['final'].split('\n')
                    if line.startswith(' *output')]
        if self.dodump.get():
            sensor_dump['mantis'].Update()
            sensor_dump._UpdateTo()
        self.status.set('run complete')

    def BuildGui(self):
        '''
            Create gui elements
        '''
        arg_names, _, _, default_vals = getargspec(self.pype.RunMantis)
        initial_vals = [None] * len(arg_names)
        if default_vals:
            initial_vals[-len(default_vals):] = default_vals
        self.gui_input_dict = {}
        for rowi, (keyname, initval) in enumerate(zip(arg_names,
                                                      initial_vals)):
            if keyname in ['self', 'pype']:
                continue
            self.gui_input_dict[keyname] = StringVar(value=str(initval))
            if keyname == "mode":
                Label(self.toplevel, text="mode").grid(row=rowi, column=0)
                Spinbox(self.toplevel,
                        textvariable=self.gui_input_dict[keyname],
                        values=(1, 2)).grid(row=rowi, column=1)
            else:
                Label(self.toplevel, text=keyname).grid(row=rowi, column=0)
                Entry(self.toplevel,
                      textvariable=self.gui_input_dict[keyname]).grid(row=rowi,
                                                                      column=1)
        rowi += 1
        Button(self.toplevel, text="Start Run",
               command=self.DoRun).grid(row=rowi, column=0)
        Label(self.toplevel, textvariable=self.status).grid(row=rowi, column=1)
        rowi += 1
        Checkbutton(self.toplevel, text="Do Sensor Dump",
                    variable=self.dodump).grid(row=rowi, column=0)
