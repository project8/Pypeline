import Tkinter
import Pmw
import string

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
        button_names=[string.translate(x,string.maketrans('_',' ')) for x in sensors]
        print button_names
        for sensor in button_names:
            self.buttonbox.add(sensor)
        self.plotbutton=Tkinter.Button(parent,text="PLOT",command=self.plot_pressed).pack()

    def plot_pressed(self):
        button_names=self.buttonbox.getvalue()
        if len(button_names)==0:
            print "no sensors selected"
            return
        sensors=[string.translate(x,string.maketrans(' ','_')) for x in button_names]
        self.logg.Plot(sensors)

