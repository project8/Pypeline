from Pypeline import DripInterface
import numpy as np
import matplotlib.pyplot as plt
import math
import sys

drip = DripInterface('http://p8portal.phys.washington.edu:5984')

#Hall Probe Calibration Data
conv = 125 #T/V

#Estimate field with Hall Probe
guess = round(abs(float(repr(drip.Get('hall_probe_voltage'))[1:16]))*conv,2)
print "Hall Probe Estimated Field: " + str(guess) + " T"

#Find precise field with DPPH
DPPH = 28042.9 #MHz/T
target = int(round(guess*DPPH))
if target < 24500:
    sys.exit("Field strength too low")

drip.Set('pancake_coil_current','enable')
drip.Set('pancake_coil_current','0A')
drip.Set('hf_sweep_start', target-50)
drip.Set('hf_sweep_stop', target+50)
drip.Set('lo_cw_freq', target-24550)
drip.Set('hf_sweep_time', 10)
run1 = eval(repr(drip.Run(subprocess = "sweepline"))[1:-1])
power1 = run1['data']
freq1 = np.linspace(0,run1['sampling_rate']/2,len(power1))

drip.Set('pancake_coil_current','1.03A')

run2 = eval(repr(drip.Run(subprocess = "sweepline"))[1:-1])
power2 = run2['data']
freq2 = np.linspace(0,run2['sampling_rate']/2,len(power2))
power = [power1[i] - power2[i] for i in range(len(power1))]
freq = freq1
drip.Set('pancake_coil_current','0A')
plt.plot(freq[20:180],[5*a for a in power[20:180]])
plt.plot(freq[20:180],power1[20:180])
plt.plot(freq[20:180],power2[20:180])
plt.show()
