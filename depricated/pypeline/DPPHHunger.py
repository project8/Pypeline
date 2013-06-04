import string
import time
import math

import Tkinter
import Pmw

import LoggedDataMonitor
import LoggedDataMonitorPlotter
import CommandMonitor
import DripInterface
import usegnuplot

class DPPHHunger:
	def __init__(self):
		self._Drip=DripInterface.DripInterface('http://p8portal.phys.washington.edu:5984')
		self._Log=LoggedDataMonitor.LoggedDataMonitor('http://p8portal.phys.washington.edu:5984')
		self._Cmd=CommandMonitor.CommandMonitor('http://p8portal.phys.washington.edu:5984')
		self._Log.BeginContinuousUpdate()
		self._Cmd.BeginContinuousUpdate()

		tRootFrame=Tkinter.Tk()
		Pmw.initialise(tRootFrame)
		tRootFrame.title('DPPH Hunger')
		tPanel=Tkinter.Frame(tRootFrame)		
		tButton=Tkinter.Button(tPanel,text="digitize",command=lambda: self.digitize())
		tRootFrame.mainloop()


	def digitize(self):
		tMantisOutput=self._Drip.RunMantis(rate=500,duration=1000,filename="/data/temp.egg",channels=1,length=4194304,count=600).Wait()['result']
		tPowerlineOutput=eval(self._Drip.RunPowerline(points=8192,events=1024,filename="/data/temp.egg").Wait()['result'])
		tSpectrum=tPowerlineOutput['data']
		tLogSpectrum=[ 10.0*math.log10(aValue) for aValue in tSpectrum ]
		tFrequencies=[ tPowerlineOutput['sampling_rate']*aValue/(2.0*len(tSpectrum)) for aValue in range(len(tSpectrum)) ]
		toplot=zip(tFrequencies,tLogSpectrum)
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