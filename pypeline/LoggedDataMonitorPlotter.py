import LoggedDataMonitor
import usegnuplot
import threading
from uuid import uuid4
import time

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
        self.ymax=1000
        self.ymin=-1000

    def StartUpdating(self):
        self.Replot()
        self.data_store.AddDoOnUpdate(self.myid,self.Replot)

    def SavePlotData(self):
        if len(self.sensors_to_plot)==0:
            return
        plotsets=[]
        units=""
        filename=time.strftime("%Y_%m_%d_%H:%M:%S_",time.localtime())
        filename+=self.sensors_to_plot[0]+"_log.txt"
        self.sensors_to_plot_mutex.acquire()
        for sensor in self.sensors_to_plot:
            plotsets.append(self.data_store.GetTimeAndValues(sensor))
        self.sensors_to_plot_mutex.release()
        print("saving to "+filename)
        f=open(filename,"w")
        counter=0
        for dataset in plotsets:
            for entry in dataset:
            for elem in entry:
                f.write(str(elem)+" ")
            f.write(self.sensors_to_plot[counter])
            f.write("\n")
            counter=counter+1
        f.close()
            
    def Replot(self):
        if len(self.sensors_to_plot)==0:
            return
        plotsets=[]
        argsets = []
        units=""
        self.sensors_to_plot_mutex.acquire()
        for sensor in self.sensors_to_plot:
            vs=[ [x[0],self.ClipY(float(x[1]))] for x in self.data_store.GetTimeAndValues(sensor)]
            #plotsets.append(self.data_store.GetTimeAndValues(sensor))
            plotsets.append(vs)
            argsets.append("using 1:3 with lines title \""+sensor+"\"")
            units=self.data_store.GetUnits(sensor)
        self.sensors_to_plot_mutex.release()
        self.g.gp("set xdata time")
        self.g.gp("set style line 1 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 2")
        self.g.gp("set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2")
        self.g.gp("set style line 11 lc rgb '#808080' lt 1")
        self.g.gp("set border 3 back ls 11")
        self.g.gp("set tics nomirror")
        self.g.gp("set style line 12 lc rgb '#808080' lt 0 lw 1")
        self.g.gp("set grid back ls 12")
        self.g.gp("set timefmt \"%Y-%m-%d %H:%M:%S\"")
        self.g.gp("set format x \"%H:%M\"")
        self.g.gp("set ylabel \""+units+"\"")
        self.g.gp("set xlabel \"Time\"")
        self.g.plotMany(plotsets,argsets)

    def SetSensors(self,sensors):
        self.sensors_to_plot_mutex.acquire()
        self.sensors_to_plot=sensors
        self.sensors_to_plot_mutex.release()

    def ClipY(self,val):
        if val>self.ymax:
            return self.ymax
        if val<self.ymin:
            return self.ymin
        return val


        

