#!/usr/bin/python

from __future__ import print_function, absolute_import
from sys import argv
from time import sleep

from numpy import array, pi
from datetime import datetime

import pypeline

def dpph_logger(pype_url='http://localhost:5984'):
    '''
    '''
    pype = pypeline.DripInterface(pype_url)
    sweep = pypeline.dpph.dpph_utils._GetSweptVoltages(pype, 26000., 26500, 32., False, 400)
    freqdata = array(sweep['frequency_curve'])
    magdata = sweep['amplitude_curve']
    fit = pypeline.dpph.dpph_utils._FindFieldFFT(26000, 26500, freqdata, magdata, width=4)
    #print(fit.keys())
    res_freq = max(zip(fit['result'], fit['freqs']))[1]
    res_freq_unct = fit['freqs'][1] - fit['freqs'][0]
    geff = 2.0036
    chargemass = 1.758e11
    freq_to_field = 4 * pi * 10**7 / (geff * chargemass)
    res_field = freq_to_field * res_freq
    res_field_unct = freq_to_field * res_freq_unct
    print('found resonance at:', res_freq, 'MHz')
    print('or in field:', res_field, 'kG')
    result = {
                'uncal_val': ' '.join([str(res_freq), '+/-', str(res_freq_unct)]),
                'cal_val': ' '.join([str(res_field), '+/-', str(res_field_unct)]),
                'timestamp': datetime.utcnow()
             }
    pype.LogValue(sensor='dpph_field', **result)
    print('field logged at', datetime.now(), '(system time)')

def start_loop(addr):
    '''
    '''
    while True:
        try:
            dpph_logger(addr)
        except:
            print("*"*60,'\n','there was a problem\n','*'*60)
        sleep(60)

if __name__ == '__main__':
    if len(argv) == 1:
        start_loop('http://localhost:5984')
    elif len(argv) == 2:
        start_loop(argv[1])
    else:
        print('too many arguments received')
