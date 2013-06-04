from __future__ import print_function, absolute_import
# built in
from math import exp, floor, ceil
# 3rd party
from numpy import multiply, concatenate, pi
from scipy import fftpack
# local
from ...usegnuplot import Gnuplot
from .dpph_utils import _GetVoltages


def fft_filter(pype, guess=25001, power=-75, span=100, step=4):
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
    init_step = int(step)
    #guess=25950
    center = guess
    halfspan = int(span/2)
    freqs = range(int(guess)-halfspan, int(guess)+halfspan, init_step)
    nfreqs = len(freqs)
    #freqs.sort(key=lambda value: abs(value - guess))

    #-- build up what I'm looking for --
    target_signal = []
    #width of signal in MHz
    #determined empiricaly by looking at filter shape
    #expected_width=2.5
    expected_width = 3
    for f in freqs:
        x = (float(f)-float(center))/float(expected_width)
        gderiv = x*exp(-x*x/2.0)
        target_signal.append(0.00001*gderiv)
    dataset_target = sorted(zip(freqs, target_signal))
    #----------------------------------

    #-- Take a scan over frequencies --
    print('Taking Coarse Scan')
    VDC = _GetVoltages(pype, freqs, power=power)
    #----------------------------------

    #--- apply the filter ---
    target_signal_fft = fftpack.fft(target_signal)
    counter_time = range(0, len(freqs))
    #apply the filter
    coarse_data_fft = fftpack.fft(VDC)
    #remove offset
    coarse_data_fft[0] = 0
    #----------------------------------

    #--- apply filter to data ---
    #numpy is a terrible name. it's like the worst
    #nickname for someone in middle school
    filtered_fft = multiply(coarse_data_fft, target_signal_fft)
    filtered = fftpack.ifft(filtered_fft)
    #print("filtered length "+str(len(filtered)))
    #this is awkward, because I have to adjust to the fact that my
    #filter has its zero crossing in the middle
    #firsthalf=range(int(center),int(center+halfspan),init_step)
    firsthalf = range(int(center-halfspan+init_step*ceil(nfreqs/2.0)),
                      int(center+halfspan), init_step)
    secondhalf = range(int(center-halfspan), int(center), init_step)
    #print("firsthalf",firsthalf)
    #print("secondhalf",secondhalf)
    adjusted_freqs = concatenate([firsthalf, secondhalf])
    absfiltered = abs(filtered)
    #print("length of adjusted freqs ",len(adjusted_freqs))
    #print("length of absfiltered ",len(absfiltered))
    #print("last frequency: ",adjusted_freqs[len(adjusted_freqs)-1])

    filtered_toplot = sorted(zip(adjusted_freqs, absfiltered))
    #----------------------------------

    #--- find the peak ---
    largest_f = 0
    largest_p = 0
    for i in range(len(absfiltered)):
        if absfiltered[i] > largest_p:
            largest_p = absfiltered[i]
            largest_f = adjusted_freqs[i]
    result['uncal'] = largest_f
    result['uncal_err'] = init_step
    result['uncal_units'] = 'MHz'
    result['uncal_val'] = (str(result['uncal']) + ' +/- ' +
                           str(result['uncal_err']) + ' ' +
                           str(result['uncal_units']))
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

    #Only plotting beyond this point

    #-- Plot the raw data and filter, for funsies
    dataset_coarse = sorted(zip(freqs, VDC))
    toplot_fdomain_raw = [dataset_coarse, dataset_target]
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
    plot1.plotMany(toplot_fdomain_raw, ['with lines title "data"',
                                        'with lines title "filter"'])
    #----------------------------------
    #--- plot the frequency domain, again for funsies
    print("frequency length "+str(len(freqs)))
    print("fft length "+str(len(target_signal_fft)))
    real_target_signal_fft = abs(target_signal_fft)
    real_coarse_data_fft = abs(coarse_data_fft)
    dataset_target_fft = sorted(zip(counter_time, real_target_signal_fft))
    dataset_coarse_fft = sorted(zip(counter_time, real_coarse_data_fft))
    toplot_tdomain_raw = [dataset_coarse_fft, dataset_target_fft]
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
    plot2.plotMany(toplot_tdomain_raw, ['with lines title "data fft"',
                                        'with lines title "filter fft"'])
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

    return result, zip(*dataset_coarse)
