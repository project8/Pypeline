import Tkinter
import Pmw
import string
import time
import math
import threading
from datetime import datetime, timedelta

import LoggedDataMonitor
import LoggedDataMonitorPlotter
import CommandMonitor
import DripInterface

def start_loggergui():
    root=Tkinter.Tk()
    Pmw.initialise(root)
    root.title=('P8 Logger Control')
    widget=LoggerGui(root)
    root.mainloop();

class LoggerGui:
    def __init__(self,parent):
        self.drip=DripInterface.DripInterface('http://p8portal.phys.washington.edu:5984')
        self.button_vars={}
        eligible_loggers=self.drip._conf_interface.EligibleLoggers()
        current_loggers=self.drip.CurrentLoggers(True)
        print current_loggers
        for x in eligible_loggers:
            if x in current_loggers:
                self.addLoggerButton(x,parent,True)
            else:
                self.addLoggerButton(x,parent,False)

    def addLoggerButton(self,loggername,parent,ison):
        print loggername
        thisbox=Tkinter.Frame(parent)
        Tkinter.Label(thisbox,text=loggername).pack(side="left")
        self.button_vars[loggername]=Tkinter.StringVar()
        if ison:
            self.button_vars[loggername].set("ON")
        else:
            self.button_vars[loggername].set("OFF")
        a=Tkinter.Radiobutton(thisbox,text="On",variable=self.button_vars[loggername],value="ON",indicatoron=0,command=lambda x=loggername:self.button_pressed(x))
        a.pack(side="left")
        b=Tkinter.Radiobutton(thisbox,text="Off",variable=self.button_vars[loggername],value="OFF",indicatoron=0,command=lambda x=loggername:self.button_pressed(x))
        b.pack(side="left")
        thisbox.pack(side="top",anchor="e")

    def button_pressed(self,loggername):
        val=self.button_vars[loggername].get()
        if val=="ON":
            print "turning logger", loggername, "on"
            self.drip.StartLoggers(loggername)
        else:
            print "turning logger", loggername, "off"
            self.drip.StopLoggers(loggername)

        

