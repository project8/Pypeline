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
		self.sweeper_power_default=-10
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
		dpphbgbutton=Tkinter.Button(dpphframe,text="DPPH Background",command=self.dpph_run_bg_threaded)
		dpphbgbutton.pack(side="top")
#		dpphwideframe=Tkinter.Frame(setcontrols)
#		dpphwideframe.pack(side="top")
#		dpphwidebutton=Tkinter.Button(dpphwideframe,text="DPPH Run Wide",command=self.dpph_run_wide_threaded)
#		dpphwidebutton.pack(side="left")
#		Tkinter.Label(dpphwideframe,text="Start Frequency").pack(side="left")
#		self.dpph_wide_freq_start_textbox=Tkinter.Entry(dpphwideframe,bg="white")
#		self.dpph_wide_freq_start_textbox.pack(side="left")
#		Tkinter.Label(dpphwideframe,text="Stop Frequency").pack(side="left")
#		self.dpph_wide_freq_stop_textbox=Tkinter.Entry(dpphwideframe,bg="white")
#		self.dpph_wide_freq_stop_textbox.pack(side="left")
		Tkinter.Label(dpphframe,text="Lower Frequency").pack(side="left")
		self.dpph_frequency_textbox=Tkinter.Entry(dpphframe,bg="white")
		self.dpph_frequency_textbox.pack(side="left")
		Tkinter.Label(dpphframe,text="Span").pack(side="left")
		self.dpph_span_textbox=Tkinter.Entry(dpphframe,bg="white")
		self.dpph_span_textbox.pack(side="left")
		
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
			fullresult=str(command_entry['result'])
			resultstring=fullresult[:20]+(fullresult[20:] and '..')
			self.consoletext.insert("0.0",mytime+": "+str(command_entry["command"])+" result: "+resultstring+"\n")
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

	def dpph_run_bg_threaded(self):
		freq=self.dpph_frequency_textbox.get()
		span=self.dpph_span_textbox.get()
		thethread=threading.Thread(target=lambda : self.dpph_run_step(freq,span,True))
		thethread.daemon=True
		thethread.start()

	def dpph_run_threaded(self):
		freq=self.dpph_frequency_textbox.get()
		span=self.dpph_span_textbox.get()
#		thethread=threading.Thread(target=lambda : self.dpph_run(freq))
		thethread=threading.Thread(target=lambda : self.dpph_run_step(freq,span,False))
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
		self.drip.Set("hf_sweeper_power",str(self.sweeper_power_default))
		lo_freq=str(int(freq)-24500)
		self.drip.Set("lo_cw_freq",lo_freq,True)
		run1=self.run_sweep(int(freq))
		self.drip.Set("dpph_current","2A",True)
		time.sleep(0.5)
		run2=self.run_sweep(int(freq))
		self.drip.Set("dpph_current","0A")
		freqs=[]
		diff=[]
		for x in range(len(run1['data'])):
			if (run1['freq'][x]-int(freq)<validstop) and (run1['freq'][x]-int(freq)>validstart):
				freqs.append(run1['freq'][x])
				diff.append((run1['data'][x]-run2['data'][x])/(run1['data'][x]+run2['data'][x]))
		toplot=zip(freqs,diff)
		return toplot

 	def dpph_run_wide_threaded(self):
		startfreq=self.dpph_wide_freq_start_textbox.get()
		stopfreq=self.dpph_wide_freq_stop_textbox.get()
		print "start frequency ",startfreq
		print "stop frequency ",stopfreq
		thethread=threading.Thread(target=lambda : self.dpph_run_wide(startfreq,stopfreq))
		thethread.daemon=True
		thethread.start()

	def dpph_run_wide(self,startfreq,stopfreq):
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

		datas=[]
		argsets=[]
		counters=[]
		nruns=int((int(stopfreq)-int(startfreq))/80)+1
		print "number of runs",nruns
		while True:
			for i in range(nruns):
				onfreq=int(startfreq)+i*80
				newdat=self.dpph_run_ret(onfreq)
				if len(datas)<=i:
					datas.append(newdat)
					counters.append(1)
				else:
					for j in range(len(datas[i])):
						datas[i][j]=(datas[i][j][0],datas[i][j][1]+newdat[j][1])
					counters[i]=counters[i]+1
				plotthings=[]
				argsets=[]
				for k in range(len(datas)):
					plotthings.append( [] )
					multiplier=1.0/float(counters[k])
					for m in range(len(datas[k])):
						plotthings[k].append( (datas[k][m][0],multiplier*(datas[k][m][1])) )
					argsets.append("using 1:2 with lines")
				g.plotMany(plotthings,argsets)

	def dpph_run_step(self,freq,span,isbg):
		validstart=10
		validstop=90
		nscans=int(int(span)/80)+1
		newscans=[]
		print "taking ",nscans," dpph scans"
		self.drip.Set("hf_sweeper_power",str(self.sweeper_power_default))
		for i in range(nscans):
			freqstart=int(freq)+i*80
			freqend=freqstart+100
			self.drip.Set("hf_sweep_start",str(freqstart))
			self.drip.Set("hf_sweep_stop",str(freqend))
			lo_freq=str(int(freqstart)-24500)
			self.drip.Set("lo_cw_freq",lo_freq,True)
			print "on frequency ",freqstart
			newscans.append(self.run_sweep(freqstart))
		if not isbg:
			argsets=[]
			toplot=[]
			filename="sweep_"+time.strftime("%Y_%m_%d_%H:%M:%S_",time.localtime())+".txt"
			f=open(filename,"w")
			for i in range(len(newscans)):
				diff=[]
				for j in range(len(newscans[i]['data'])):
