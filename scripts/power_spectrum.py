from Pypeline import DripInterface, peakdet
import numpy as np
import matplotlib.pyplot as plt
import sys

drip = DripInterface('http://p8portal.phys.washington.edu:5984')

if len(sys.argv) == 1:
    dur = '250'
    srate = '500'
    short_run =  eval(repr(drip.Run())[1:-1])
elif len(sys.argv) == 2:
    dur = sys.argv[1]
    srate = '500'
    short_run = eval(repr(drip.Run(duration=dur))[1:-1])
elif len(sys.argv) == 3:
    dur = sys.argv[1]
    srate = sys.argv[2]
    short_run = eval(repr(drip.Run(rate=srate, duration=dur))[1:-1])
else:
    print "Error: Incorrect number of arguments"
    sys.exit()

y = short_run['data']
x = np.linspace(0,short_run['sampling_rate']/2,len(y))
y = y[1:-1]
x = x[1:-1]
print peakdet(y,0.5,x)
plt.plot(x,y)
plt.title("Power Spectrum (Sampling Rate = " + srate + " MHz, Duration = " + dur + " ms)")
plt.xlabel("Frequency (MHz)")
plt.ylabel("Power (mW)")
plt.show()
