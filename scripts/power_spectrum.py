#standard libs
import sys
from uuid import uuid4
from math import log
#3rd party
import numpy as np
import matplotlib.pyplot as plt
#custom
from pypeline import DripInterface, peakdet

def power_spectrum(d='250', r='500', f='/data/' + uuid4().hex + '.egg', c='1', subprocess='powerline', args=False):
    '''
    power_spectrum is a function to take a digitization run and plot it. Should
    be called as a script, or be executed by other scripts.

        Arguments:
        -h  -> Print this help message
        -d  -> Enter duration of digitization run in milliseconds
        -r  -> Enter rate of digitization in MHz, up to 1500 MHz
        -f  -> Enter *.egg filename to save digitization data in Ignatius
               /data/ folder
        -c  -> Enter channel number
        -lo -> Enter local oscillator frequency in MHz
        -sp -> Enter subprocess for processing raw data files (powerline or
               sweepline)
    '''
    drip = DripInterface('http://p8portal.phys.washington.edu:5984')
    lo = False
    if '-h' in args:
        print(power_spectrum.__doc__)
        sys.exit()
    if '-d' in args:
        d = args[args.index('-d') + 1]
    if '-r' in args:
        r = args[args.index('-r') + 1]
    if '-f' in args:
        f = '/data/' + args[args.index('-f') + 1]
    if '-c' in args:
        c = args[args.index('-c') + 1]
    if '-lo' in args:
        lo = args[args.index('-lo') + 1]
    if '-sp' in args:
        subprocess = args[args.index('-sp') + 1]
    if lo:
        drip.Set('lo_cw_freq',lo)

    run = eval(drip.CreatePowerSpectrum(drip.Run(rate=r,duration=d,filename=f).Wait(),sp=subprocess).Wait()['result'])
    
    y = run['data']
    x = np.linspace(0,run['sampling_rate']/2,len(y))
    y = y[1:-1]
    x = x[1:-1]
    dbm = [10*log(a,10) for a in y]
    if subprocess == 'sweepline':
        for i in range(len(x)):
            if x[i] > 90:
                stop = i
                break
        for i in range(len(x)):
            if x[i] > 10:
                start = i
                break
        dbm = dbm[start:stop]
        x = x[start:stop]
    plt.plot(x,dbm)
    plt.title("Power Spectrum (Sampling Rate = " + r + " MHz, Duration = " + d + " ms)")
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("Power (dBm)")
    plt.show()

if __name__ == '__main__':
    power_spectrum(args=sys.argv) 
