'''
    This script checks the functionality of all channels in Pypeline.
'''

from Pypeline import DripInterface

drip = DripInterface('http://p8portal.phys.washington.edu:5984')
clist = drip.EligibleChannels()

# ============== Check bypass valve temp =================
try:
    if drip.Get('bypass_valve_t')['final'][0] == '-':
        print "bypass_valve_t reading negative temperature " + repr(drip.Get('bypass_valve_t'))
    else:
        print "bypass_valve_t ok" + repr(drip.Get('bypass_valve_t'))
except KeyError:
    try:
        if drip.Get('bypass_valve_t')['final'][0] == '-':
            print "bypass_valve_t reading negative temperature " + repr(drip.Get('bypass_valve_t'))
        else:
            print "bypass_valve_t ok" + repr(drip.Get('bypass_valve_t'))
    except KeyError:
        print "bypass_valve_t not responding"
            
# =========== Check temperature sensors on cable A ================
try:
    if drip.Get('cernox_a_t1')['final'][0] == '-':
        print "cernox_a_t1 reading negative resistance " + repr(drip.Get('cernox_a_t1'))
    else:
        print "cernox_a_t1 ok " + repr(drip.Get('cernox_a_t1'))
except KeyError:
    try:
        if drip.Get('cernox_a_t1')['final'][0] == '-':
            print "cernox_a_t1 reading negative resistance " + repr(drip.Get('cernox_a_t1'))
        else:
            print "cernox_a_t1 ok " + repr(drip.Get('cernox_a_t1'))
    except KeyError:
        print "cernox_a_t1 not responding"
        
try:
    if drip.Get('cernox_a_t2')['final'][0] == '-':
        print "cernox_a_t2 reading negative resistance " + repr(drip.Get('cernox_a_t2'))
    else:
        print "cernox_a_t2 ok " + repr(drip.Get('cernox_a_t2'))
except KeyError:
    try:
        if drip.Get('cernox_a_t2')['final'][0] == '-':
            print "cernox_a_t2 reading negative resistance " + repr(drip.Get('cernox_a_t2'))
        else:
            print "cernox_a_t2 ok " + repr(drip.Get('cernox_a_t2'))
    except KeyError:
        print "cernox_a_t2 not responding"
        
try:
    if drip.Get('cernox_a_t3')['final'][0] == '-':
        print "cernox_a_t3 reading negative resistance " + repr(drip.Get('cernox_a_t3'))
    else:
        print "cernox_a_t3 ok " + repr(drip.Get('cernox_a_t3'))
except KeyError:
    try:
        if drip.Get('cernox_a_t3')['final'][0] == '-':
            print "cernox_a_t3 reading negative resistance " + repr(drip.Get('cernox_a_t3'))
        else:
            print "cernox_a_t3 ok " + repr(drip.Get('cernox_a_t3'))
    except KeyError:
        print "cernox_a_t3 not responding"
        
try:
    if drip.Get('cernox_a_t4')['final'][0] == '-':
        print "cernox_a_t4 reading negative resistance " + repr(drip.Get('cernox_a_t4'))
    else:
        print "cernox_a_t4 ok " + repr(drip.Get('cernox_a_t4'))
except KeyError:
    try:
        if drip.Get('cernox_a_t4')['final'][0] == '-':
            print "cernox_a_t4 reading negative resistance " + repr(drip.Get('cernox_a_t4'))
        else:
            print "cernox_a_t4 ok " + repr(drip.Get('cernox_a_t4'))
    except KeyError:
        print "cernox_a_t4 not responding"


# =========== Check temperature sensors on cable C ================
try:
    if drip.Get('cernox_c_t1')['final'][0] == '-':
        print "cernox_c_t1 reading negative resistance " + repr(drip.Get('cernox_c_t1'))
    else:
        print "cernox_c_t1 ok " + repr(drip.Get('cernox_c_t1'))
