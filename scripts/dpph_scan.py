#system
import sys
import math
from uuid import uuid4
from datetime import datetime
#3rd party
import numpy as np
import matplotlib.pyplot as plt
from scipy import special
#custom
from pypeline import DripInterface

drip = DripInterface('http://p8portal.phys.washington.edu:5984')
tempf = '/data/' + uuid4().hex + '.egg'
fname = str(datetime.today().year) + str(datetime.today().month) + str(datetime.today().day) + str(datetime.today().hour) + str(datetime.today().minute) + str(datetime.today().second)
conflevel = .005

#Calibration Data
hallconst = 118 #T/V
coilconst = .35 #T/A
coiloffset = .084 #T

#Estimate field with Hall Probe
hguess = round(abs(float(drip.Get('hall_probe_voltage').Wait()['final'][1:16]))*hallconst,3)
print "Hall Probe Estimated Field: " + str(hguess) + " T"

#Estimate field with coil constant
cguess = round(float(raw_input("Enter magnet current in Amps: "))*coilconst + coiloffset,3)
print "Coil constant estimated field: " + str(cguess) + " T"

#Check for reasonable agreement
#if int(1000*abs(hguess-cguess)) > 10:
#    sys.exit('Hall Probe and coil constant do not agree. Try again or check calibration.')

guess = round((hguess+cguess)/2,4)

#Find precise field with DPPH
DPPH = 28042.9 #MHz/T
Li = 27992.5*2.0004/2 #MHz/T

target = int(round(guess*DPPH))
if target < 24590:
    sys.exit("Field strength too low, (must be at least .877 T)")

sigpow = []
bgpow = []
freq = []
scanwin = 80 #MHz
runlim = int(round(abs(hguess-cguess)*DPPH/scanwin)) + 3
scantime = 2000 #ms
runnum = 0
dummy = list(np.linspace(0,250,513))
for i in dummy:
    if i > (100-scanwin)/2:
        lb = dummy.index(i)
        break
    
for i in reversed(dummy):
    if i < (100+scanwin)/2:
        ub = dummy.index(i)
        break
    
drip.Set('pancake_coil_current','enable')
drip.Set('hf_sweeper_power','-40')
while runnum < runlim:
    drip.Set('pancake_coil_current','0A')
    drip.Set('hf_sweep_start', target-(scanwin*(runlim-1)+100)/2+scanwin*runnum)
    drip.Set('hf_sweep_stop', target-(scanwin*(runlim-1)+100)/2+scanwin*runnum+100)
    drip.Set('hf_sweep_time', 10)
    drip.Set('lo_cw_freq', target-24500-(scanwin*(runlim-1)+100)/2+scanwin*runnum)
    sigrun = eval(repr(drip.CreatePowerSpectrum(drip.Run(filename = tempf, duration = scantime),sp="sweepline"))[1:-1])
    sigtp = sigrun['data']
    tf = list(np.linspace(target-(scanwin*(runlim-1)+100)/2+scanwin*runnum,sigrun['sampling_rate']/2+target-(scanwin*(runlim-1)+100)/2+scanwin*runnum,len(sigtp)))
    sigpow = sigpow + sigtp[lb:ub]
    freq = freq + tf[lb:ub]
    drip.Set('pancake_coil_current','4A')
    bgrun = eval(repr(drip.CreatePowerSpectrum(drip.Run(filename = tempf, duration = scantime)),sp="sweepline")[1:-1])
    bgtp = bgrun['data']
    bgpow = bgpow + bgtp[lb:ub]
    runnum = runnum + 1

drip.Set('pancake_coil_current','0A')
WINDOW = 5
weightings = np.repeat(1.0, WINDOW) / WINDOW
sigavg = np.convolve(sigpow, weightings)[WINDOW-1:-(WINDOW-1)]
bgavg = np.convolve(bgpow, weightings)[WINDOW-1:-(WINDOW-1)]
diffavg = [sigavg[i] - bgavg[i] for i in range(len(sigavg))]
b = [a / 28042.9 for a in freq[2:-2]]
plt.plot(b, [5*a for a in diffavg], label='difference*5')
plt.plot(b, sigavg, label='signal')
plt.plot(b, bgavg, label='background')
plt.legend(loc='best')
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
        "pvalue":pvalue
        }
    print rval

if pvalue >= conflevel:
    rval = {
        "field":round(field,4),
        "error":0.0003,
        "pvalue":pvalue
        }
    print rval

plt.savefig('/Users/Micah/project8/pypeline/scripts/dpph_images/' + fname + '.jpg')
plt.show()
