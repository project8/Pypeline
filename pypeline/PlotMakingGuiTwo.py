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
		settable_variables=["hf_cw_freq","hf_sweep_start","hf_sweep_stop","hf_sweep_time","hf_sweeper_power","lo_cw_freq","dpph_current","trap_current","waveguide_cell_heater_current"]
		setcontrols=Tkinter.Frame(notconsole)
		self.set_entry_field={}
		for key in settable_variables:
			self.add_settable_line(key,setcontrols)
		digibutton1=Tkinter.Button(setcontrols,text="Digitize Channel 1",command=lambda i=1: self.digitize(i))
		digibutton1.pack(side="top")
		corrbutton1=Tkinter.Button(setcontrols,text="Correlate Channels",command=self.correlate)
		corrbutton1.pack(side="top")
		dpphframe=Tkinter.Frame(setcontrols)
		dpphbutton=Tkinter.Button(dpphframe,text="DPPH Run",command=self.dpph_run_threaded)
		dpphbutton.pack(side="left")
		dpphwidebutton=Tkinter.Button(setcontrols,text="DPPH Run Wide",command=self.dpph_run_wide_threaded)
		dpphwidebutton.pack(side="top")
		Tkinter.Label(dpphframe,text="Frequency").pack(side="left")
		self.dpph_frequency_textbox=Tkinter.Entry(dpphframe,bg="white")
		self.dpph_frequency_textbox.pack(side="left")
		dpphframe.pack(side="top")
		setcontrols.pack(side="left")
		notconsole.pack(side="top")
		cframe=Tkinter.Frame(parent)
		self.consoletext=Tkinter.Text(cframe)
		self.consoletext.pack(side="top")
		cframe.pack(side="bottom")
		self.logg.AddDoOnUpdate("update_gui_sensors",self.update_sensor_values)
		self.cmd.AddDoOnUpdate("update_console",self.do_on_command_update)
		self.dpph_set=False

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
			theval=float(self.logg.values[varname][len(self.logg.values[varname])-1])
			if abs(theval) > 0.1:
				self.sensor_display_labels[key].config(text='%.1f'%theval+" "+self.logg.units[varname])
			else:
				self.sensor_display_labels[key].config(text='%.1g'%theval+" "+self.logg.units[varname])
	
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
		if "result" in command_entry:
			self.consoletext.insert("0.0",mytime+": "+str(command_entry["command"])+" result: "+str(command_entry["result"])+"\n")
		else:
			self.consoletext.insert("0.0",mytime+": "+str(command_entry["command"])+"\n")

	def digitize(self,channel):
		run=eval(self.drip.CreatePowerSpectrum(self.drip.Run(rate=200,duration=100,filename="/data/temp.egg").Wait(),sp="powerline").Wait()['result'])
		dat=run['data']
		freqs=[]
		moddat=[ 10.0*math.log10(x) for x in dat ]
		for x in range(len(dat)):
			freqs.append(run['sampling_rate']*x/(2.0*len(dat)))
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
			freqs.append(run['sampling_rate']*x/(2.0*1e6))
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

	def dpph_run_threaded(self):
		freq=self.dpph_frequency_textbox.get()
