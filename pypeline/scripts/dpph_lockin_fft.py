# built in
from time import sleep
from sys import stdout
import math
# 3rd party
from numpy import std, mean, array, less, arange, pi, where, diff
from numpy import sign, sin, polyfit, sqrt, multiply,concatenate
from scipy import optimize, fftpack
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
        drip_resp = interface.Get('dpph_magphase').Wait()
        sleep(slptime)
        magphase = [float(val) for val in drip_resp['final'].split(',')]
        return magphase[0] * sign(sin(magphase[1] * pi / 180))
    except KeyError as keyname:
        if keyname[0] == 'result':
            print('\n\n' + '*' * 60 + 'No response from sweeper' + '\n\n')
            raise
        elif keyname[0] == 'final':
            print('\n\n' + '*' * 60 + 'No response from lock-in' + '\n\n')
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
        <stop_volts>:   absolute voltage to stop looping
    '''
    pype.Set('hf_sweeper_power', power).Wait()
    if not float(pype.Get('hf_sweeper_power').Wait()['final']):
        raise AssertionError('power setting not stable')
    VDC = []
    for count, freq in enumerate(freq_list):
        VDC.append(GetLockinValue(pype, freq))
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


def dpph_lockin_fft(pype, guess=25001, stop_nsigma=30, stop_voltage=9e-7):
    '''
        Do a dpph scan using DripInterface instance <pype>

        Inputs:
            <guess> is an intial guess for the starting frequency
    '''
    result = {}
    fitline = False
    dataset = sorted(zip([0], [0]))
    num_stats_freqs = 10

    #init_step = 2
    init_step = 4
    guess=25520
    center=25520
    halfspan=50
    freqs = range(int(guess)-halfspan, int(guess)+halfspan, init_step)
    #freqs.sort(key=lambda value: abs(value - guess))

    #-- build up what I'm looking for --
    target_signal=[]
    #width of signal in MHz
    #determined empiricaly by looking at filter shape
    #expected_width=2.5
    expected_width=3
    for f in freqs:
        x=(float(f)-float(center))/float(expected_width)
        gderiv=x*math.exp(-x*x/2.0)
        target_signal.append(0.00001*gderiv)
    dataset_target=sorted(zip(freqs,target_signal))
    #----------------------------------

    #-- Take a scan over frequencies --
    print('Taking Coarse Scan')
    VDC = GetVoltages(pype, freqs)
    #VDC = [0] * len(freqs)
    #----------------------------------
    
    #--- apply the filter ---
    target_signal_fft=fftpack.fft(target_signal)
    counter_time=range(0,len(freqs))
    #apply the filter
    coarse_data_fft=fftpack.fft(VDC)
    #remove offset
    coarse_data_fft[0]=0
    #----------------------------------

    #--- apply filter to data ---
    #numpy is a terrible name. it's like the worst
    #nickname for someone in middle school
    filtered_fft=multiply(coarse_data_fft,target_signal_fft)
    filtered=fftpack.ifft(filtered_fft)
    print("filtered length "+str(len(filtered)))
    #this is awkward, because I have to adjust to the fact that my
    #filter has its zero crossing in the middle
    firsthalf=range( center,center+halfspan,init_step)
    secondhalf=range(center-halfspan,center,init_step)
    adjusted_freqs = concatenate([firsthalf,secondhalf] )
    filtered_toplot=sorted(zip(adjusted_freqs,abs(filtered)))
    #----------------------------------

    #Only plotting beyond this point

    #-- Plot the raw data and filter, for funsies
    dataset_coarse = sorted(zip(freqs, VDC))
    toplot_fdomain_raw=[dataset_coarse,dataset_target]
    plot1 = Gnuplot()
    plot1.gp("set style line 1 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 2")
    plot1.gp("set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2")
    plot1.gp("set style line 11 lc rgb '#808080' lt 1")
    plot1.gp("set border 3 back ls 11")
    plot1.gp("set tics nomirror")
    plot1.gp("set style line 12 lc rgb '#808080' lt 0 lw 1")
    plot1.gp("set grid back ls 12")
    plot1.gp("set xlabel \"Sweeper Frequency [MHz]\"")
    plot1.gp("set ylabel \"Lockin Output [V]\"")
    plot1.gp("set title \"Raw Frequency Domain Data and Filter\"")
    plot1.plotMany(toplot_fdomain_raw, ['with lines title "data"','with lines title "filter"'])
    #----------------------------------


    
    #--- plot the frequency domain, again for funsies
    print("frequency length "+str(len(freqs)))
    print("fft length "+str(len(target_signal_fft)))
    real_target_signal_fft=abs(target_signal_fft)
    real_coarse_data_fft=abs(coarse_data_fft)
    dataset_target_fft=sorted(zip(counter_time,real_target_signal_fft))
    dataset_coarse_fft=sorted(zip(counter_time,real_coarse_data_fft))
    toplot_tdomain_raw=[dataset_coarse_fft,dataset_target_fft]
    plot2 = Gnuplot()
    plot2.gp("set style line 1 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 2")
    plot2.gp("set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2")
    plot2.gp("set style line 11 lc rgb '#808080' lt 1")
    plot2.gp("set border 3 back ls 11")
    plot2.gp("set tics nomirror")
    plot2.gp("set style line 12 lc rgb '#808080' lt 0 lw 1")
    plot2.gp("set grid back ls 12")
    plot2.gp("set xlabel \"something\"")
    plot2.gp("set ylabel \"fft of Lockin Output [V]\"")
    plot2.gp("set title \"Time Domain Data and Filter\"")
    plot2.plotMany(toplot_tdomain_raw, ['with lines title "data fft"','with lines title "filter fft"'])
    #----------------------------------

    
    #--- plot filter result ---
    plot3 = Gnuplot()
    plot3.gp("set style line 1 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 2")
    plot3.gp("set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2")
    plot3.gp("set style line 11 lc rgb '#808080' lt 1")
    plot3.gp("set border 3 back ls 11")
    plot3.gp("set tics nomirror")
    plot3.gp("set style line 12 lc rgb '#808080' lt 0 lw 1")
    plot3.gp("set grid back ls 12")
    plot3.gp("set xlabel \"Sweeper Frequency [MHz]\"")
    plot3.gp("set ylabel \"Magnitude\"")
    plot3.gp("unset key")
    plot3.gp("set title \"Filter Result, Freq Domain \"")
    plot3.plot1d(filtered_toplot, 'with lines')
    #----------------------------------

    #No more beyond this point





    #---- This is all leftover from other method
    #---- But I'm keeping it around for reference, commented out
    #VDC_freqs = freqs[:len(VDC)]
    #if not len(VDC) == len(freqs):
    #    interesting_freq = VDC_freqs[-1]
    #dataset = sorted(zip(VDC_freqs, VDC))
    commenstring="""

    # take a set of fine data points to capture the structure
    try:
        assert interesting_freq, 'interesting_freq'
        fine_freqs = range(interesting_freq - 25, interesting_freq + 20, 2)
        print('coarse scan of structure')
        VDC_fine = GetVoltages(pype, fine_freqs)
        dataset = sorted(zip(fine_freqs, VDC_fine))
        # find zero crossing
        min_index = VDC_fine.index(min(VDC_fine))
        max_index = VDC_fine.index(max(VDC_fine))
        found_crossing = True
        try:
            crossing = min(min_index, max_index) + where(
                diff(sign(VDC_fine[min(min_index, max_index):
                                   max(min_index, max_index) + 1])))[0][-1]
        except IndexError:
            found_crossing = False
        if found_crossing:
            est = fine_freqs[crossing] - VDC_fine[crossing] * (
                (fine_freqs[crossing + 1] - fine_freqs[crossing])
                / (VDC_fine[crossing + 1] - VDC_fine[crossing]))

            # take some very finely spaced data for doing a fit
            very_fine_freqs = arange(est - 1, est + 1, 0.1)
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
            result['uncal'] = fit[0][0]
            result['uncal_err'] = result['uncal'] * (0.0002 / 2.0036)
            result['uncal_units'] = 'MHz'
            result['uncal_val'] = (str(result['uncal']) + ' +/- ' +
                                   str(result['uncal_err']) + ' ' +
                                   str(result['uncal_units']))
            slope = fit[0][1]
            cov = fit[1]
            fitline = [very_fine_freqs[0],
                       slope * (very_fine_freqs[0] - result['uncal']),
                       very_fine_freqs[-1],
                       slope * (very_fine_freqs[-1] - result['uncal'])]

            print('Found zero crossing at ' + str(result['uncal']) + ' +/- ' +
                  str(result['uncal_err']) + ' MHz')
            geff = 2.0036
            chargemass = 1.758e11
            freq_to_field = 4 * pi * 10 ** 7 / (geff * chargemass)
            result['cal'] = freq_to_field * result['uncal']
            result['cal_err'] = freq_to_field * result['uncal_err']
            result['cal_units'] = 'kG'
            result['cal_val'] = (str(result['cal']) + ' +/- ' +
                                 str(result['cal_err']) + ' ' +
                                 str(result['cal_units']))
            print('Field is: ' + str(result['cal']) + ' +/- ' +
                  str(result['cal_err']) + str(result['cal_units']))
        else:
            print('crossing not found, displaying ROI')

    except AssertionError as e:
        if e[0] == 'interesting_freq':
            print('\n' + '*' * 60 + '\nNo interesting frequencies found\n' +
                  '*' * 60 + '\n')
        if e[0] == 'zero_crossing':
            print('\n' + '*' * 60 + '\nNo zero question\n' + '*' * 60 + '\n')
    except IndexError as e:
        if e[0] == -1:
            print('\n' + '*' * 60 + '\nNo zero question\n' + '*' * 60 + '\n')
    except:
        print('\n' + '*' * 60 + '\nSome other error\n' + '*' * 60 + '\n')
        raise
    """

    return result, zip(*dataset)
