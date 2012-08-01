from DripInterface import DripInterface
import numpy as np
import matplotlib.pyplot as plt
import math
import sys
from uuid import uuid4
from datetime import datetime
from scipy import special

drip = DripInterface('http://p8portal.phys.washington.edu:5984')
tempf = '/data/' + uuid4().hex + '.egg'
fname = str(datetime.today().year) + str(datetime.today().month) + str(datetime.today().day) + str(datetime.today().hour) + str(datetime.today().minute) + str(datetime.today().second)
conflevel = .005

#Hall Probe Calibration Data
conv = 118 #T/V

#Estimate field with Hall Probe
guess = round(abs(float(repr(drip.Get('hall_probe_voltage'))[1:16]))*conv,3)
#print "Hall Probe Estimated Field: " + str(guess) + " T"

#Find precise field with DPPH
DPPH = 28042.9 #MHz/T
target = int(round(guess*DPPH))
if target < 24590:
    sys.exit("Field strength too low, (must be at least .877 T)")

drip.Set('pancake_coil_current','enable')
drip.Set('pancake_coil_current','0A')
drip.Set('hf_sweep_start', target-90)
drip.Set('hf_sweep_stop', target+10)
drip.Set('lo_cw_freq', target-24590)
drip.Set('hf_sweep_time', 10)
sigrun1 = eval(repr(drip.Run(subprocess = "sweepline", duration = 2000, filename = tempf))[1:-1])
#print "Signal run 1 of 2 complete"
sigpow1 = sigrun1['data']
sigfreq1 = list(np.linspace(target-90,sigrun1['sampling_rate']/2+target-90,len(sigpow1)))
sigpow1 = sigpow1[21:184]
sigfreq1 = sigfreq1[21:184]
drip.Set('pancake_coil_current','4A')
bgrun1 = eval(repr(drip.Run(subprocess = "sweepline", duration = 2000, filename = tempf))[1:-1])
#print "Background run 1 of 2 complete"
bgpow1 = bgrun1['data']
bgfreq1 = list(np.linspace(target-90,bgrun1['sampling_rate']/2+target-90,len(bgpow1)))
bgpow1 = bgpow1[21:184]
bgfreq1 = bgfreq1[21:184]

drip.Set('pancake_coil_current','0A')
drip.Set('hf_sweep_start', target-10)
drip.Set('hf_sweep_stop', target+90)
drip.Set('lo_cw_freq', target-24510)
sigrun2 = eval(repr(drip.Run(subprocess = "sweepline", duration = 2000, filename = tempf))[1:-1])
#print "Signal run 2 of 2 complete"
sigpow2 = sigrun2['data']
sigfreq2 = list(np.linspace(target-10,sigrun2['sampling_rate']/2 + target-10,len(sigpow2)))
sigpow2 = sigpow2[21:184]
sigfreq2 = sigfreq2[21:184]
drip.Set('pancake_coil_current','4A')
bgrun2 = eval(repr(drip.Run(subprocess = "sweepline", duration = 2000, filename = tempf))[1:-1])
#print "Background run 2 of 2 complete"
bgpow2 = bgrun2['data']
bgfreq2 = np.linspace(target-10,bgrun2['sampling_rate']/2 + target-10,len(bgpow2))
bgpow2 = bgpow2[21:184]
bgfreq2 = bgfreq2[21:184]
freq = sigfreq1 + sigfreq2
sigpow = sigpow1 + sigpow2
bgpow = bgpow1 + bgpow2
drip.Set('pancake_coil_current','0A')

WINDOW = 5
weightings = np.repeat(1.0, WINDOW) / WINDOW
sigavg1 = np.convolve(sigpow1, weightings)[WINDOW-1:-(WINDOW-1)]
bgavg1 = np.convolve(bgpow1, weightings)[WINDOW-1:-(WINDOW-1)]
diffavg1 = [sigavg1[i] - bgavg1[i] for i in range(len(sigavg1))]
sigavg2 = np.convolve(sigpow2, weightings)[WINDOW-1:-(WINDOW-1)]
bgavg2 = np.convolve(bgpow2, weightings)[WINDOW-1:-(WINDOW-1)]
diffavg2 = [sigavg2[i] - bgavg2[i] for i in range(len(sigavg2))]
sigavg = np.convolve(sigpow, weightings)[WINDOW-1:-(WINDOW-1)]
bgavg = np.convolve(bgpow, weightings)[WINDOW-1:-(WINDOW-1)]
diffavg = [sigavg[i] - bgavg[i] for i in range(len(sigavg))]
d = {'sig':sigavg, 'bg':bgavg, 'diff*5':diffavg}
#f = open('/data/dpph/runs/' + fname + '.dat','a')
#f.write(d)
#f.close()
b = [a / 28042.9 for a in freq[2:-2]]
diff = plt.plot(b, [5*a for a in diffavg], label='difference*5')
sig = plt.plot(b, sigavg, label='signal')
bg = plt.plot(b, bgavg, label='background')
plt.legend()
plt.xlabel('Magnetic Field (T)')
plt.ylabel('Power (mW)')
plt.title('DPPH Resonance Signal')
field = freq[diffavg.index(min(diffavg))] / 28042.9
zscore = (min(diffavg)-np.mean(diffavg))/np.std(diffavg)
pvalue = special.ndtr(zscore)
if pvalue < conflevel:
    rval = {
        "field":round(field,4),
        "error":0.0003,
        "accuracy":"accurate"
        }
    print rval

if pvalue >= conflevel:
    rval = {
        "field":round(field,4),
        "error":0.0003,
        "accuracy":"inaccurate"
        }
    print rval


#plt.savefig('/data/dpph/images/' + fname + '.jpg')
plt.show()
