#system
import sys
import math
import time
from datetime import datetime
from uuid import uuid4
#custom
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
#custom
from pypeline import DripInterface, peakdet

drip = DripInterface('http://p8portal.phys.washington.edu:5984')

fname = str(datetime.today().year) + str(datetime.today().month) + str(datetime.today().day) + str(datetime.today().hour) + str(datetime.today().minute) + str(datetime.today().second)
tempf = '/data/' + uuid4().hex + '.egg'
busycount = 0
busylim = 10
syncount = 0
synlim = 3
keycount = 0
keylim = 2
istart = 20
istop = 30
istep = 5
jstart = 700
jstop = 900
jstep = 100
transferx = []
transfery = []
transferz = []
drip.Set('hf_sweeper_power', '-75')
j = jstart
while j <= jstop:
    i = istart
    drip.Set('lo_cw_freq',str(j))
    print "LO set for " + str(j) + " MHz"
    dumx = []
    dumy = []
    dumz = []
    while i <= istop:
        drip.Set('hf_cw_freq',str(24500+j+i))
        print str(i) + " MHz"
        try:
            run = eval(eval(repr(drip.CreatePowerSpectrum(drip.Run(filename=tempf).Wait(), sp="powerline").Wait()))['result'])
            i = i + istep
            keycount = 0
            syncount = 0
            busycount = 0
        except KeyError:
            if keycount == keylim:
                print "KeyError at " + str(i) + " MHz"
                dumx.append(i)
                dumy.append(j)
                dumz.append(0)
                i = i + istep
                keycount = 0
            else:
                keycount = keycount + 1
                print "KeyError " + str(keycount) + " of " + str(keylim)
            continue
        except SyntaxError:
            if syncount == synlim:
                print "SyntaxError at " + str(i) + " MHz"
                dumx.append(i)
                dumy.append(j)
                dumz.append(0)
                i = i + istep
                syncount = 0
            else:
                syncount = syncount + 1
                print "SyntaxError " + str(syncount) + " of " + str(synlim)
            continue
        except NameError:
            time.sleep(30)
            if busycount == busylim:
                print "Timeout occurred at " + str(i) + " MHz"
                transferx = np.array(transferx)
                transfery = np.array(transfery)
                transferz = np.array(transferz)
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.plot_surface(transferx,transfery,transferz,cmap=cm.jet)
                #plt.plot(transferx, transfery, 'o')
                #plt.xlabel("Frequency (MHz)")
                #plt.ylabel("Peak Height (dBm)")
                #plt.title("Transfer Function")
                plt.show()
                raise
            else:
                busycount = busycount + 1
                print "NameError " + str(busycount) + " of " + str(busylim)
            continue
        except:
            print "Unexpected error:", sys.exc_info()[0]
            transferx = np.array(transferx)
            transfery = np.array(transfery)
            transferz = np.array(transferz)
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(transferx,transfery,transferz,cmap=cm.jet)
            #plt.plot(transferx, transfery, 'o')
            #plt.xlabel("Frequency (MHz)")
            #plt.ylabel("Peak Height (dBm)")
            #plt.title("Transfer Function")
            plt.show()
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
            if round(k[0]) == (i-istep):
                dumx.append(k[0])
                dumy.append(j)
                dumz.append(k[1])
        f = open('/Users/Micah/project8/pypeline/scripts/run_data/' + fname + '.txt', 'a')
        f.write(repr([dumx,dumy,dumz]))
        f.close()
        #print transferx
        #print transfery
    transferx.append(dumx)
    transfery.append(dumy)
    transferz.append(dumz)
    j = j + jstep

transferx = np.array(transferx)
transfery = np.array(transfery)
transferz = np.array(transferz)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(transferx,transfery,transferz,rstride=istep,cstride=jstep,cmap=cm.jet)
#plt.plot(transferx, transfery, 'o')
#plt.xlabel("Output Frequency (hf_cw_freq - 24.5 GHz - lo_cw_freq) (MHz)")
#plt.ylabel("Peak Height (dBm)")
#plt.title("Transfer Function")
plt.savefig('/Users/Micah/project8/pypeline/scripts/run_images/' + fname + '.jpg')
plt.show()
