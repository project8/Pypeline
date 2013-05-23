# system
import sys
import math
import time
from datetime import datetime
from uuid import uuid4
# 3rd party
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
# custom
from pypeline import DripInterface, peakdet

drip = DripInterface('http://p8portal.phys.washington.edu:5984')

if len(sys.argv) != 3:
    sys.exit(
        "Please enter hf_cw_freq and lo_cw_freq in MHz as arguments when running this script.")
fname = str(datetime.today().year) + str(datetime.today().month) + str(datetime.today().day) + str(
    datetime.today().hour) + str(datetime.today().minute) + str(datetime.today().second)
powx = []
powy = []
hf = sys.argv[1]
lo = sys.argv[2]
drip.Set('hf_cw_freq', hf)
drip.Set('lo_cw_freq', lo)
tempf = '/data/' + uuid4().hex + '.egg'
for i in range(-100, 0, 5):
    drip.Set('hf_sweeper_power', i)
    run = eval(repr(drip.Run(filename=tempf))[1:-1])
    power = run['data']
    freq = np.linspace(0, run['sampling_rate'] / 2, len(power))
    power = power[1:-1]
    freq = freq[1:-1]
    logpower = [10 * math.log(a, 10) for a in power]
    peaks = peakdet(logpower, 2, freq)
    for k in peaks[0]:
        if round(k[0]) == 50:
            powx.append(i)
            powy.append(k[1])

plt.plot(powx, powy)
plt.xlabel('Input Power (dBm)')
plt.ylabel('Output Power (dBm)')
plt.title('Compression at LO = ' + lo + ', and HF = ' + hf)
plt.savefig(
    '/Users/Micah/project8/pypeline/scripts/compression_images/' + fname + '.jpg')
plt.show()
