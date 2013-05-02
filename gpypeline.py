from Tkinter import *
from datetime import datetime
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
        self.time = StringVar()
        self.time.set(datetime.now())
        self.which_script = StringVar()
        self.which_script.set("check_heartbeat")

        # Text labels
        self.timedesc = Label(self.frame, text="The time is:", relief=RAISED)
        self.timedesc.grid(row=0, sticky=W)

        self.timeval = Label(self.frame, textvariable=self.time, relief=SUNKEN)
        self.timeval.grid(row=0, column=1)
       
        # Buttons
        self.hi_there = Button(self.frame, text="Hello", command=self.say_hi)
        self.hi_there.grid(row=1, column=1, sticky=W)

        self.script_selection = OptionMenu(self.frame, self.which_script, *['check_heartbeat', 'run_dpph'])
        self.script_selection.grid(row=2,column=0)
        
        self.run_script = Button(self.frame, text="Run", command=self.run_script)
        self.run_script.grid(row=2,column=1,sticky=W)


    def update_values(self):
        '''
            Update displayed values
        '''
        self.time.set(str(datetime.now()))
        self.timeval.after(200, self.update_values)

    def run_script(self):
        script_name = self.which_script.get()
        getattr(self, script_name)()

    def say_hi(self):
        print("hi there, everyone!")

    def run_dpph(self):
        '''
            Do a dpph run using the lockin method
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
        checkhall = Button(dpph_popup, text="Check Hall Probe", command=self.checkhallprobe)
        checkhall.grid(row=1, column=0, columnspan=2)
        dorun = Button(dpph_popup, text="Start Scan", command=self.dpph_lockin)
        dorun.grid(row=1, column=2)

    def checkhallprobe(self):
        halldoc = self.pype.Get('hall_probe_voltage').Wait()
        self.guessval.set(float(halldoc['final'].split()[0]))
        self.guessunits.set('kG')

    def dpph_lockin(self):
        geff = 2.0036
        chargemass = 1.758e11
        freq_to_field = 4*pi*10**7/(geff*chargemass)
        if self.guessunits.get() is "kG":
            self.guessval.set(self.guessval.get()/freq_to_field)
            self.guessunits.sset("MHz")
        scripts.dpph_lockin(self.pype, self.guessval.get())

    def check_heartbeat(self):
        '''
            check dripline for a heartbeat
        '''
        scripts.check_pulse(self.pype)

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
