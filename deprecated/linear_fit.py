from __future__ import print_function, absolute_import
# built in
# 3rd party
from numpy import std, mean, array, arange, pi, where, diff, sign
from scipy import optimize
# local
from ...usegnuplot import Gnuplot
from .dpph_utils import _GetVoltages


def linear_fit(pype, guess=25000, stop_nsigma=30, stop_voltage=9e-7,
               power=-75):
    '''
        Do a dpph scan using DripInterface instance <pype>

        Inputs:
            <guess> is an intial guess for the starting frequency
    '''
    result = {}
    fitline = False
    dataset = sorted(zip([0], [0]))
    num_stats_freqs = 10

    init_step = 2
    if guess == 25000:
        init_step = 5
    freqs = range(25000, 26500, init_step)
    freqs.sort(key=lambda value: abs(value - guess))

    # determine a mean and standard deviation
    print('determining mean and standard deviation')
    VDC = _GetVoltages(pype, freqs[-num_stats_freqs:], power=power)
    VDC_freqs = freqs[-num_stats_freqs:]
    VDC_std = std(VDC)
    VDC_mean = mean(VDC)
    print('mean is: ' + str(VDC_mean) + ' VDC')
    print('std is: ' + str(VDC_std) + ' VDC')

    # find where the structure starts
    interesting_freq = False
    print('looking for structure')
    VDC = _GetVoltages(pype, freqs, reference=VDC_mean, deviation=VDC_std,
                       stop_sigma=stop_nsigma, stop_volts=stop_voltage,
                       power=power)
    VDC_freqs = freqs[:len(VDC)]
    if not len(VDC) == len(freqs):
        interesting_freq = VDC_freqs[-1]
    dataset = sorted(zip(VDC_freqs, VDC))

    # take a set of fine data points to capture the structure
    try:
        assert interesting_freq, 'interesting_freq'
        fine_freqs = range(interesting_freq - 25, interesting_freq + 20, 2)
        print('coarse scan of structure')
        VDC_fine = _GetVoltages(pype, fine_freqs, power=power)
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
            VDC_very_fine = _GetVoltages(pype, very_fine_freqs, power=power)
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
    return result, zip(*dataset)
