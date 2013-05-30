#from pypeline import LoggedDataMonitor
#from pypeline import LoggedDataMonitorPlotter
#import time
#x=LoggedDataMonitor.LoggedDataMonitor('http://p8portal.phys.washington.edu:5984')
#x.BeginContinuousUpdate()
#y=LoggedDataMonitorPlotter.LoggedDataMonitorPlotter(x)
#y.sensors_to_plot=['waveguide_cell_body_t']
#y.StartUpdating()
#while True:
#	time.sleep(5)
from pypeline import DPPHHunger

tDPPH=DPPHHunger.DPPHHunger()
tDPPH.digitize()
