from Pypeline import DripInterface, peakdet
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import sys
import math
import time

drip = DripInterface('http://p8portal.phys.washington.edu:5984')

fname = str(time.time())
busycount = 0
busylim = 10
syncount = 0
synlim = 3
keycount = 0
keylim = 2
istart = 20
istop = 35
istep = 5
jstart = 300
jstop = 450
jstep = 50
transferx = []
transfery = []
transferz = []
drip.Set('hf_sweeper_power', '-90')
j = jstart
while j < jstop:
    i = istart
    drip.Set('lo_cw_freq',str(j))
    print "LO set for " + str(j) + " MHz"
    dumx = []
    dumy = []
    dumz = []
    while i < istop:
        drip.Set('hf_cw_freq',str(24500+j+i))
        print str(i) + " MHz"
        try:
            run = eval(repr(drip.Run())[1:-1])
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
            if math.floor(k[0]) == (i-istep):
                dumx.append(k[0])
                dumy.append(j)
                dumz.append(k[1])
        f = open('/Users/Micah/project8/Pypeline/scripts/run_data/' + fname + '.txt', 'a')
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
plt.savefig('/Users/Micah/project8/Pypeline/scripts/run_images/' + fname + '.jpg')
plt.show()
