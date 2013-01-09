import Tkinter
import Pmw
import string
import time

import LoggedDataHandler_Gnuplot


def start_plotgui():
    root=Tkinter.Tk()
    Pmw.initialise(root)
    root.title('P8 Plotting')
    widget=PlotMakingGui(root)
    root.mainloop()

class PlotMakingGui:
    def __init__(self,parent):
        self.buttonbox=Pmw.RadioSelect(parent,labelpos='nw',label_text='sensors',orient='vertical',selectmode='multiple',buttontype='checkbutton')
        self.buttonbox.pack(fill='both',padx=8,pady=8)
        self.logg=LoggedDataHandler_Gnuplot.LoggedDataHandler_Gnuplot('http://p8portal.phys.washington.edu:5984')
        sensors=self.logg.EligibleLoggers()
#pmw complains if there are underscores in a button name
#possible cause: pmw was written by insects
        #button_names=[string.translate(x,string.maketransU('_',' ')) for x in sensors]
        button_names=[self.python_is_horrible(x,"_"," ") for x in sensors]
        print(button_names)
        for sensor in button_names:
            self.buttonbox.add(sensor)
        self.plotbutton=Tkinter.Button(parent,text="PLOT",command=self.plot_pressed).pack()
        self.plot_start_time_entry=Pmw.EntryField(label_text="Start Time:",labelpos='w',value=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-60*60*3)))
        self.plot_start_time_entry.pack(fill='x',padx=10,pady=10)
        self.plot_stop_time_entry=Pmw.EntryField(label_text="Stop Time:",labelpos='w',value="now")
        self.plot_stop_time_entry.pack(fill='x',padx=10,pady=10)



    def plot_pressed(self):
        button_names=self.buttonbox.getvalue()
        if len(button_names)==0:
            print("no sensors selected")
            return
        #sensors=[string.translate(x,string.maketrans(' ','_')) for x in button_names]
        sensors=[self.python_is_horrible(x," ","_") for x in button_names]
        if self.plot_stop_time_entry.getvalue()=="now":
            self.logg.Plot(sensors=sensors,start=self.plot_start_time_entry.getvalue())
        else:
            self.logg.Plot(sensors=sensors,start=self.plot_start_time_entry.getvalue(),stop=self.plot_stop_time_entry.getvalue())


    def python_is_horrible(self,s,a,b):
        ret=""
        for c in s:
            if c==a:
                ret=ret+b
            else:
                ret=ret+c
        return ret
