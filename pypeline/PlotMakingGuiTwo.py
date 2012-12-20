import Tkinter
import Pmw
import string
import time
import math
from datetime import datetime, timedelta

import LoggedDataMonitor
import LoggedDataMonitorPlotter
import CommandMonitor
import DripInterface
import usegnuplot


def start_plotgui():
	root=Tkinter.Tk()
	Pmw.initialise(root)
	root.title('P8 Plotting')
	widget=PlotMakingGuiTwo(root)
	root.mainloop()

class PlotMakingGuiTwo:
	def __init__(self,parent):
#		self.buttonbox=Pmw.RadioSelect(parent,labelpos='nw',label_text='sensors',orient='vertical',selectmode='multiple',buttontype='checkbutton')
#		self.buttonbox.pack(fill='both',padx=8,pady=8)
		notconsole=Tkinter.Frame(parent)
		plotcontrols=Tkinter.Frame(notconsole)
		buttonbox=Tkinter.Frame(plotcontrols);

		self.drip=DripInterface.DripInterface('http://p8portal.phys.washington.edu:5984')
		self.logg=LoggedDataMonitor.LoggedDataMonitor('http://p8portal.phys.washington.edu:5984')
		self.cmd=CommandMonitor.CommandMonitor('http://p8portal.phys.washington.edu:5984')
		self.logg.BeginContinuousUpdate()
		self.cmd.BeginContinuousUpdate()
#pmw complains if there are underscores in a button name
#possible cause: pmw was written by insects
        #button_names=[string.translate(x,string.maketransU('_',' ')) for x in sensors]
		sensors=self.logg.GetSensors()
		print sensors
		button_names=[self.python_is_horrible(x,"_"," ") for x in sensors]
		print button_names
#		for sensor in button_names:
#			self.buttonbox.add(sensor)
		self.selectedsensors={}
		self.sensor_display_labels={}
		for sensor in button_names:
			self.selectedsensors[sensor]=Tkinter.IntVar()
			thisbox=Tkinter.Frame(buttonbox)
			c=Tkinter.Checkbutton(thisbox,text=sensor,variable=self.selectedsensors[sensor])
			self.sensor_display_labels[sensor]=Tkinter.Label(thisbox,text="val")
			c.pack(side="left",anchor="w")
			self.sensor_display_labels[sensor].pack(side="left",anchor="e",expand=True)
			thisbox.pack(side="top",anchor="w",fill="x",expand=True)
		buttonbox.pack(side="top")
		self.plots = [None,None,None,None]
		self.plots[1]=LoggedDataMonitorPlotter.LoggedDataMonitorPlotter(self.logg)
		self.plots[1].StartUpdating()
		self.plots[2]=LoggedDataMonitorPlotter.LoggedDataMonitorPlotter(self.logg)
		self.plots[2].StartUpdating()
		self.plots[3]=LoggedDataMonitorPlotter.LoggedDataMonitorPlotter(self.logg)
		self.plots[3].StartUpdating()
		plotframe=Tkinter.Frame(plotcontrols)
		plotframe.pack(side="top")
		self.plotbutton_1=Tkinter.Button(plotframe,text="PLOT ON 1",command=lambda i=1: self.plot_pressed(i)).pack(side="left")
 		self.plotbutton_2=Tkinter.Button(plotframe,text="PLOT ON 2",command=lambda i=2: self.plot_pressed(i)).pack(side="left")
		self.plotbutton_3=Tkinter.Button(plotframe,text="PLOT ON 3",command=lambda i=3: self.plot_pressed(i)).pack(side="left")
		saveframe=Tkinter.Frame(plotcontrols)
		saveframe.pack(side="top")
		self.savebutton_1=Tkinter.Button(saveframe,text="SAVE 1",command=lambda i=1: self.save_pressed(i)).pack(side="left")
		self.savebutton_2=Tkinter.Button(saveframe,text="SAVE 2",command=lambda i=2: self.save_pressed(i)).pack(side="left")
		self.savebutton_3=Tkinter.Button(saveframe,text="SAVE 3",command=lambda i=3: self.save_pressed(i)).pack(side="left")
		plotcontrols.pack(side="left")
		settable_variables=["hf_cw_freq","hf_sweep_start","hf_sweep_stop","hf_sweep_time","hf_sweeper_power","lo_cw_freq","dpph_current","trap_current"]
		setcontrols=Tkinter.Frame(notconsole)
		self.set_entry_field={}
		for key in settable_variables:
			self.add_settable_line(key,setcontrols)
		digibutton1=Tkinter.Button(setcontrols,text="Digitize Channel 1",command=lambda i=1: self.digitize(i))
		digibutton1.pack(side="top")
		corrbutton1=Tkinter.Button(setcontrols,text="Correlate Channels",command=self.correlate)
		corrbutton1.pack(side="top")
		setcontrols.pack(side="left")
		notconsole.pack(side="top")
		cframe=Tkinter.Frame(parent)
		self.consoletext=Tkinter.Text(cframe)
		self.consoletext.pack(side="top")
		cframe.pack(side="bottom")
		self.logg.AddDoOnUpdate("update_gui_sensors",self.update_sensor_values)
		self.cmd.AddDoOnUpdate("update_console",self.do_on_command_update)

