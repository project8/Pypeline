#!/usr/bin/python

#python3 prints and imports
from __future__ import print_function, absolute_import
#standard
import sys
from datetime import timedelta
#3rd party
import numpy
import matplotlib.pyplot as plt
#local
import pypeline

def get_noise_temp(start, stop):
    '''
    '''
    ych_name = 'power_meter_output'
    xch_name = 'terminator_temp'
    #time_format = '%Y-%m-%d %H:%M:%S'
    pype = pypeline.DripInterface('http://myrna.phys.washington.edu:5984')
    xraw = pype.GetTimeSeries(xch_name, start, stop)
    yraw = pype.GetTimeSeries(ych_name, start, stop)
    xdata=[]
    ydata=[]
    for tx, x in zip(xraw[0], xraw[1]):
        xtmp = False
        ytmp = False
        dt = timedelta(seconds=60)
        for ty, y in zip(yraw[0], yraw[1]):
            if abs(ty - tx) < dt:
                dt = abs(ty - tx)
                xtmp = x
                ytmp = y
            if dt < timedelta(seconds=1):
                break
        if xtmp and ytmp:
            xdata.append(xtmp)
            ydata.append(ytmp)
    [xdata, ydata] = zip(*sorted(zip(xdata,ydata)))
    xdimless = [x/xdata[0] for x in xdata]
    ydimless = [y/ydata[0] for y in ydata]
    [m, b] = numpy.polyfit(xdimless, ydimless, 1)
    print('noise temp is', b * xdata[0] / m)
    plt.plot(xdimless, ydimless,'bo', [xdimless[0],xdimless[-1]],[xdimless[0]*m+b,xdimless[-1]*m+b], 'r-')
    plt.show()

if __name__ == '__main__':
    get_noise_temp(*sys.argv[1:])