#		thethread=threading.Thread(target=lambda : self.dpph_run(freq))
		thethread=threading.Thread(target=lambda : self.dpph_run_step(freq,240))
		thethread.daemon=True
		thethread.start()
		
	def dpph_run(self,freq):
		toplot=self.dpph_run_ret(freq)
 		g=usegnuplot.Gnuplot()
		g.gp("set style line 1 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 2")
		g.gp("set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2")
		g.gp("set style line 11 lc rgb '#808080' lt 1")
		g.gp("set border 3 back ls 11")
		g.gp("set tics nomirror")
		g.gp("set style line 12 lc rgb '#808080' lt 0 lw 1")
		g.gp("set grid back ls 12")
		g.gp("set xlabel \"Frequency (MHz)\"")
		g.gp("set ylabel \"Normalized Difference\"")
		g.gp("unset key")
		g.plot1d(toplot," with lines")

	def dpph_run_ret(self,freq,validstart=10,validstop=90):
		freqend=int(freq)+100
		inttime=4000
		self.drip.Set("dpph_current","0A",True)
		self.drip.Set("hf_sweep_start",freq)
		self.drip.Set("hf_sweep_stop",str(freqend))
		self.drip.Set("hf_sweeper_power",-20)
		lo_freq=str(int(freq)-24500)
		self.drip.Set("lo_cw_freq",lo_freq,True)
		run1=eval(self.drip.CreatePowerSpectrum(self.drip.Run(rate=200,duration=1000,filename="/data/temp1.egg").Wait(),sp="powerline").Wait()['result'])
		dat1=run1['data']
		self.drip.Set("dpph_current","2A",True)
		time.sleep(1)
		run2=eval(self.drip.CreatePowerSpectrum(self.drip.Run(rate=200,duration=1000,filename="/data/temp2.egg").Wait(),sp="powerline").Wait()['result'])
		dat2=run2['data']
		diff=[]
		freqs=[]
		self.drip.Set("dpph_current","0A")
		for x in range(len(dat1)):
			if (run2['sampling_rate']*x/(2.0*(len(dat1)))<validstop) and (run2['sampling_rate']*x/(2.0*(len(dat1)))>validstart):
				freqs.append(int(freq)+run2['sampling_rate']*x/(2.0*(len(dat1))))
				diff.append((dat1[x]-dat2[x])/(dat1[x]+dat2[x]))
		toplot=zip(freqs,diff)
		return toplot

 	def dpph_run_wide_threaded(self):
		freq=self.dpph_frequency_textbox.get()
		thethread=threading.Thread(target=lambda : self.dpph_run_wide())
		thethread.daemon=True
		thethread.start()

	def dpph_run_wide(self):
		plotthings=[]
		argsets=[]
		for i in range(18):
			onfreq=25000+i*80
			plotthings.append(self.dpph_run_ret(onfreq))
			argsets.append("using 1:2 with lines")
 		g=usegnuplot.Gnuplot()
		g.gp("set style line 1 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 2")
		g.gp("set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2")
		g.gp("set style line 11 lc rgb '#808080' lt 1")
		g.gp("set border 3 back ls 11")
		g.gp("set tics nomirror")
		g.gp("set style line 12 lc rgb '#808080' lt 0 lw 1")
		g.gp("set grid back ls 12")
		g.gp("set xlabel \"Frequency (MHz)\"")
		g.gp("set ylabel \"Normalized Difference\"")
		g.gp("unset key")
		#g.plot1d(toplot," with lines")
		g.plotMany(plotthings,argsets)

	def dpph_run_step(self,freq,span):
		validstart=10
		validstop=90
		nscans=int(span/80)
		newscans=[]
		newfreqs=[]
		print "taking ",nscans," dpph scans"
		self.drip.Set("hf_sweeper_power",-10)
		for i in range(nscans):
			freqstart=int(freq)+i*80
			freqend=int(freqstart)+100
			inttime=2000
			self.drip.Set("hf_sweep_start",freq)
			self.drip.Set("hf_sweep_stop",str(freqend))
			lo_freq=str(int(freq)-24500)
			self.drip.Set("lo_cw_freq",lo_freq,True)
			time.sleep(0.1)
			run1=eval(self.drip.CreatePowerSpectrum(self.drip.Run(rate=200,duration=inttime,filename="/data/temp1.egg").Wait(),sp="sweepline").Wait()['result'])
			dat1=run1['data']
			freqs=[]
			for x in range(len(dat1)):
				freqs.append(int(freqstart)+run1['sampling_rate']*x/(2.0*(len(dat1))))
			newfreqs.append(freqs)
			newscans.append(dat1)
		if self.dpph_set:
			argsets=[]
			toplot=[]
			for i in range(len(newscans)):
				diff=[]
				for j in range(len(newscans[i])):
					diff.append((newscans[i][j]-self.last_dpph[i][j])/(newscans[i][j]+self.last_dpph[i][j]))
				toplot.append(zip(newfreqs[i],diff))
				argsets.append("using 1:2 with lines")
 			g=usegnuplot.Gnuplot()
			g.gp("set style line 1 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 2")
			g.gp("set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2")
			g.gp("set style line 11 lc rgb '#808080' lt 1")
			g.gp("set border 3 back ls 11")
			g.gp("set tics nomirror")
			g.gp("set style line 12 lc rgb '#808080' lt 0 lw 1")
			g.gp("set grid back ls 12")
			g.gp("set xlabel \"Frequency (MHz)\"")
			g.gp("set ylabel \"Normalized Difference\"")
			g.gp("unset key")
			g.plotMany(toplot,argsets)
		else:
			print "Initial DPPH Scan done"
		self.dpph_set=True
		self.last_dpph=newscans













		

		





