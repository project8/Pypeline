# built in
from time import sleep
from sys import stdout
# 3rd party
from numpy import std, mean, array, less, arange, pi, where, diff, sign
from scipy import stats, signal
# local
from pypeline import DripInterface, usegnuplot

def GetLockinValue(interface, freq=25553.440, power=-60, slptime=1):
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
    #if 'a'=='a':
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

def GetVoltages(pype, freq_list, power=-40, reference=0, deviation=0.2, stop_condition=1e10):
    '''
        Get a list for frequency <-> lockin voltage pairs with updates to the user

        <pype>:         pypeline DripInterface instance
        <freq_list>:    an iterable of frequencies in MHz
        <reference>:    if stopping at structure, this is the reference voltage (usually mean)
        <deviation>:    if stopping at structure, count number of these away (usually standard deviation)
        <stop_condition>:   number of <deviation> from <reference> to stop looping
    '''
    VDC = []
    for freq in freq_list:
        stdout.write('trying ' + str(freq) + ' MHz\r')
        stdout.flush()
        VDC.append(GetLockinValue(pype, freq, power))
        if abs((VDC[-1]-reference)/deviation) > stop_condition:
            print('something of interest at ' + str(interesting_freq) + ' MHz')
            break
    return VDC

if __name__ == "__main__":
    '''
        If run as: $python dpph_lockin.py, do these things:
    '''
    num_stats_freqs = 5
    pype = DripInterface('http://p8portal.phys.washington.edu:5984')

    freqs = range(25000, 26500, 10)
    
    #determine a mean and standard deviation
    VDC = [GetLockinValue(pype, freq) for freq in freqs[0:num_stats_freqs]]
    VDC_freqs = freqs[0:num_stats_freqs]
    VDC_end = [GetLockinValue(pype, freq) for freq in freqs[-num_stats_freqs:]]
    VDC_std = std(VDC + VDC_end)
    VDC_mean = mean(VDC + VDC_end)
    print('mean is: ' + str(VDC_mean) + ' VDC')
    print('std is: ' + str(VDC_std) + ' VDC')

    #find where the structure starts
    interesting_freq = False
    VDC += GetVoltages(pype, freqs[num_stats_freqs:],
                       reference=VDC_mean, deviation=VDC_std, stop_condition=40)
    VDC_freqs = freqs[:len(VDC)]
    if not len(VDC) == len(freqs):
        interesting_freq = VDC_freqs[-1]

    #take a set of fine data points to capture the structure
    try:
        assert interesting_freq, 'interesting_freq'
        fine_freqs = range(interesting_freq-20, interesting_freq+30, 2)
        VDC_fine = GetVoltages(pype, fine_freqs)
        #find global extrema
        min_index = VDC_fine.index(min(VDC_fine))
        max_index = VDC_fine.index(max(VDC_fine))
        dataset = zip(fine_freqs, VDC_fine)
        #assert VDC_fine[min_index]*VDC_fine[max_index] < 0, 'zero_crossing'
        crossing = where(diff(sign(VDC_fine)))[0][-1]
        assert crossing, 'zero_crossing'

        #zoom in on the zero crossing
#        count = 20
#        left = fine_freqs[min(min_index, max_index)]
#        right = fine_freqs[max(min_index, max_index)]
#        leftV = VDC_fine[fine_freqs.index(left)]
#        rightV = VDC_fine[fine_freqs.index(right)]
#        while count:
#            freq = left - leftV*(right-left)/(rightV-leftV)
#            voltage = GetVoltages(pype, freq)[0]
#            if voltage*leftV<0:
#                right = freq
#                rightV = voltage
#            elif voltage*rightV<0:
#                left = freq
#                leftV = voltage
#            else:
#                assert voltage, 'zero_crossing'
#            dataset = sorted(dataset+[(freq, voltage)])
#            count = (count-1)*((leftV*rightV)<0)*((right-left)>.1)

        #take some very finely spaced data for doing a fit
   #     firstpos = list(array(VDC_fine[glmin:glmax])<0).index(True)+glmin
        very_fine_freqs = arange(fine_freqs[crossing]-.5, fine_freqs[crossing+1]+.5, 0.1)
   #     very_fine_freqs = arange(fine_freqs[firstpos-1], fine_freqs[firstpos], 0.1)
        print('starting very fine grain frequency measurement')
        VDC_very_fine = GetVoltages(pype, very_fine_freqs)#[GetLockinValue(pype, freq) for freq in very_fine_freqs]

        slope, intercept, r_value, p_value, std_err = stats.linregress(array(very_fine_freqs), array(VDC_very_fine))
        

        dataset = zip(fine_freqs+list(very_fine_freqs),VDC_fine+VDC_very_fine)
        fitline = [fine_freqs[min_index], slope*fine_freqs[min_index]+intercept,
                   fine_freqs[max_index], slope*fine_freqs[max_index]+intercept]
        #,zip([VDC_freqs[0],VDC_freqs[-1]],[VDC_freqs[0]*slope+intercept,VDC_freqs[-1]*slope+intercept])]
        plot = usegnuplot.Gnuplot()
        plot.gp("set style line 1 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 2")
        plot.gp("set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2")
        plot.gp("set style line 11 lc rgb '#808080' lt 1")
        plot.gp("set border 3 back ls 11")
        plot.gp("set tics nomirror")
        plot.gp("set style line 12 lc rgb '#808080' lt 0 lw 1")
        plot.gp("set grid back ls 12")
        plot.gp("set xlabel \"Linear Encoder\"")
        plot.gp("set ylabel \"Hall Probe\"")
        plot.gp("unset key")
        plot.g.stdin.write('set arrow from ' + str(fitline[0]) +','+ str(fitline[1]) + ' to ' + str(fitline[2]) +',' + str(fitline[3]) + 'nohead\n')
        plot.plot1d(dataset, '')

        print('Found zero crossing at ' + str(-intercept/slope))
        geff = 2.0036
        chargemass = 1.758e11
        print('find found slope: '+str(slope)+
              'intercept: '+str(intercept)+
              'r_value: '+str(r_value)+
              'p_value: '+str(p_value)+
              'std_err: '+str(std_err))
        print('Field is: ' + str(4*pi*(-intercept/slope)*10**7/(geff*chargemass)) + ' kGauss')
        raw_input('waiting for you to finish looking')

    except AssertionError as e:
        if e[0] == 'interesting_freq':
            print('\nNo interesting frequencies found\n')
        if e[0] == 'zero_crossing':
            print('\nNo zero question \n')
        raise
