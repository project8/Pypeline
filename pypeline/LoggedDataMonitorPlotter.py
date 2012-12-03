import LoggedDataMonitor
import usegnuplot
import threading
from uuid import uuid4

class LoggedDataMonitorPlotter:
	'''
		Class that plots data from a data monitor
	'''
	def __init__(self,data_store):
		self.data_store=data_store
		self.sensors_to_plot=[]
		self.sensors_to_plot_mutex=threading.Lock()
		self.g=usegnuplot.Gnuplot()
		self.myid=uuid4()

	def StartUpdating(self):
		self.data_store.AddDoOnUpdate(self.myid,self.Replot)

	def Replot(self):
		if len(self.sensors_to_plot)==0:
			return
		plotsets=[]
		argsets = []
		units=""
		self.sensors_to_plot_mutex.acquire()
		for sensor in self.sensors_to_plot:
			plotsets.append(self.data_store.GetTimeAndValues(sensor))
			argsets.append("using 1:3 with lines title \""+sensor+"\"")
			units=self.data_store.GetUnits(sensor)
		self.sensors_to_plot_mutex.release()
		self.g.gp("set xdata time")
		self.g.gp("set timefmt \"%Y-%m-%d %H:%M:%S\"")
		self.g.gp("set format x \"%H:%M\"")
		self.g.gp("set ylabel \""+units+"\"")
		self.g.gp("set xlabel \"Time\"")
		self.g.plotMany(plotsets,argsets)

	def SetSensors(self,sensors):
		self.sensors_to_plot_mutex.acquire()
		self.sensors_to_plot=sensors
		self.sensors_to_plot_mutex.release()



		

