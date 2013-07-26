from __future__ import print_function
from __future__ import absolute_import
# built in
from time import sleep
from sys import stdout
from datetime import datetime
# 3rd party
from numpy import sign, sin, pi, sqrt
# local
from ...PypelineErrors import NoResponseError


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
    sets.append(pype.Set('hf_sweep_time', sweep_time))
    sets.append(pype.Set('hf_sweeper_power', power))
    for i in range(100):
        if not sum([set.Waiting() for set in sets]):
            break
    if sum([set.Waiting() for set in sets]):
        print('sweeper sets failed')
    print('*' * 60, '\nsweeper complete, setting lockin', datetime.now())
    sample_length = num_points
    sample_period = int((sweep_time / num_points) * 1000)
    pype.Set('lockin_raw_write', "NC").Wait()
    pype.Set('lockin_raw_write', "CBD 51").Wait()
    #len is number of samples to take, period is how often
    pype.Set('lockin_raw_write', "LEN " + str(int(sample_length))).Wait()
    pype.Set('lockin_raw_write', "STR " + str(int(sample_period))).Wait()
    print('*' * 60, '\ntaking data', datetime.now())
    pype.Set('lockin_raw_write', "TD").Wait()
    sleep(sweep_time + 30)
    print('*' * 60, '\nretrieving data', datetime.now())
    adc_curve = pype.Get('lockin_adc1_curve').Wait()['final']
    x_curve = pype.Get('lockin_x_curve').Wait()['final']
    y_curve = pype.Get('lockin_y_curve').Wait()['final']
    print('*' * 60, '\ncomputing final form and return', datetime.now())
    amplitude_curve = [sqrt(xi**2 + yi**2) for xi, yi in zip(x_curve, y_curve)]
    slope = (stop_freq - start_freq) / 10000.
    frequency_curve = [start_freq+ slope * adc for adc in adc_curve]
    return (frequency_curve, amplitude_curve)
