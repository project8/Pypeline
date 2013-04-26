# built in
from time import sleep
from sys import stdout
# 3rd party
from numpy import std, mean, array, less, arange, pi, where, diff, sign, polyfit, sqrt
from scipy import optimize
# local
from DripInterface import DripInterface
from usegnuplot import usegnuplot

def GetLockinValue(interface, freq=25553.440, power=-40, slptime=1):
    '''
        Make a reading with the lockin amplifier at a specific frequency.

        Inputs:
            <interface> a DripInterface object
            <freq>      the frequency in MHz
            <power>     the sweeper power in dBm

        Output:
            <reading>   the DVM reading in Volts DC from the lockin
    '''
    try:
        interface.Set('hf_cw_freq', freq).Wait()['result']=='ok'
        interface.Set('hf_sweeper_power', power).Wait()['result']=='ok'
        sleep(slptime)
        out = interface.Get('lockin_out').Wait()
        return float(out['final'].strip().strip('NDCV'))
    except KeyError as keyname:
        if keyname[0] == 'result':
            print('failed to interface with sweeper')
            raise
        elif keyname[0] == 'final':
            print('failed to interface with dvm')
            raise
        else:
            raise

def GetVoltages(pype, freq_list, power=-40, reference=0, deviation=0.2, stop_sigma=1e10, stop_volts=20):
    '''
        Get a list for frequency <-> lockin voltage pairs with updates to the user

        <pype>:         pypeline DripInterface instance
        <freq_list>:    an iterable of frequencies in MHz
        <reference>:    if stopping at structure, this is the reference voltage (usually mean)
        <deviation>:    if stopping at structure, count number of these away (usually standard deviation)
        <stop_sigma>:   number of <deviation> from <reference> to stop looping
    '''
    VDC = []
#    interest = False
    for freq in freq_list:
        stdout.write('trying ' + str(freq) + ' MHz\r')
        stdout.flush()
        VDC.append(GetLockinValue(pype, freq, power))
        if (abs((VDC[-1]-reference)/deviation) > stop_sigma) or (abs(VDC[-1]) > stop_volts):
#            if interest:
                print('something of interest (' + str(VDC[-1]) + ' V) at ' + str(freq) + ' MHz')
                break
#            else:
#                interest = True
#        else:
#            interest = False
    return VDC

#if __name__ == "__main__":
def dpph_lockin(pype):
    '''
        Do a dpph scan using DripInterface instance <pype>
    '''
    num_stats_freqs = 5

    freqs = range(25000, 26500, 10)
    
    #determine a mean and standard deviation
    VDC = [GetLockinValue(pype, freq) for freq in freqs[0:num_stats_freqs]]
    VDC_freqs = freqs[0:num_stats_freqs]
    VDC_end = [GetLockinValue(pype, freq) for freq in freqs[-num_stats_freqs:]]
    VDC_std = std(VDC + VDC_end)
    VDC_mean = mean(VDC + VDC_end)
    print('mean is: ' + str(VDC_mean) + ' VDCi')
    print('std is: ' + str(VDC_std) + ' VDC')

    #find where the structure starts
    interesting_freq = False
    VDC += GetVoltages(pype, freqs[num_stats_freqs:],
                       reference=VDC_mean, deviation=VDC_std, stop_sigma=30, stop_volts=1)
    VDC_freqs = freqs[:len(VDC)]
    if not len(VDC) == len(freqs):
        interesting_freq = VDC_freqs[-2]
    else:
        for pair in zip(freqs, VDC):
            print(pair)

    #take a set of fine data points to capture the structure
    try:
        assert interesting_freq, 'interesting_freq'
        fine_freqs = range(interesting_freq-30, interesting_freq+30, 2)
        VDC_fine = GetVoltages(pype, fine_freqs)
        #find zero crossing
        min_index = VDC_fine.index(min(VDC_fine))
        max_index = VDC_fine.index(max(VDC_fine))
        crossing = min(min_index,max_index) + where(diff(sign(VDC_fine[min(min_index,max_index):max(min_index,max_index)])))[0][-1]
        assert crossing, 'zero_crossing'
        est = fine_freqs[crossing]-VDC_fine[crossing]*(fine_freqs[crossing+1]-fine_freqs[crossing])/(VDC_fine[crossing+1]-VDC_fine[crossing])

        #take some very finely spaced data for doing a fit
        very_fine_freqs = arange(est-1, est+1, 0.1)
        print('starting very fine grain frequency measurement')
        VDC_very_fine = GetVoltages(pype, very_fine_freqs)

        fitfunc = lambda p, x: p[1] * (x - p[0])
        errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err
        p_in = [25000.0, -1.0]
        fit = optimize.leastsq(errfunc, p_in, args=(array(very_fine_freqs), array(VDC_very_fine), array([1e-5]*len(very_fine_freqs))), full_output=1)
        resonance = fit[0][0]
        slope = fit[0][1]
        cov = fit[1]
        resonance_err = (0.0002/2.0036)*resonance

        dataset = sorted(zip(fine_freqs+list(very_fine_freqs),VDC_fine+VDC_very_fine))
        fitline = [very_fine_freqs[0], slope * (very_fine_freqs[0]-resonance),
                   very_fine_freqs[-1], slope * (very_fine_freqs[-1]-resonance)]

        plot = usegnuplot.Gnuplot()
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
        plot.g.stdin.write('set arrow from ' + str(fitline[0]) +','+ str(fitline[1]) + ' to ' + str(fitline[2]) +',' + str(fitline[3]) + 'nohead\n')
        plot.plot1d(dataset, '')

        print('Found zero crossing at ' + str(resonance) + ' +/- ' + str(resonance_err) + ' MHz')
        geff = 2.0036
        chargemass = 1.758e11
        freq_to_field = 4*pi*10**7/(geff*chargemass)
        print('Field is: ' + str(freq_to_field*resonance) + ' +/- ' + str(freq_to_field*resonance_err) + ' kGauss')
        raw_input('waiting for you to finish looking')

    except AssertionError as e:
        if e[0] == 'interesting_freq':
            print('\n' + '*'*60 + '\nNo interesting frequencies found\n' + '*'*60 + '\n')
        if e[0] == 'zero_crossing':
            print('\n' + '*'*60 + '\nNo zero question\n' + '*'*60 + '\n')
        raise
