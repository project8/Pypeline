from __future__ import print_function
from __future__ import absolute_import
# built in
from time import sleep
from sys import stdout
from datetime import datetime
# 3rd party
from numpy import sign, sin, pi, sqrt, exp, multiply, mean, concatenate
from scipy import fftpack
# local
from ...PypelineErrors import NoResponseError, DriplineError


def _GetLockinValue(interface, freq=25553.440, slptime=2):
    '''
        Make a reading with the lockin amplifier at a specific frequency.

        Inputs:
            <interface> a DripInterface instance
            <freq>      the frequency in MHz
            <slptime>   time to sleep before reading the lockin (in seconds)

        Output:
            <reading>   the DVM reading in Volts DC from the lockin
    '''
    try:
        interface.Set('hf_cw_freq', freq).Wait()['result'] == 'ok'
        drip_resp = interface.Get('dpph_magphase').Wait()
        sleep(slptime)
        magphase = [float(val) for val in drip_resp['final'].split(',')]
        return magphase[0] * sign(sin(magphase[1] * pi / 180))
    except KeyError as keyname:
        if keyname[0] == 'result':
            raise NoReponseError('Sweeper did not respond')
        elif keyname[0] == 'final':
            raise NoResponseError('No response from lock-in')
        else:
            raise


def _GetVoltages(pype, freq_list, power=-75, reference=0, deviation=0.2,
                 stop_sigma=1e10, stop_volts=20):
    '''
        Get a list for frequency <-> lockin voltage pairs with updates

        <pype>:         pypeline DripInterface instance
        <freq_list>:    an iterable of frequencies in MHz
        <reference>:    if stopping at structure, this is the reference voltage
        <deviation>:    if stopping at structure, count number of these away
        <stop_sigma>:   number of <deviation> from <reference> to stop looping
        <stop_volts>:   absolute voltage to stop looping
    '''
    pype.Set('hf_sweeper_power', power).Wait()
    if not float(pype.Get('hf_sweeper_power').Wait()['final']):
        raise AssertionError('power setting not stable')
    VDC = []
    for count, freq in enumerate(freq_list):
        VDC.append(_GetLockinValue(pype, freq))
        stdout.write('{:.2E} MHz -> {:.2E} VDC ({:.1%})\r'.format(freq,
                     VDC[-1], float(count) / len(freq_list)))
        stdout.flush()
        if ((abs((VDC[-1] - reference) / deviation) > stop_sigma) or
           (abs(VDC[-1]) > stop_volts)):
                print('something of interest (' + str(VDC[-1]) + ' V) at '
                      + str(freq) + ' MHz')
                break
    stdout.write(' ' * 60 + '\r')
    stdout.flush()
    return VDC


def _GetSweptVoltages(pype, start_freq, stop_freq, sweep_time=60, power=-75, num_points=360):
    '''
        Use the lockin's built in ADC to link it to the sweeper and take data
        <pype> an DripInterface instance
        <start_freq> lower frequency bound for the sweep (corresponds to 0 V on the ADC)
        <stop_freq> upper frequency bound for the sweep (corresponds to 10 V on the ADC)
        <sweep_time> time, in seconds, to do a sweep
        <power> output power, in dBm, from the sweeper
        <num_points> number of samplings for the lockin to take
    '''
    print('*' * 60, '\nsetting sweeper', datetime.now())
    sets = []
    sets.append(pype.Set('hf_sweep_start', start_freq))
    sets.append(pype.Set('hf_sweep_stop', stop_freq))
    sets.append(pype.Set('hf_sweep_time', sweep_time * 1000))
    if power:
        sets.append(pype.Set('hf_sweeper_power', power))
    for i in range(100):
        if not sum([set.Waiting() for set in sets]):
            break
        sleep(1)
    if sum([set.Waiting() for set in sets]):
        for set in sets:
            print(set)
        raise DriplineError('Sweeper sets failed or not yet complete')
    print('*' * 60, '\nsweeper complete, setting lockin', datetime.now())
    sample_length = num_points
    sample_period = int(((sweep_time + 5) / num_points) * 1000)
    pype.Set('lockin_raw_write', "NC").Wait()
    pype.Set('lockin_raw_write', "CBD 51").Wait()
    #len is number of samples to take, period is how often
    pype.Set('lockin_raw_write', "LEN " + str(int(sample_length))).Wait()
    pype.Set('lockin_raw_write', "STR " + str(int(sample_period))).Wait()
    print('*' * 60, '\ntaking data', datetime.now())
    pype.Set('lockin_raw_write', "TD").Wait()
    sleep(sweep_time + 30)
#    maxsleep = 100
#    sleep(10)
#    for i in range(maxsleep):
#        sleep(1)
#        statusfull = pype.Get('lockin_data_status').Wait()['final']
#        if statusfull[0] == '0':
#            break
    print('*' * 60, '\nretrieving data', datetime.now())
    adc_curve = pype.Get('lockin_adc1_curve').Wait()['final']
    x_curve = pype.Get('lockin_x_curve').Wait()['final']
    y_curve = pype.Get('lockin_y_curve').Wait()['final']
    print('*' * 60, '\ncomputing final form and return', datetime.now())
    amplitude_curve = [sqrt(xi**2 + yi**2) for xi, yi in zip(x_curve, y_curve)]
    slope = (stop_freq - start_freq) / 10000.
    frequency_curve = [start_freq+ slope * adc for adc in adc_curve]
    all_curves = list(zip(frequency_curve, x_curve, y_curve, amplitude_curve, adc_curve))
    filtered_data = [pt for pt in all_curves[5:-3] if (pt[-1] > 0.1 and pt[-1] < 10000.)]
    frequency_curve, x_curve, y_curve, amplitude_curve, adc_curve = zip(*sorted(filtered_data))
    print('*' * 60, '\ndone')
    print('*' * 60)
    return {'adc_curve': adc_curve,
            'frequency_curve': frequency_curve,
            'x_curve': x_curve,
            'y_curve': y_curve,
            'amplitude_curve': amplitude_curve}


def _FindFieldFFT(min_freq, max_freq, freq_data, volts_data):
    '''
    '''
    #cut down to a window
    all_data = zip(freq_data, volts_data)
    cut_data = [point for point in all_data if (min_freq < point[0] and point[0] < max_freq)]
    frequencies, voltages = zip(*cut_data)
    #build target
    target_signal = []
    expected_width = 3
    for f in frequencies:
        x = (f - mean([min_freq, max_freq])) / expected_width
        gderiv = x * exp(-x * x / 2.)
        target_signal.append(0.00001 * gderiv)
    target_fft = fftpack.fft(target_signal)
    data_fft = fftpack.fft(voltages)
    data_fft[0] = 0
    #apply filter
    filtered_fft = multiply(data_fft, target_fft)
    filtered = fftpack.ifft(filtered_fft)
    idx = int(len(filtered)/2)
    return {'freqs': frequencies,
            'result': abs(concatenate([filtered[idx:], filtered[0:idx]]))}
