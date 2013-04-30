from Tkinter import *
from datetime import datetime
from pypeline import DripInterface, dpph_lockin, scripts


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

        # Text labels
        self.timedesc = Label(self.frame, text="The time is:", relief=RAISED)
        self.timedesc.grid(row=0, sticky=W)

        self.timeval = Label(self.frame, textvariable=self.time, relief=SUNKEN)
        self.timeval.grid(row=0, column=1)
       
        # Buttons
        self.button = Button(self.frame, text="QUIT", fg="red", command=self.frame.quit)
        self.button.grid(row=1, column=0)

        self.hi_there = Button(self.frame, text="Hello", command=self.say_hi)
        self.hi_there.grid(row=1, column=1, sticky=W)

        #self.update = Button(self.frame, text="Update", command=self.update_values)
        #self.update.grid(row=1, column=2, sticky=E)

        self.check_heartbeat = Button(self.frame, text="Check Heartbeat", command=self.check_heartbeat)
        self.check_heartbeat.grid(row=1, column=3)

        self.run_dpph = Button(self.frame, text="DPPH", command=self.run_dpph)
        self.run_dpph.grid(row=1, column=2)


    def update_values(self):
        '''
            Update displayed values
        '''
        self.time.set(str(datetime.now()))
        self.timeval.after(200, self.update_values)

    def say_hi(self):
        print("hi there, everyone!")

    def run_dpph(self):
        '''
            Do a dpph run using the lockin method
        '''
        dpph_lockin(self.pype)

    def check_heartbeat(self):
        '''
            check dripline for a heartbeat
        '''
        scripts.check_pulse(self.pype)

root = Tk()
app = App(root)
root.mainloop()