#        self.plot_start_time_entry=Pmw.EntryField(label_text="Start Time:",labelpos='w',value=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-60*60*3)))
#        self.plot_start_time_entry.pack(fill='x',padx=10,pady=10)
#        self.plot_stop_time_entry=Pmw.EntryField(label_text="Stop Time:",labelpos='w',value="now")
#        self.plot_stop_time_entry.pack(fill='x',padx=10,pady=10)



	def plot_pressed(self,whichwindow):
		button_names=[]
		for key in self.selectedsensors:
#			print key," is ", self.selectedsensors[key]
			if self.selectedsensors[key].get()==1:
				button_names.append(key)
#		button_names=self.buttonbox.getvalue()
		if len(button_names)==0:
			print "no sensors selected"
			return
#       sensors=[string.translate(x,string.maketrans(' ','_')) for x in button_names]
		sensors=[self.python_is_horrible(x," ","_") for x in button_names]
		print "setting "+str(whichwindow)+" to plot "
		print sensors
		self.plots[whichwindow].SetSensors(sensors)
	
	def save_pressed(self,whichwindow):
	    self.plots[whichwindow].SavePlotData()

	def python_is_horrible(self,s,a,b):
		ret=""
		for c in s:
			if c==a:
				ret=ret+b
			else:
				ret=ret+c
		return ret

	def update_sensor_values(self):
		for key in self.selectedsensors:
			varname=self.python_is_horrible(key," ","_") 
			self.sensor_display_labels[key].config(text='%.1f'%float(self.logg.values[varname][len(self.logg.values[varname])-1])+" "+self.logg.units[varname])
	
	def add_settable_line(self,sensorname,parent):
		c=Tkinter.Frame(parent)
		l=Tkinter.Label(c,text=self.python_is_horrible(sensorname,"_"," "))
		l.pack(side="left",anchor="w")
		self.set_entry_field[sensorname]=Tkinter.Entry(c,bg="white")
		self.set_entry_field[sensorname].pack(side="left",anchor="e")
		#What about units??
		#l2=Tkinter.Label(c,text="A")
		#l2.pack(side="left")
		sb=Tkinter.Button(c,text="Set",command=lambda x=sensorname: self.set_pressed(sensorname))
		sb.pack(side="left",anchor="e")
		c.pack(side="top",anchor="w",fill="x")

	def set_pressed(self,sensorname):
		print "set "+sensorname+" to "+self.set_entry_field[sensorname].get()
		self.drip.Set(sensorname,self.set_entry_field[sensorname].get())

	def do_on_command_update(self,command_entry):
		mytime=datetime.today().strftime("%Y-%m-%d %H:%M:%S")
#		if "result" in command_entry:
#			self.consoletext.insert("0.0",mytime+": "+str(command_entry["command"])+" result: "+str(command_entry["result"])+"\n")
#		else:
		self.consoletext.insert("0.0",mytime+": "+str(command_entry["command"])+"\n")

	def digitize(self,channel):
		run=eval(self.drip.CreatePowerSpectrum(self.drip.Run(rate=200,duration=100,filename="/data/temp.egg").Wait(),sp="powerline").Wait()['result'])
		dat=run['data']
		freqs=[]
		moddat=[ 10.0*math.log10(x) for x in dat ]
		for x in range(len(dat)):
			freqs.append(run['sampling_rate']*x/2.0)
		toplot=zip(freqs,moddat)
		g=usegnuplot.Gnuplot()
		g.gp("set style line 1 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 2")
		g.gp("set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2")
		g.gp("set style line 11 lc rgb '#808080' lt 1")
		g.gp("set border 3 back ls 11")
		g.gp("set tics nomirror")
		g.gp("set style line 12 lc rgb '#808080' lt 0 lw 1")
		g.gp("set grid back ls 12")
		g.gp("set xlabel \"Frequency (MHz)\"")
		g.gp("set ylabel \"Power (dBm)\"")
		g.gp("unset key")
		g.plot1d(toplot," with lines")

	def correlate(self):
		run=eval(self.drip.CreatePowerSpectrum(self.drip.Run(rate=200,duration=100,filename="/data/temp.egg").Wait(),sp="correline").Wait()['result'])
		dat=run['data']
		freqs=[]
#		moddat=[ 10.0*math.log10(x) for x in dat ]
		for x in range(len(dat)):
			freqs.append(run['sampling_rate']*x/2.0)
		toplot=zip(freqs,dat)
		g=usegnuplot.Gnuplot()
		g.gp("set style line 1 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 2")
		g.gp("set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2")
		g.gp("set style line 11 lc rgb '#808080' lt 1")
		g.gp("set border 3 back ls 11")
		g.gp("set tics nomirror")
		g.gp("set style line 12 lc rgb '#808080' lt 0 lw 1")
		g.gp("set grid back ls 12")
		g.gp("set xlabel \"Frequency (MHz)\"")
		g.gp("set ylabel \"Correlated Power\"")
		g.gp("unset key")
		g.plot1d(toplot," with lines")

		

		





