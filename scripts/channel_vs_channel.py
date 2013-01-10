'''
    Utility script which will plot logger data for two channels, one against the other.

    Per usual, the module can be can be imported and the function used in some other module, or called directly from the terminal with arguments unpacked into the arguments in order.
'''

# standard libraries
import sys
from datetime import datetime, timedelta
# third party libraries
# pypeline and 'internal' libraries
import pypeline

def channel_vs_channel(channely, channelx, start, stop):
    '''
        Utility function which will plot logger data for two channels, one against the other.
        <channely> is the channel name for y values (a string)
        <channelx> is the channel name for x values (a string)
        <start> is the start time for the plot (a datetime object)
        <stop> is the stop time for the plot (a datetime object)
    '''
    ldh = pypeline.LoggedDataHandler('http://p8portal.phys.washington.edu:5984')
    string_format = '%Y-%m-%d %H:%M:%S'
    xdata = ldh.Get(channelx, start.strftime(string_format), stop.strftime(string_format))
    ydata = ldh.Get(channely, start.strftime(string_format), stop.strftime(string_format))
    ys=[]
    xs=[]
    for tx,x in zip(xdata[0], xdata[1]):
        xtmp = False
        ytmp = False
        dt = timedelta(seconds=60)
        for ty,y in zip(ydata[0], ydata[1]):
            if abs(ty-tx) < dt:
                dt = abs(ty-tx)
                xtmp = x
                ytmp = y
        if xtmp and ytmp:
            ys.append(ytmp)
            xs.append(xtmp)
    dataset = sorted(zip(xs,ys))
    plot = pypeline.usegnuplot.Gnuplot()
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
    plot.plot1d(dataset, ' with lines')
    raw_input('waiting for you to finish looking')

if __name__=='__main__':
    print('in main:')
    print(len(sys.argv))
    try:
        # hall probe vs linear encoder, is the one I want now and a reasonable default for tests. This will probably be removed and instead print usage once finished.
        if len(sys.argv) == 1:
            print('got 2 args')
            channel_vs_channel('hall_probe_voltage', 'linear_encoder', datetime(2012,12,20,15,27), datetime(2012,12,20,15,57))
        elif len(sys.argv) > 1:
            channel_vs_channel(*sys.argv[1:])
    except:
        print("it didn't work, I'll put in better exception catching later")
        print("probably bad arguments... you gave this:")
        print(sys.argv[1:])
