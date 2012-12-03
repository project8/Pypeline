import Tkinter
import Pmw
import string
import time

import LoggedDataMonitor
import LoggedDataMonitorPlotter


def start_plotgui():
	root=Tkinter.Tk()
	Pmw.initialise(root)
	root.title('P8 Plotting')
	widget=PlotMakingGuiTwo(root)
	root.mainloop()

class PlotMakingGuiTwo:
	def __init__(self,parent):
		self.buttonbox=Pmw.RadioSelect(parent,labelpos='nw',label_text='sensors',orient='vertical',selectmode='multiple',buttontype='checkbutton')
		self.buttonbox.pack(fill='both',padx=8,pady=8)
		self.logg=LoggedDataMonitor.LoggedDataMonitor('http://p8portal.phys.washington.edu:5984')
		self.logg.BeginContinuousUpdate()
#pmw complains if there are underscores in a button name
#possible cause: pmw was written by insects
        #button_names=[string.translate(x,string.maketransU('_',' ')) for x in sensors]
		sensors=self.logg.GetSensors()
		print sensors
		button_names=[self.python_is_horrible(x,"_"," ") for x in sensors]
		print button_names
		for sensor in button_names:
			self.buttonbox.add(sensor)
		self.plots = [None,None,None,None]
		self.plots[1]=LoggedDataMonitorPlotter.LoggedDataMonitorPlotter(self.logg)
		self.plots[1].StartUpdating()
		self.plots[2]=LoggedDataMonitorPlotter.LoggedDataMonitorPlotter(self.logg)
		self.plots[2].StartUpdating()
		self.plots[3]=LoggedDataMonitorPlotter.LoggedDataMonitorPlotter(self.logg)
		self.plots[3].StartUpdating()
		self.plotbutton_1=Tkinter.Button(parent,text="PLOT ON 1",command=lambda i=1: self.plot_pressed(i)).pack()
 		self.plotbutton_2=Tkinter.Button(parent,text="PLOT ON 2",command=lambda i=2: self.plot_pressed(i)).pack()
		self.plotbutton_3=Tkinter.Button(parent,text="PLOT ON 3",command=lambda i=3: self.plot_pressed(i)).pack()
#        self.plot_start_time_entry=Pmw.EntryField(label_text="Start Time:",labelpos='w',value=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-60*60*3)))
#        self.plot_start_time_entry.pack(fill='x',padx=10,pady=10)
#        self.plot_stop_time_entry=Pmw.EntryField(label_text="Stop Time:",labelpos='w',value="now")
#        self.plot_stop_time_entry.pack(fill='x',padx=10,pady=10)



	def plot_pressed(self,whichwindow):
		button_names=self.buttonbox.getvalue()
		if len(button_names)==0:
			print "no sensors selected"
			return
        #sensors=[string.translate(x,string.maketrans(' ','_')) for x in button_names]
		sensors=[self.python_is_horrible(x," ","_") for x in button_names]
		print "setting "+str(whichwindow)+" to plot "
		print sensors
		self.plots[whichwindow].SetSensors(sensors)

	def python_is_horrible(self,s,a,b):
		ret=""
		for c in s:
			if c==a:
				ret=ret+b
			else:
				ret=ret+c
		return ret
