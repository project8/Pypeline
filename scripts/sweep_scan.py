from pypeline import DripInterface, peakdet
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import sys
import math
import time
from datetime import datetime
from uuid import uuid4

drip = DripInterface('http://p8portal.phys.washington.edu:5984')

fname = str(datetime.today().year) + str(datetime.today().month) + str(datetime.today().day) + str(datetime.today().hour) + str(datetime.today().minute) + str(datetime.today().second)
tempf = '/data/' + uuid4().hex + '.egg'
transferx = []
transfery = []
transferz = []
lostart = 400
lostop = 2000
lostep = 10

lo = lostart
drip.Set('hf_sweeper_power','-65')
drip.Set('hf_sweep_time',10)
while lo <= lostop:
    drip.Set('lo_cw_freq',lo)
    print "lo set to " + str(lo)
    drip.Set('hf_sweep_start',lo+24500)
    drip.Set('hf_sweep_stop',lo+24600)
    run = eval(eval(repr(drip.CreatePowerSpectrum(drip.Run(filename=tempf, rate=250).Wait(), sp="sweepline").Wait()))['result'])
    power = run['data']
    freq = np.linspace(0,run['sampling_rate']/2,len(power))
    for i in range(len(freq)):
        if freq[i] > 90:
            stop = i
            break
    for i in range(len(freq)):
        if freq[i] > 10:
            start = i
            break
    power = power[start:stop]
    freq = freq[start:stop]
    logpower = [10*math.log(a,10) for a in power]
    transferx.append(freq)
    transfery.append(np.linspace(lo,lo,len(freq)))
    transferz.append(logpower)
    lo = lo + lostep

transferx = np.array(transferx)
transfery = np.array(transfery)
transferz = np.array(transferz)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(transferx, transfery, transferz, rstride=1, cstride=1, cmap=cm.jet, linewidth=0)
plt.show()
