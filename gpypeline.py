#!/usr/bin/python2
from __future__ import print_function, absolute_import
from sys import version_info
inpy3 = not version_info[0] < 3

# Standard Libs
if inpy3:
    from tkinter import *
    from tkinter.filedialog import asksaveasfile
else:
    from Tkinter import *
    from tkFileDialog import asksaveasfile
from datetime import datetime
from json import dump
from inspect import getargspec, getmembers, isclass, isfunction
# 3rd party Libs
from numpy import pi
# internal Libs
from pypeline import DripInterface, scripts, NoResponseError


class App:

    def __init__(self, master):
        self.master = master

        self.frame = Frame(master)
        self.frame.grid()

        self.pype = DripInterface('http://myrna.phys.washington.edu:5984')

        self.BuildGUI()
        self.update_values()

    def BuildGUI(self):
        '''
            Create the permanent text, should only need to call this once
        '''
        row = 0
        self.channels = self.pype.Get()
        # Tkinter Variables
        #
        # current time
        self.time = StringVar(value=datetime.now())
        # which script to run
        self.which_script = StringVar(value="channel_plot")
        # which channel to get
        self.getchannelVar = StringVar()
        # get return
        self.getchannelvalueVar = StringVar()
        # which channel to set
        self.setchannelVar = StringVar()
        # value to set
        self.setchannelvalueVar = StringVar()
        # which logger to turn on 
        self.logchannelVar = StringVar()
        self.logintervalVar = IntVar(value=20)
        # values in loggers
        self.loggers_list = self.pype.ListWithProperty('logging')
        self.loggers_dict = {}
        self.loggers_time = {}
        for channel in self.loggers_list:
            self.loggers_dict[channel] = StringVar()
            self.loggers_time[channel] = StringVar()

        # Text labels
        self.timedesc = Label(self.frame, text="The time is:")
        self.timedesc.grid(row=row, sticky=W)
        self.timeval = Label(self.frame, textvariable=self.time, relief=SUNKEN)
        self.timeval.grid(row=row, column=1)
        row += 1

        # Buttons ########################################
        # Get interface
        self.get_button = Button(self.frame, text="Get",
                                 command=self.GetChannel)
        self.get_button.grid(row=row, column=0, sticky=EW)
        self.get_selection = OptionMenu(self.frame, self.getchannelVar,
                                        *self.channels)
        self.get_selection.grid(row=row, column=1, sticky=EW)
        self.get_answer_label = Label(self.frame,
                                      textvariable=self.getchannelvalueVar,
                                      relief=SUNKEN)
        self.get_answer_label.grid(row=row, column=2, sticky=EW)
        row += 1

        # Set interface
        self.set_button = Button(self.frame, text="Set",
                                 command=self.SetChannel)
        self.set_button.grid(row=row, column=0, sticky=EW)
        self.set_selection = OptionMenu(self.frame, self.setchannelVar,
                                        *self.channels)
        self.set_selection.grid(row=row, column=1, sticky=EW)
        self.set_answer_label = Entry(self.frame,
                                      textvariable=self.setchannelvalueVar,
                                      relief=SUNKEN)
        self.set_answer_label.grid(row=row, column=2, sticky=EW)
        row += 1

        # Start logger interface
        self.start_button = Button(self.frame, text="Start Logging",
                                   command=self.StartLogger)
        self.start_button.grid(row=row, column=0, sticky=EW)
        self.log_selection = OptionMenu(self.frame, self.logchannelVar,
                                        *self.channels)
        self.log_selection.grid(row=row, column=1, sticky=EW)
        Entry(self.frame, textvariable=self.logintervalVar,
              relief=SUNKEN).grid(row=row, column=2, sticky=EW)
        row += 1


        # Run interface
        self.run_script = Button(self.frame, text="Run",
                                 command=self.ScriptDialog)
        self.run_script.grid(row=row, column=0, sticky=EW)
        scriptlist = [name[0] for name in getmembers(scripts, isfunction)]
        scriptlist += [name[0] for name in getmembers(scripts, isclass)]
        #scriptlist += ['run_dpph']
        self.script_selection = OptionMenu(self.frame, self.which_script,
                                           *scriptlist)
        self.script_selection.grid(row=row, column=1, sticky=EW)

        # Data display
        #
        for rowi, channel in enumerate(self.loggers_list):
            Label(self.frame, text=channel).grid(row=rowi, column=3)
            Label(self.frame, textvariable=self.loggers_dict[channel],
                  relief=SUNKEN).grid(row=rowi, column=4, sticky=EW)
            Label(self.frame, textvariable=self.loggers_time[channel],
                  relief=SUNKEN).grid(row=rowi, column=5, sticky=EW)

    def update_values(self):
        '''
            Update displayed values
        '''
        self.time.set(datetime.now().strftime('%B %d, %Y %H:%M:%S'))
        latest = self.pype.GetLatestValues(self.loggers_list)
        for key in latest:
            self.loggers_dict[key].set(latest[key]['value'])
            self.loggers_time[key].set(latest[key]['time'])
        self.timeval.after(5*60*1000, self.update_values)

    def GetChannel(self):
        try:
            result = self.pype.Get(self.getchannelVar.get()).Wait()['final']
        except KeyError:
            result = "No response from dripline"
        except:
            raise
        self.getchannelvalueVar.set(result)

    def SetChannel(self):
        result = self.pype.Set(self.setchannelVar.get(),
                               self.setchannelvalueVar.get()).Wait()['final']
        self.setchannelvalueVar.set(result)

    def StartLogger(self):
        if not logchannelVar.get() in self.pype.EligibleLoggers():
            self.pype.AddLoggers([self.logchannelVar.get()],
                                 [self.logintervalVar.get()])
        result = self.pype.StartLoggers([self.logchannelVar.get()]).Wait()
        if 'final' in result:
            print('started')
        else:
            print(result)
            raise NoResponseError('no response to start loggers')


    def ScriptDialog(self):
        #### this section should be added to the later parts asap
