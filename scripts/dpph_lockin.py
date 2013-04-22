# built in
from time import sleep
from sys import stdout
# 3rd party
from numpy import std, mean, array, less
from scipy import stats, signal
# local
from pypeline import DripInterface, usegnuplot

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

if __name__ == "__main__":
    '''
        If run as: $python dpph_lockin.py, do these things:
    '''
    num_stats_freqs = 5
    pype = DripInterface('http://p8portal.phys.washington.edu:5984')

#    freqs = range(25000, 26500, 10)
    freqs = range(25640, 26500, 10)

    VDC = [GetLockinValue(pype, freq) for freq in freqs[0:num_stats_freqs]]
    VDC_freqs = freqs[0:num_stats_freqs]
    VDC_end = [GetLockinValue(pype, freq) for freq in freqs[-num_stats_freqs:]]
    VDC_std = std(VDC + VDC_end)
    VDC_mean = mean(VDC + VDC_end)
    print('mean is: ' + str(VDC_mean) + ' VDC')
    print('std is: ' + str(VDC_std) + ' VDC')

    interesting_freq = False
    for freq in freqs[num_stats_freqs:]:
        #print('trying ' + str(freq) + ' MHz')
        stdout.write('trying ' + str(freq) + ' MHz\r')
        stdout.flush()
        VDC.append(GetLockinValue(pype, freq))
        VDC_freqs.append(freq)
        if abs((VDC[-1]-VDC_mean)/VDC_std) > 40:
            interesting_freq = freq
            print('something of interest at ' + str(interesting_freq) + ' MHz')
            break
    try:
        assert interesting_freq, 'interesting_freq'
        fine_freqs = range(interesting_freq-15, interesting_freq+25)
        VDC = VDC + [GetLockinValue(pype, freq) for freq in fine_freqs]
        VDC_freqs += fine_freqs
        #for freq,volt in zip(VDC_freqs, VDC):
        #    print(str(freq) + ' MHz -> ' + str(volt) + ' V')
        min_index = VDC.index(min(VDC))
        max_index = VDC.index(max(VDC))
        minima = signal.argrelextrema(array(VDC), less)[0]
        min_index = max((array(VDC)[minima]<0)*minima)
        slope, intercept, r_value, p_value, std_err = stats.linregress(array(VDC_freqs[min_index:max_index]), array(VDC[min_index:max_index]))

        dataset = zip(VDC_freqs,VDC)
        fitline = [VDC_freqs[min_index], slope*VDC_freqs[min_index]+intercept,
                   VDC_freqs[max_index], slope*VDC_freqs[max_index]+intercept]
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
        plot.plot1d(dataset[0], ' with lines')
        raw_input('Found zero crossing at ' + str(-intercept/slope) + '\nwaiting for you to finish looking')

    except AssertionError as e:
        if e[0] == 'interesting_freq':
            print('No interesting frequencies found')
        raise
