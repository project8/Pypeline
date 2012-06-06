#!/usr/bin/python3

import Pypeline

pype = Pypeline.Pypeline('http://p8portal.phys.washington.edu:5984')

#set initial values
pype.Set('hf_sweeper_power',1)######## 1 should be changed to something real

for lo_cw_freq in range(300, 2001, 50):
    pype.Set('lo_cw_freq',lo_cw_freq)
    for hf_cw_freq in range(lo_cw_freq+5+24500):
        pype.Set('hf_cw_freq',hf_cw_freq)
        #pype.<something to take a short run> ######## fix this line to do somethingjj

#make plots
values = []
for lo_cw_freq in range(300, 2001, 50):
    for hf_cw_freq in range(lo_cw_freq+5+24500):
        #either call a compiled katydid program to return the output or some lines of katydid
        #an array or TH2D[low_cw_freq,hf_cw_freq].Fill(value from last line)
# Make the desired cut(s) and plot the 2D rather than 1D result
