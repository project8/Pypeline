from Pypeline import DripInterface, peakdet
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

fname1 = str(datetime.today().year) + str(datetime.today().month) + str(datetime.today().day) + str(datetime.today().hour) + str(datetime.today().minute) + str(datetime.today().second) + '.1'
fname2 = str(datetime.today().year) + str(datetime.today().month) + str(datetime.today().day) + str(datetime.today().hour) + str(datetime.today().minute) + str(datetime.today().second) + '.2'
tempf = '/data/' + uuid4().hex + '.egg'
busycount = 0
busylim = 10
syncount = 0
synlim = 3
keycount = 0
keylim = 2
hfstart = 30
hfstop = 100
hfstep = 10
lo = 1000
sumx1 = []
sumy1 = []
sumx2 = []
sumy2 = []
drip.Set('hf_sweeper_power', '-90')
print "First run:"
hf = hfstart
drip.Set('lo_cw_freq',str(lo))
print "LO set for " + str(lo) + " MHz"
while hf <= hfstop:
    drip.Set('hf_cw_freq',str(24500+lo+hf))
    print str(hf) + " MHz"
    try:
        time.sleep(10)
        run = eval(repr(drip.Run(filename=tempf))[1:-1])
        hf = hf + hfstep
        keycount = 0
        syncount = 0
        busycount = 0
    except KeyError:
        if keycount == keylim:
            print "KeyError at " + str(hf) + " MHz"
            sumx1.append(hf)
            sumy1.append(0)
            hf = hf + hfstep
            keycount = 0
        else:
            keycount = keycount + 1
            print "KeyError " + str(keycount) + " of " + str(keylim)
            time.sleep(20)
        continue
    except SyntaxError:
        if syncount == synlim:
            print "SyntaxError at " + str(hf) + " MHz"
            sumx1.append(hf)
            sumy1.append(0)
            hf = hf + hfstep
            syncount = 0
        else:
            syncount = syncount + 1
            print "SyntaxError " + str(syncount) + " of " + str(synlim)
        continue
    except NameError:
        time.sleep(30)
        if busycount == busylim:
            print "Timeout occurred at " + str(hf) + " MHz"
            raise
        else:
            busycount = busycount + 1
            print "NameError " + str(busycount) + " of " + str(busylim)
        continue
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    power = run['data']
    freq = np.linspace(0,run['sampling_rate']/2,len(power))
    power = power[1:-1]
    freq = freq[1:-1]
    logpower = [10*math.log(a,10) for a in power]
    #plt.plot(x,logy)
    peaks = peakdet(logpower,2,freq)
    #print peaks[0]
    for k in peaks[0]:
        #print j
        #print i-step
        if math.floor(k[0]) == (hf-hfstep):
            sumx1.append(k[0])
            sumy1.append(k[1])
            f = open('/Users/Micah/project8/Pypeline/scripts/dpph_data/' + fname1 + '.txt', 'a')
            f.write(repr([k[0],k[1]]))
            f.close()

# Pause to set new magnetic field value
raw_input("Set new magnetic field, then press enter.")

print "Second run:"
hf = hfstart
while hf <= hfstop:
    drip.Set('hf_cw_freq',str(24500+lo+hf))
    print str(hf) + " MHz"
    try:
        time.sleep(10)
        run = eval(repr(drip.Run(filename=tempf))[1:-1])
        hf = hf + hfstep
        keycount = 0
        syncount = 0
        busycount = 0
    except KeyError:
        if keycount == keylim:
            print "KeyError at " + str(hf) + " MHz"
            sumx2.append(hf)
            sumy2.append(0)
            hf = hf + hfstep
            keycount = 0
        else:
            keycount = keycount + 1
            print "KeyError " + str(keycount) + " of " + str(keylim)
            time.sleep(20)
        continue
    except SyntaxError:
        if syncount == synlim:
            print "SyntaxError at " + str(hf) + " MHz"
            sumx2.append(hf)
            sumy2.append(0)
            hf = hf + hfstep
            syncount = 0
        else:
            syncount = syncount + 1
            print "SyntaxError " + str(syncount) + " of " + str(synlim)
        continue
    except NameError:
        time.sleep(30)
        if busycount == busylim:
            print "Timeout occurred at " + str(hf) + " MHz"
            raise
        else:
            busycount = busycount + 1
            print "NameError " + str(busycount) + " of " + str(busylim)
        continue
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    power = run['data']
    freq = np.linspace(0,run['sampling_rate']/2,len(power))
    power = power[1:-1]
    freq = freq[1:-1]
    logpower = [10*math.log(a,10) for a in power]
    #plt.plot(x,logy)
    peaks = peakdet(logpower,2,freq)
    #print peaks[0]
    for k in peaks[0]:
        #print j
        #print i-step
        if math.floor(k[0]) == (hf-hfstep):
            sumx2.append(k[0])
            sumy2.append(k[1])
            f = open('/Users/Micah/project8/Pypeline/scripts/dpph_data/' + fname2 + '.txt', 'a')
            f.write(repr([k[0],k[1]]))
            f.close()

sumx = sumx1
sumy = [sumy1[i] - sumy2[i] for i in range(len(sumy1))]
plt.plot(sumx, sumy, 'o')
plt.xlabel("Output Frequency (hf_cw_freq - 24.5 GHz - lo_cw_freq) (MHz)")
plt.ylabel("Peak Height (dBm)")
plt.title("DPPH Resonance")
plt.savefig('/Users/Micah/project8/Pypeline/scripts/dpph_images/' + fname1 + '.jpg')
plt.show()