except KeyError:
    try:
        if drip.Get('cernox_c_t1')['final'][0] == '-':
            print "cernox_c_t1 reading negative resistance " + repr(drip.Get('cernox_c_t1'))
        else:
            print "cernox_c_t1 ok " + repr(drip.Get('cernox_c_t1'))
    except KeyError:
        print "cernox_c_t1 not responding"
        
try:
    if drip.Get('cernox_c_t2')['final'][0] == '-':
        print "cernox_c_t2 reading negative resistance " + repr(drip.Get('cernox_c_t2'))
    else:
        print "cernox_c_t2 ok " + repr(drip.Get('cernox_c_t2'))
except KeyError:
    try:
        if drip.Get('cernox_c_t2')['final'][0] == '-':
            print "cernox_c_t2 reading negative resistance " + repr(drip.Get('cernox_c_t2'))
        else:
            print "cernox_c_t2 ok " + repr(drip.Get('cernox_c_t2'))
    except KeyError:
        print "cernox_c_t2 not responding"
        
try:
    if drip.Get('cernox_c_t3')['final'][0] == '-':
        print "cernox_c_t3 reading negative resistance " + repr(drip.Get('cernox_c_t3'))
    else:
        print "cernox_c_t3 ok " + repr(drip.Get('cernox_c_t3'))
except KeyError:
    try:
        if drip.Get('cernox_c_t3')['final'][0] == '-':
            print "cernox_c_t3 reading negative resistance " + repr(drip.Get('cernox_c_t3'))
        else:
            print "cernox_c_t3 ok " + repr(drip.Get('cernox_c_t3'))
    except KeyError:
        print "cernox_c_t3 not responding"
        
try:
    if drip.Get('cernox_c_t4')['final'][0] == '-':
        print "cernox_c_t4 reading negative resistance " + repr(drip.Get('cernox_c_t4'))
    else:
        print "cernox_c_t4 ok " + repr(drip.Get('cernox_c_t4'))
except KeyError:
    try:
        if drip.Get('cernox_c_t4')['final'][0] == '-':
            print "cernox_c_t4 reading negative resistance " + repr(drip.Get('cernox_c_t4'))
        else:
            print "cernox_c_t4 ok " + repr(drip.Get('cernox_c_t4'))
    except KeyError:
        print "cernox_c_t4 not responding"

# ============== Check getter valve temp =================
try:
    if drip.Get('getter_valve_t')['final'][0] == '-':
        print "getter_valve_t reading negative temperature " + repr(drip.Get('getter_valve_t'))
    else:
        print "getter_valve_t ok " + repr(drip.Get('getter_valve_t'))
except KeyError:
    try:
        if drip.Get('getter_valve_t')['final'][0] == '-':
            print "getter_valve_t reading negative temperature " + repr(drip.Get('getter_valve_t'))
        else:
            print "getter_valve_t ok " + repr(drip.Get('getter_valve_t'))
    except KeyError:
        print "getter_valve_t not responding"

# =============== Check high frequency ===================
try:
    drip.Set('hf_cw_freq', '25000')
    if int(drip.Get('hf_cw_freq')['final']) != 25000000:
        print "error setting hf_cw_freq to 25 GHz " + repr(drip.Get('hf_cw_freq'))
    else:
        print "hf_cw_freq ok " + repr(drip.Get('hf_cw_freq'))
except KeyError:
    try:
        drip.Set('hf_cw_freq', '25000')
        if int(drip.Get('hf_cw_freq')['final']) != 25000000:
            print "error setting hf_cw_freq to 25 GHz " + repr(drip.Get('hf_cw_freq'))
        else:
            print "hf_cw_freq ok " + repr(drip.Get('hf_cw_freq'))
    except KeyError:
        print "hf_cw_freq not responding"
#try:
#drip.Set('hf_sweep_start', '24000')
#drip.Set('hf_sweep_stop', '25000')
#drip.Set('hf_sweep_time', '1000')
#if drip.Get('hf_sweep_start') !=
