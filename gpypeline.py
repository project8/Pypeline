#!/usr/bin/python2

# Standard Libs
from Tkinter import *
from tkFileDialog import asksaveasfile
from datetime import datetime
from json import dump
from inspect import getargspec, getmembers, isclass, isfunction
# 3rd party Libs
from numpy import pi
# internal Libs
from pypeline import DripInterface, scripts


class App:

    def __init__(self, master):
        self.master = master

        self.frame = Frame(master)
        self.frame.grid()

        self.pype = DripInterface('http://myrna.phys.washington.edu:5984')

        self.setup_grid()
        self.update_values()

    def setup_grid(self):
        '''
            Create the permanent text, should only need to call this once
        '''
        self.channels = self.pype.Get()
        # Tkinter Variables
        #
        # current time
        self.time = StringVar(value=datetime.now())
        # which script to run
        self.which_script = StringVar(value="check_pulse")
        # which channel to get
        self.getchannelVar = StringVar()
        # get return
        self.getchannelvalueVar = StringVar()
        # which channel to set
        self.setchannelVar = StringVar()
        # value to set
        self.setchannelvalueVar = DoubleVar()
        # values in loggers
        self.loggers_list = ['bypass_valve_t',
                             'coldhead_bottom_face_t',
                             'dpph_field',
                             'getter_valve_t',
                             'hall_probe_voltage',
                             'inlet_pressure',
                             'left_gas_line_lower_t',
                             'left_gas_line_upper_t',
                             'linear_encoder',
                             'liquid_helium_level',
                             'liquid_nitrogen_level',
                             'lower_nrao_amp_t',
                             'outlet_pressure',
                             'platinum_rtd_c_t1',
                             'platinum_rtd_c_t2',
                             'platinum_rtd_c_t3',
                             'platinum_rtd_c_t4',
                             'pump_valve_t',
                             'right_gas_line_lower_t',
                             'right_gas_line_upper_t',
                             'trap_magnet_current',
                             'upper_nrao_amp_t',
                             'vent_valve_t',
                             'waveguide_cell_body_t']
        self.loggers_dict = {}
        for channel in self.loggers_list:
            self.loggers_dict[channel] = StringVar()

        # Text labels
        self.timedesc = Label(self.frame, text="The time is:")
        self.timedesc.grid(row=0, sticky=W)
        self.timeval = Label(self.frame, textvariable=self.time, relief=SUNKEN)
        self.timeval.grid(row=0, column=1)

        # Buttons
        #
        # Get interface
        self.get_button = Button(self.frame, text="Get",
                                 command=self.GetChannel)
        self.get_button.grid(row=1, column=0, sticky=EW)
        self.get_selection = OptionMenu(self.frame, self.getchannelVar,
                                        *self.channels)
        self.get_selection.grid(row=1, column=1, sticky=EW)
        self.get_answer_label = Label(self.frame,
                                      textvariable=self.getchannelvalueVar,
                                      relief=SUNKEN)
        self.get_answer_label.grid(row=1, column=2, sticky=EW)

        # Set interface
        self.set_button = Button(self.frame, text="Set",
                                 command=self.SetChannel)
        self.set_button.grid(row=2, column=0, sticky=EW)
        self.set_selection = OptionMenu(self.frame, self.setchannelVar,
                                        *self.channels)
        self.set_selection.grid(row=2, column=1, sticky=EW)
        self.set_answer_label = Entry(self.frame,
                                      textvariable=self.setchannelvalueVar,
                                      relief=SUNKEN)
        self.set_answer_label.grid(row=2, column=2, sticky=EW)

        # Run interface
        self.run_script = Button(self.frame, text="Run",
                                 command=self.ScriptDialog)
        self.run_script.grid(row=3, column=0, sticky=EW)
        self.script_selection = OptionMenu(self.frame, self.which_script,
                                           *['check_pulse', 'run_dpph', 'run_mantis'])
        self.script_selection.grid(row=3, column=1, sticky=EW)

        # Data display
        #
        for rowi, channel in enumerate(self.loggers_list):
            Label(self.frame, text=channel).grid(row=rowi, column=3)
            Label(self.frame, textvariable=self.loggers_dict[channel],
                  relief=SUNKEN).grid(row=rowi, column=4, sticky=EW)

    def update_values(self):
        '''
            Update displayed values
        '''
        self.time.set(datetime.now().strftime('%B %d, %Y %H:%M:%S'))
        latest = self.pype._log_database.view('pypeline_view/latest_values')
        for channel in self.loggers_list:
            ch_val = latest[channel].rows[0]['value']['cal_val']
            if ch_val:
                entrylist = ch_val.split()
                update = []
                for snip in entrylist:
                    try:
                        update.append('%.5E' % float(snip))
                    except ValueError:
                        update.append(snip)
                self.loggers_dict[channel].set(" ".join(update))
        self.timeval.after(2000, self.update_values)

    def GetChannel(self):
        result = self.pype.Get(self.getchannelVar.get()).Wait()['final']
        self.getchannelvalueVar.set(result)

    def SetChannel(self):
        result = self.pype.Set(self.setchannelVar.get(),
                               self.setchannelvalueVar.get()).Wait()['final']
        self.setchannelvalueVar.set(result)

    def ScriptDialog(self):
        #### this section should be added to the later parts asap
        special_scripts = ['run_dpph']
        ####################
        func_scripts = [name[0] for name in getmembers(scripts, isfunction)]
        class_scripts = [line[0] for line in getmembers(scripts, isclass)]
        script_name = self.which_script.get()
        if script_name in func_scripts:
            self.generic_function_script_popup(script_name)
        elif script_name in class_scripts:
            self.generic_class_script_popup(script_name)
        elif script_name in special_scripts:
            self.run_dpph
        else:
            print('\n\n' + '*' * 60 + '\nscript not found\n' + '*' * 60)

    def generic_class_script_popup(self, script_name):
        script_popup = Toplevel()
        script_popup.grid()
        getattr(scripts, script_name)(self.pype, script_popup)

    def generic_function_script_popup(self, script_name):
        script_popup = Toplevel()
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

    def say_hi(self):
        print("hi there, everyone!")

    def run_dpph(self):
        '''
            Dpph popup window
        '''
        self.guessval = DoubleVar(value=25000)
        self.guessunits = StringVar(value="MHz")
        self.nsigmavar = DoubleVar(value=20)
        self.nvoltsvar = DoubleVar(value=9e-7)

        dpph_popup = Toplevel()
        dpph_popup.grid()
        # user guess
        Label(dpph_popup, text="guess").grid(row=0, column=0, sticky=EW)
        guessentry = Entry(dpph_popup, textvariable=self.guessval)
        guessentry.grid(row=0, column=1, sticky=EW)
        unitsoption = OptionMenu(dpph_popup, self.guessunits, *["MHz", "kG"])
        unitsoption.grid(row=0, column=2, sticky=EW)
        # stop conditions
        Label(dpph_popup, text='Sigma limit').grid(row=1, column=0, sticky=EW)
        nsigmaentry = Entry(dpph_popup, textvariable=self.nsigmavar)
        nsigmaentry.grid(row=1, column=1, sticky=EW)
        Label(dpph_popup, text='(a real)', justify=LEFT).grid(row=1, column=2)
        Label(dpph_popup, text='Voltage limit').grid(row=2, column=0,
                                                     sticky=EW)
        nvoltsentry = Entry(dpph_popup, textvariable=self.nvoltsvar)
        nvoltsentry.grid(row=2, column=1, sticky=EW)
        Label(dpph_popup, text='[V]', justify=LEFT).grid(row=2, column=2)
        # get hall probe guses
        checkhall = Button(dpph_popup, text="Hall Probe",
                           command=self.checkhallprobe)
        checkhall.grid(row=0, column=3)
        # buttons to do the run etc
        dorun = Button(dpph_popup, text="Start Scan", command=self.dpph_lockin)
        dorun.grid(row=3, column=0)
        savebutton = Button(dpph_popup, text="Save Plot Data",
                            command=self.store_dpph_data_json)
        savebutton.grid(row=3, column=1)
        logresult = Button(dpph_popup, text="Log Result",
                           command=self.log_dpph)
        logresult.grid(row=3, column=2)

    def checkhallprobe(self):
        halldoc = self.pype.Get('hall_probe_voltage').Wait()
        self.guessval.set(abs(float(halldoc['final'].split()[0])))
        self.guessunits.set('kG')

    def dpph_lockin(self):
        geff = 2.0036
        chargemass = 1.758e11
        freq_to_field = 4 * pi * 10 ** 7 / (geff * chargemass)
        if self.guessunits.get() == "kG":
            self.guessval.set(self.guessval.get() / freq_to_field)
            self.guessunits.set("MHz")
        dpph_result, dpph_dataset = (scripts.dpph_lockin(self.pype,
                                     guess=self.guessval.get(),
                                     stop_nsigma=self.nsigmavar.get(),
                                     stop_voltage=self.nvoltsvar.get()))
        self.dpph_result = dpph_result
        self.dpph_dataset = dpph_dataset

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

    def check_pulse(self):
        '''
            check dripline for a pulse
        '''
        scripts.check_pulse(self.pype)

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
