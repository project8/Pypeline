from Tkinter import *
from tkFileDialog import asksaveasfile
from datetime import datetime
from json import dump
from numpy import pi
from pypeline import DripInterface, scripts


class App:
    def __init__(self, master):
        self.master = master

        self.frame = Frame(master)
        self.frame.grid()

        self.pype = DripInterface('http://p8portal.phys.washington.edu:5984')

        self.setup_grid()
        self.update_values()

    def setup_grid(self):
        '''
            Create the permanent text, should only need to call this once
        '''
        self.channels=self.pype.Get()
        # Tkinter Variables
        #########################
        #current time
        self.time = StringVar()
        self.time.set(datetime.now())
        #which script to run
        self.which_script = StringVar()
        self.which_script.set("check_heartbeat")
        #which channel to get
        self.getchannelVar = StringVar()
        #get return
        self.getchannelvalueVar = StringVar()
        #which channel to set
        self.setchannelVar = StringVar()
        #value to set
        self.setchannelvalueVar = DoubleVar()

        # Text labels
        self.timedesc = Label(self.frame, text="The time is:")
        self.timedesc.grid(row=0, sticky=W)
        self.timeval = Label(self.frame, textvariable=self.time, relief=SUNKEN)
        self.timeval.grid(row=0, column=1)

        # Buttons
        #########################
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
                                 command=self.run_script)
        self.run_script.grid(row=3, column=0, sticky=EW)
        self.script_selection = OptionMenu(self.frame, self.which_script,
                                           *['check_heartbeat', 'run_dpph'])
        self.script_selection.grid(row=3, column=1, sticky=EW)


    def update_values(self):
        '''
            Update displayed values
        '''
        self.time.set(datetime.now().strftime('%B %d, %Y %H:%M:%S'))
        self.timeval.after(200, self.update_values)

    def GetChannel(self):
        result = self.pype.Get(self.getchannelVar.get()).Wait()['final']
        self.getchannelvalueVar.set(result)

    def SetChannel(self):
        result = self.pype.Set(self.setchannelVar.get(),
                               self.setchannelvalueVar.get()).Wait()['final']
        self.setchannelvalueVar.set(result)

    def run_script(self):
        script_name = self.which_script.get()
        getattr(self, script_name)()

    def say_hi(self):
        print("hi there, everyone!")

    def run_dpph(self):
        '''
            Dpph popup window
        '''
        self.guessval = DoubleVar()
        self.guessval.set(25000)
        self.guessunits = StringVar()
        self.guessunits.set("MHz")

        dpph_popup = Toplevel()
        dpph_popup.grid()
        guesslabel = Label(dpph_popup, text="guess")
        guesslabel.grid(row=0, column=0)
        guessentry = Entry(dpph_popup, textvariable=self.guessval)
        guessentry.grid(row=0, column=1)
        unitsoption = OptionMenu(dpph_popup, self.guessunits, *["MHz", "kG"])
        unitsoption.grid(row=0, column=2)
        checkhall = Button(dpph_popup, text="Check Hall Probe",
                           command=self.checkhallprobe)
        checkhall.grid(row=1, column=0, columnspan=2)
        dorun = Button(dpph_popup, text="Start Scan", command=self.dpph_lockin)
        dorun.grid(row=1, column=2)
        savebutton = Button(dpph_popup, text="Save",
                            command=self.store_dpph_data)
        savebutton.grid(row=1, column=3)

    def checkhallprobe(self):
        halldoc = self.pype.Get('hall_probe_voltage').Wait()
        self.guessval.set(abs(float(halldoc['final'].split()[0])))
        self.guessunits.set('kG')

    def dpph_lockin(self):
        geff = 2.0036
        chargemass = 1.758e11
        freq_to_field = 4*pi*10**7/(geff*chargemass)
        if self.guessunits.get() == "kG":
            self.guessval.set(self.guessval.get()/freq_to_field)
            self.guessunits.set("MHz")
        self.dpph_result = scripts.dpph_lockin(self.pype, self.guessval.get())

    def store_dpph_data(self):
        if not self.dpph_result:
            print('no dpph_result stored')
            return
        outfile = tkFileDialog.asksaveasfile(defaultextension='.json')
        dump({"frequencies":self.dpph_result[0],
              "voltages":self.dpph_result[1]},
             outfile)
        outfile.close()

    def check_heartbeat(self):
        '''
            check dripline for a heartbeat
        '''
        scripts.check_pulse(self.pype)

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