#					print i," and ",j," newscans is ",newscans[i]['data'][j]
#					print i," and ",j," oldscans is ",self.last_dpph[i]['data'][j]
					x=newscans[i]['data'][j]
					y=self.last_dpph[i]['data'][j]
					deltaf=newscans[i]['freq'][j]-newscans[i]['freq'][0]
					if (deltaf<validstop) and (deltaf>validstart):
						if x+y==0:
							diff.append( (newscans[i]['freq'][j],0 ) )
						else:
							diff.append( (newscans[i]['freq'][j],(x-y)/(x+y)) )
							f.write( str(newscans[i]['freq'][j])+" "+str((x-y)/(x+y))+"\n")
				toplot.append(diff)
				argsets.append("using 1:2 with lines")
			f.close()
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
			argsets=[]
			toplot=[]
			for i in range(len(newscans)):
				subplot=[]
				for j in range(len(newscans[i]['data'])):
					deltaf=newscans[i]['freq'][j]-newscans[i]['freq'][0]
					if (deltaf<validstop) and (deltaf>validstart):
						subplot.append( (newscans[i]['freq'][j],newscans[i]['data'][j]) )
				toplot.append(subplot)
				argsets.append("using 1:(10.0*log10($2)) with lines")
			self.last_dpph=newscans
			self.dpph_set=True
 			g=usegnuplot.Gnuplot()
			g.gp("set style line 1 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 2")
			g.gp("set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2")
			g.gp("set style line 11 lc rgb '#808080' lt 1")
			g.gp("set border 3 back ls 11")
			g.gp("set tics nomirror")
			g.gp("set style line 12 lc rgb '#808080' lt 0 lw 1")
			g.gp("set grid back ls 12")
			g.gp("set xlabel \"Frequency (MHz)\"")
			g.gp("set ylabel \"Power\"")
			g.gp("unset key")
			g.plotMany(toplot,argsets)


	def run_sweep(self,freq_offset):
		myrate=200
		myduration=2000
		run=eval(self.drip.CreatePowerSpectrum(self.drip.Run(rate=myrate,duration=myduration,filename="/data/temp1.egg").Wait(),sp="sweepline").Wait()['result'])
		freqs=[]
		for x in range(len(run['data'])):
			freqs.append(int(freq_offset)+run['sampling_rate']*x/(2.0*(len(run['data']))))
		run['freq']=freqs
		return run