#        special_scripts = ['run_dpph']
        ####################
        func_scripts = [name[0] for name in getmembers(scripts, isfunction)]
        class_scripts = [line[0] for line in getmembers(scripts, isclass)]
        script_name = self.which_script.get()
        if script_name in func_scripts:
            self.generic_function_script_popup(script_name)
        elif script_name in class_scripts:
            self.generic_class_script_popup(script_name)
#        elif script_name in special_scripts:
#            self.run_dpph()
        else:
            print('\n\n' + '*' * 60 + '\nscript not found\n' + '*' * 60)

    def generic_class_script_popup(self, script_name):
        script_popup = Toplevel()
        script_popup.title(script_name)
        script_popup.grid()
        getattr(scripts, script_name)(self.pype, script_popup)

    def generic_function_script_popup(self, script_name):
        script_popup = Toplevel()
        script_popup.title(script_name)
        script_popup.grid()

        script_fun = getattr(scripts, script_name)
        arg_names, _, _, default_vals = getargspec(script_fun)
        initial_vals = [None] * len(arg_names)
        if default_vals:
            initial_vals[-len(default_vals):] = default_vals
        self.gui_input_dict = {}
        for rowi, (keyname, initval) in enumerate(zip(arg_names,
                                                      initial_vals)):
            if keyname == 'pype':
                continue
            self.gui_input_dict[keyname] = StringVar(value=str(initval))
            Label(script_popup, text=keyname).grid(row=rowi, column=0)
            Entry(script_popup,
                  textvariable=self.gui_input_dict[keyname]).grid(row=rowi,
                                                                  column=1)
        startbt = Button(script_popup, text="Start Script",
                         command=lambda: self.exec_script(script_fun))
        startbt.grid(row=len(self.gui_input_dict.keys()) + 1, columnspan=2)

    def exec_script(self, script):
        args_dict = {}
        for key in self.gui_input_dict:
            args_dict[key] = self.gui_input_dict[key].get()
        script(self.pype, *args_dict)


if __name__ == "__main__":
    root = Tk()
    root.title("gpypeline")
    app = App(root)
    root.mainloop()
