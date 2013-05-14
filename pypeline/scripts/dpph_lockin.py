# built in
from time import sleep
from sys import stdout
# 3rd party
from numpy import std, mean, array, less, arange, pi, where, diff
from numpy import sign, sin, polyfit, sqrt
from scipy import optimize
# local
from ..DripInterface import DripInterface
from ..usegnuplot import Gnuplot


def GetLockinValue(interface, freq=25553.440, slptime=2):
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
        sleep(slptime)
        drip_resp = interface.Get('dpph_magphase').Wait()
        magphase = [float(val) for val in drip_resp['final'].split(',')]
        return magphase[0]*sign(sin(magphase[1]*pi/180))
    except KeyError as keyname:
        if keyname[0] == 'result':
            print('\n\n' + '*'*60 + 'No response from sweeper' +'\n\n')
            raise
        elif keyname[0] == 'final':
            print('\n\n' + '*'*60 + 'No response from lock-in' +'\n\n')
            raise
        else:
            raise


def GetVoltages(pype, freq_list, power=-75, reference=0, deviation=0.2,
                stop_sigma=1e10, stop_volts=20):
    '''
        Get a list for frequency <-> lockin voltage pairs with updates

        <pype>:         pypeline DripInterface instance
        <freq_list>:    an iterable of frequencies in MHz
        <reference>:    if stopping at structure, this is the reference voltage
        <deviation>:    if stopping at structure, count number of these away
        <stop_sigma>:   number of <deviation> from <reference> to stop looping
    '''
    pype.Set('hf_sweeper_power', power).Wait()
    if not float(pype.Get('hf_sweeper_power').Wait()['final']):
        raise AssertionError('power setting not stable')
    VDC = []
    for count,freq in enumerate(freq_list):
        VDC.append(GetLockinValue(pype, freq))
        stdout.write('{:.2E} MHz -> {:.2E} VDC ({:.1%})\r'.format(freq,
                     VDC[-1], float(count)/len(freq_list)))
        stdout.flush()
        if ((abs((VDC[-1]-reference)/deviation) > stop_sigma) or
           (abs(VDC[-1]) > stop_volts)):
                print('something of interest (' + str(VDC[-1]) + ' V) at '
                      + str(freq) + ' MHz')
                break
    stdout.write(' '*60 + '\r')
    stdout.flush()
    return VDC


def dpph_lockin(pype, guess=25000):
    '''
        Do a dpph scan using DripInterface instance <pype>

        Inputs:
            <guess> is an intial guess for the starting frequency
    '''
    fitline = False
    dataset = sorted(zip([0],[0]))
    num_stats_freqs = 10

    init_step = 2
    if guess == 25000:
        init_step = 5
    freqs = range(25000, 26500, init_step)
    freqs.sort(key=lambda value: abs(value-guess))

    #determine a mean and standard deviation
    print('determine mean and standard deviation')
    VDC = GetVoltages(pype, freqs[-num_stats_freqs:])
    VDC_freqs = freqs[-num_stats_freqs:]
    VDC_std = std(VDC)
    VDC_mean = mean(VDC)
    print('mean is: ' + str(VDC_mean) + ' VDC')
    print('std is: ' + str(VDC_std) + ' VDC')

    #find where the structure starts
    interesting_freq = False
    print('look for structure')
    VDC = GetVoltages(pype, freqs, reference=VDC_mean, deviation=VDC_std,
                      stop_sigma=30, stop_volts=9e-7)
    VDC_freqs = freqs[:len(VDC)]
    if not len(VDC) == len(freqs):
        interesting_freq = VDC_freqs[-1]
    dataset = sorted(zip(VDC_freqs, VDC))
    #else:
    #    for pair in zip(freqs, VDC):
    #        print(pair)

    #take a set of fine data points to capture the structure
    try:
        assert interesting_freq, 'interesting_freq'
        fine_freqs = range(interesting_freq-25, interesting_freq+20, 2)
        print('coarse scan of structure')
        VDC_fine = GetVoltages(pype, fine_freqs)
        dataset = sorted(zip(fine_freqs, VDC_fine))
        #find zero crossing
        min_index = VDC_fine.index(min(VDC_fine))
        max_index = VDC_fine.index(max(VDC_fine))
        found_crossing = True
        try:
            crossing = min(min_index, max_index) + where(
                diff(sign(VDC_fine[min(min_index, max_index):
                                   max(min_index, max_index)+1])))[0][-1]
        except IndexError:
            found_crossing = False
        if found_crossing:
            est = fine_freqs[crossing] - VDC_fine[crossing] * (
                (fine_freqs[crossing+1] - fine_freqs[crossing])
                / (VDC_fine[crossing+1] - VDC_fine[crossing]))
    
            #take some very finely spaced data for doing a fit
            very_fine_freqs = arange(est-1, est+1, 0.1)
            print('fine scan of zero crossing')
            VDC_very_fine = GetVoltages(pype, very_fine_freqs)
            dataset = sorted(dataset + zip(very_fine_freqs, VDC_very_fine))
    
            fitfunc = lambda p, x: p[1] * (x - p[0])
            errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err
            p_in = [25000.0, -1.0]
            fit = optimize.leastsq(errfunc, p_in, full_output=1,
                                   args=(array(very_fine_freqs),
                                         array(VDC_very_fine),
                                         array([1e-5] * len(very_fine_freqs))))
            resonance = fit[0][0]
            slope = fit[0][1]
            cov = fit[1]
            resonance_err = (0.0002/2.0036)*resonance
            fitline = [very_fine_freqs[0],
                       slope * (very_fine_freqs[0]-resonance),
                       very_fine_freqs[-1],
                       slope * (very_fine_freqs[-1]-resonance)]

            print('Found zero crossing at ' + str(resonance) + ' +/- ' +
                  str(resonance_err) + ' MHz')
            geff = 2.0036
            chargemass = 1.758e11
            freq_to_field = 4*pi*10**7/(geff*chargemass)
            print('Field is: ' + str(freq_to_field*resonance) + ' +/- ' +
                  str(freq_to_field*resonance_err) + ' kGauss')
        else:
            print('crossing not found, displaying ROI')

    except AssertionError as e:
        if e[0] == 'interesting_freq':
            print('\n' + '*'*60 + '\nNo interesting frequencies found\n' +
                  '*'*60 + '\n')
        if e[0] == 'zero_crossing':
            print('\n' + '*'*60 + '\nNo zero question\n' + '*'*60 + '\n')
    except IndexError as e:
        if e[0] == -1:
            print('\n' + '*'*60 + '\nNo zero question\n' + '*'*60 + '\n')
    except:
        print('\n' + '*'*60 + '\nSome other error\n' + '*'*60 + '\n')
        raise
    
    plot = Gnuplot()
    plot.gp("set style line 1 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 2")
    plot.gp("set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2")
    plot.gp("set style line 11 lc rgb '#808080' lt 1")
    plot.gp("set border 3 back ls 11")
    plot.gp("set tics nomirror")
    plot.gp("set style line 12 lc rgb '#808080' lt 0 lw 1")
    plot.gp("set grid back ls 12")
    plot.gp("set xlabel \"Sweeper Frequency [MHz]\"")
    plot.gp("set ylabel \"Lockin Output [V]\"")
    plot.gp("unset key")
    if fitline:
        plot.g.stdin.write('set arrow from ' + str(fitline[0]) + ',' +
                           str(fitline[1]) + ' to ' + str(fitline[2]) + ',' +
                           str(fitline[3]) + 'nohead\n')
    plot.plot1d(dataset, '')
    return zip(*dataset)
