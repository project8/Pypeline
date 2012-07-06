'''
    This script checks the functionality of all channels in Pypeline:

    bypass_valve_t
    cernox_a_t1
    cernox_a_t2
    cernox_a_t3
    cernox_a_t4
    getter_valve_t
    hf_cw_freq
    hf_sweep_start
    hf_sweep_stop
    hf_sweep_time
    hf_sweeper_power
    ignatius_data_disk
    inlet_pressure
    linear_encoder
    lo_cw_freq
    lo_power_level
    outlet_pressure
    p8portal_root_disk
    platinum_rtd_c_t1
    platinum_rtd_c_t2
    platinum_rtd_c_t3
    platinum_rdt_c_t4
    pump_valve_t
    vent_valve_t
'''

from Pypeline import DripInterface
import sys

drip = DripInterface('http://p8portal.phys.washington.edu:5984')


# ============== Check bypass valve temp =================
try:
    if drip.Get('bypass_valve_t')['final'][0] == '-':
        print "bypass_valve_t reading negative temperature " + repr(drip.Get('bypass_valve_t'))
    elif drip.Get('bypass_valve_t')['final'][0] == '+':
        print "bypass_valve_t ok " + repr(drip.Get('bypass_valve_t'))
    else:
        print "bypass_valve_t reading unexpected value " + repr(drip.Get('bypass_valve_t'))
except KeyError:
    try:
        if drip.Get('bypass_valve_t')['final'][0] == '-':
            print "bypass_valve_t reading negative temperature " + repr(drip.Get('bypass_valve_t'))
        elif drip.Get('bypass_valve_t')['final'][0] == '+':
            print "bypass_valve_t ok " + repr(drip.Get('bypass_valve_t'))
        else:
            print "bypass_valve_t reading unexpected value " + repr(drip.Get('bypass_valve_t'))
    except KeyError:
        print "bypass_valve_t not responding"
    except:
        print "bypass_valve_t unexpected error:", sys.exc_info()[0]
except:
    print "bypass_valve_t unexpected error:", sys.exc_info()[0]
            
# =========== Check cernox temperature sensors on cable A ================
try:
    if drip.Get('cernox_a_t1')['final'][0].isdigit():
        print "cernox_a_t1 ok " + repr(drip.Get('cernox_a_t1'))
    else:
        print "cernox_a_t1 reading unexpected value " + repr(drip.Get('cernox_a_t1'))
except KeyError:
    try:
        if drip.Get('cernox_a_t1')['final'][0].isdigit():
            print "cernox_a_t1 ok " + repr(drip.Get('cernox_a_t1'))
        else:
            print "cernox_a_t1 reading unexpected value " + repr(drip.Get('cernox_a_t1'))
    except KeyError:
        print "cernox_a_t1 not responding"
    except:
        print "cernox_a_t1 unexpected error:", sys.exc_info()[0]
except:
    print "cernox_a_t1 unexpected error:", sys.exc_info()[0]
        
try:
    if drip.Get('cernox_a_t2')['final'][0].isdigit():
        print "cernox_a_t2 ok " + repr(drip.Get('cernox_a_t2'))
    else:
        print "cernox_a_t2 reading unexpected value " + repr(drip.Get('cernox_a_t2'))
except KeyError:
    try:
        if drip.Get('cernox_a_t2')['final'][0].isdigit():
            print "cernox_a_t2 ok " + repr(drip.Get('cernox_a_t2'))
        else:
            print "cernox_a_t2 reading unexpected value " + repr(drip.Get('cernox_a_t2'))
    except KeyError:
        print "cernox_a_t2 not responding"
    except:
        print "cernox_a_t2 unexpected error:", sys.exc_info()[0]
except:
    print "cernox_a_t2 unexpected error:", sys.exc_info()[0]
        
try:
    if drip.Get('cernox_a_t3')['final'][0].isdigit():
        print "cernox_a_t3 ok " + repr(drip.Get('cernox_a_t3'))
    else:
        print "cernox_a_t3 reading unexpected value " + repr(drip.Get('cernox_a_t3'))
except KeyError:
    try:
        if drip.Get('cernox_a_t3')['final'][0].isdigit():
            print "cernox_a_t3 ok " + repr(drip.Get('cernox_a_t3'))
        else:
            print "cernox_a_t3 reading unexpected value " + repr(drip.Get('cernox_a_t3'))
    except KeyError:
        print "cernox_a_t3 not responding"
    except:
        print "cernox_a_t3 unexpected error:", sys.exc_info()[0]
except:
    print "cernox_a_t3 unexpected error:", sys.exc_info()[0]
        
try:
    if drip.Get('cernox_a_t4')['final'][0].isdigit():
        print "cernox_a_t4 ok " + repr(drip.Get('cernox_a_t4'))
    else:
        print "cernox_a_t4 reading unexpected value " + repr(drip.Get('cernox_a_t4'))
except KeyError:
    try:
        if drip.Get('cernox_a_t4')['final'][0].isdigit():
            print "cernox_a_t4 ok " + repr(drip.Get('cernox_a_t4'))
        else:
            print "cernox_a_t4 reading unexpected value " + repr(drip.Get('cernox_a_t4'))
    except KeyError:
        print "cernox_a_t4 not responding"
    except:
        print "cernox_a_t4 unexpected error:", sys.exc_info()[0]
except:
    print "cernox_a_t4 unexpected error:", sys.exc_info()[0]

# ============== Check getter valve temp =================
try:
    if drip.Get('getter_valve_t')['final'][0] == '-':
        print "getter_valve_t reading negative temperature " + repr(drip.Get('getter_valve_t'))
    elif drip.Get('getter_valve_t')['final'][0] == '+':
        print "getter_valve_t ok " + repr(drip.Get('getter_valve_t'))
    else:
        print "getter_valve_t reading unexpected value " + repr(drip.Get('getter_valve_t'))
except KeyError:
    try:
        if drip.Get('getter_valve_t')['final'][0] == '-':
            print "getter_valve_t reading negative temperature " + repr(drip.Get('getter_valve_t'))
        elif drip.Get('getter_valve_t')['final'][0] == '+':
            print "getter_valve_t ok " + repr(drip.Get('getter_valve_t'))
        else:
            print "getter_valve_t reading unexpected value " + repr(drip.Get('getter_valve_t'))
    except KeyError:
        print "getter_valve_t not responding"
    except:
        print "getter_valve_t unexpected error:", sys.exc_info()[0]
except:
    print "getter_valve_t unexpected error:", sys.exc_info()[0]

# =============== Check high frequency ===================
try:
    drip.Set('hf_cw_freq', '25000')
    if int(drip.Get('hf_cw_freq')['final']) != 25000000000:
        print "error setting hf_cw_freq to 25 GHz " + repr(drip.Get('hf_cw_freq'))
    else:
        print "hf_cw_freq ok " + repr(drip.Get('hf_cw_freq'))
except KeyError:
    try:
        drip.Set('hf_cw_freq', '25000')
        if int(drip.Get('hf_cw_freq')['final']) != 25000000000:
            print "error setting hf_cw_freq to 25 GHz " + repr(drip.Get('hf_cw_freq'))
        else:
            print "hf_cw_freq ok " + repr(drip.Get('hf_cw_freq'))
    except KeyError:
        print "hf_cw_freq not responding"
    except:
        print "hf_cw_freq unexpected error:", sys.exc_info()[0]
except:
    print "hf_cw_freq unexpected error:", sys.exc_info()[0]
    
try:
    drip.Set('hf_sweep_start', '24000')
    if int(drip.Get('hf_sweep_start')['final']) != 24000000000:
        print "error setting hf_sweep_start to 24 GHz " + repr(drip.Get('hf_sweep_start'))
    else:
        print "hf_sweep_start ok " + repr(drip.Get('hf_sweep_start'))
except KeyError:
    try:
        drip.Set('hf_sweep_start', '24000')
        if int(drip.Get('hf_sweep_start')['final']) != 24000000000:
            print "error setting hf_sweep_start to 24 GHz " + repr(drip.Get('hf_sweep_start'))
        else:
            print "hf_sweep_start ok " + repr(drip.Get('hf_sweep_start'))
    except KeyError:
        print "hf_sweep_start not responding"
    except:
        print "hf_sweep start unexpected error:", sys.exc_info()[0]
except:
    print "hf_sweet_start unexpected error:", sys.exc_info()[0]
    
try:
    drip.Set('hf_sweep_stop', '25000')
    if int(drip.Get('hf_sweep_stop')['final']) != 25000000000:
        print "error setting hf_sweep_stop to 25 GHz " + repr(drip.Get('hf_sweep_stop'))
    else:
        print "hf_sweep_stop ok " + repr(drip.Get('hf_sweep_stop'))
except KeyError:
    try:
        drip.Set('hf_sweep_stop', '25000')
        if int(drip.Get('hf_sweep_stop')['final']) != 25000000000:
            print "error setting hf_sweep_stop to 25 GHz " + repr(drip.Get('hf_sweep_stop'))
        else:
            print "hf_sweep_stop ok " + repr(drip.Get('hf_sweep_stop'))
    except KeyError:
        print "hf_sweep_stop not responding"
    except:
        print "hf_sweep_stop unexpected error:", sys.exc_info()[0]
except:
    print "hf_sweep_Stop unexpected error:", sys.exc_info()[0]
        
try:
    drip.Set('hf_sweep_time', '1000')
    if float(drip.Get('hf_sweep_time')['final']) != 1:
        print "error setting hf_sweep_time to 1000 ms " + repr(drip.Get('hf_sweep_time'))
    else:
        print "hf_sweep_time ok " + repr(drip.Get('hf_sweep_time'))
except KeyError:
    try:
        drip.Set('hf_sweep_time', '1000')
        if float(drip.Get('hf_sweep_time')['final']) != 1:
            print "error setting hf_sweep_time to 1000 ms " + repr(drip.Get('hf_sweep_time'))
        else:
            print "hf_sweep_time ok " + repr(drip.Get('hf_sweep_time'))
    except KeyError:
        print "hf_sweep_time not responding"
    except:
        print "hf_sweep_time unexpected error:", sys.exc_info()[0]
except:
    print "hf_sweep_time unexpected error:", sys.exc_info()[0]
    
try:
    drip.Set('hf_sweeper_power', '-31')
    if float(drip.Get('hf_sweeper_power')['final']) != -31:
        print "error setting hf_sweeper_power to -31 dB " + repr(drip.Get('hf_sweeper_power'))
    else:
        print "hf_sweeper_power ok " + repr(drip.Get('hf_sweeper_power')['final'])
except KeyError:
    try:
        drip.Set('hf_sweeper_power', '-31')
        if float(drip.Get('hf_sweeper_power')['final']) != -31:
            print "error setting hf_sweeper_power to -31 dB " + repr(drip.Get('hf_sweeper_power'))
        else:
            print "hf_sweeper_power ok " + repr(drip.Get('hf_sweeper_power')['final'])
    except KeyError:
        print "hr_sweeper_power not responding"
    except:
        print "hf_sweeper_power unexpected error:", sys.exc_info()[0]
except:
    print "hf_sweeper_power unexpected error:", sys.exc_info()[0]

# ======================== Check Ignatius Data Disk =======================
try:
    print "ignatius_data_disk ok " + '\n' + drip.Get('ignatius_data_disk')['final']
except KeyError:
    try:
        print "ignatius_data_disk ok " + '\n' + drip.Get('ignatius_data_disk')['final']
    except KeyError:
        print "ignatius_data_disk not responding"
    except:
        print "ignatius_data_disk unexpected error", sys.exc_info()[0]
except:
    print "ignatius_data_disk unexpected error", sys.exc_info()[0]
    
# ========================= Check Inlet Pressure ==========================
try:
    if drip.Get('inlet_pressure')['final'][0].isdigit():
        if float(drip.Get('inlet_pressure')['final'].split()[0]) < 1000:
            print "inlet_pressure ok " + repr(drip.Get('inlet_pressure'))
        else:
            print "inlet_pressure malfunction " + repr(drip.Get('inlet_pressure'))
    else:
        print "inlet_pressure reading unexpected value " + repr(drip.Get('inlet_pressure'))
except KeyError:
    try:
        if drip.Get('inlet_pressure')['final'][0].isdigit():
            if float(drip.Get('inlet_pressure')['final'].split()[0]) > 1000:
                print "inlet_pressure ok " + repr(drip.Get('inlet_pressure'))
            else:
                print "inlet_pressure malfunction " + repr(drip.Get('inlet_pressure'))
        else:
            print "inlet_pressure reading unexpected value " + repr(drip.Get('inlet_pressure'))
    except KeyError:
        print "inlet_pressure not responding"
    except:
        print "inlet_pressure unexpected error", sys.exc_info()[0]
except:
    print "inlet_pressure unexpected error", sys.exc_info()[0]

# ========================= Check Linear Encoder ==========================
try:
    if drip.Get('linear_encoder')['final'][0].isdigit():
        print "linear_encoder ok " + repr(drip.Get('linear_encoder'))
    else:
        print "linear_encoder reading unexpected value " + repr(drip.Get('linear_encoder'))
except KeyError:
    try:
        if drip.Get('linear_encoder')['final'][0].isdigit():
            print "linear_encoder ok " + repr(drip.Get('linear_encoder'))
        else:
            print "linear_encoder reading unexpected value " + repr(drip.Get('linear_encoder'))
    except KeyError:
        print "linear_encoder not responding"
    except:
        print "linear_encoder unexpected error:", sys.exc_info()[0]
except:
    print "linear_encoder unexpected error:", sys.exc_info()[0]

# ========================= Check Local Oscilltor =========================
try:
    if str(drip.Set('lo_cw_freq', '400')) == '<ok>':
        print "lo_cw_freq ok <400 MHz>"
    else:
        "lo_cw_freq not responding"
except:
    "lo_cw_freq not responding", sys.exc_info()[0]

try:
    if str(drip.Set('lo_power_level', '-30')) == '<ok>':
        print "lo_power_level ok <-30 dB>"
    else:
        "lo_power_level not responding"
except:
    "lo_power_level not responding", sys.exc_info()[0]
    
# ========================= Check Outlet Pressure =========================
try:
    if drip.Get('outlet_pressure')['final'][0].isdigit():
        if float(drip.Get('outlet_pressure')['final'].split()[0]) < 1000:
            print "outlet_pressure ok " + repr(drip.Get('outlet_pressure'))
        else:
            print "outlet_pressure malfunction " + repr(drip.Get('outlet_pressure'))
    else:
        print "outlet_pressure reading unexpected value " + repr(drip.Get('outlet_pressure'))
except KeyError:
    try:
        if drip.Get('outlet_pressure')['final'][0].isdigit():
            if float(drip.Get('outlet_pressure')['final'].split()[0]) > 1000:
                print "outlet_pressure ok " + repr(drip.Get('outlet_pressure'))
            else:
                print "outlet_pressure malfunction " + repr(drip.Get('outlet_pressure'))
        else:
            print "outlet_pressure reading unexpected value " + repr(drip.Get('outlet_pressure'))
    except KeyError:
        print "outlet_pressure not responding"
    except:
        print "outlet_pressure unexpected error", sys.exc_info()[0]
except:
    print "outlet_pressure unexpected error", sys.exc_info()[0]

# ======================== Check p8portal Root Disk =======================
try:
    print "p8portal ok " + '\n' + drip.Get('p8portal_root_disk')['final']
except KeyError:
    try:
        print "p8portal ok " + '\n' + drip.Get('p8portal_root_disk')['final']
    except KeyError:
        print "p9portal_root_disk not responding"
    except:
        print "p8portal_root_disk unexpected error", sys.exc_info()[0]
except:
    print "p8portal_root_disk unexpected error", sys.exc_info()[0]
    
# ============== Check Pt temperature sensors on cable C ==================
try:
    if drip.Get('platinum_rtd_c_t1')['final'][0] == '-':
        print "platinum_rtd_c_t1 reading negative temperature " + repr(drip.Get('platinum_rtd_c_t1'))
    elif drip.Get('platinum_rtd_c_t1')['final'][0] == '+':
        print "platinum_rtd_c_t1 ok " + repr(drip.Get('platinum_rtd_c_t1'))
    else:
        print "platinum_rtd_c_t1 reading unexpected value " + repr(drip.Get('platinum_rtd_c_t1'))
except KeyError:
    try:
        if drip.Get('platinum_rtd_c_t1')['final'][0] == '-':
            print "platinum_rtd_c_t1 reading negative temperature " + repr(drip.Get('platinum_rtd_c_t1'))
        elif drip.Get('platinum_rtd_c_t1')['final'][0] == '+':
            print "platinum_rtd_c_t1 ok " + repr(drip.Get('platinum_rtd_c_t1'))
        else:
            print "platinum_rtd_c_t1 reading unexpected value " + repr(drip.Get('platinum_rtd_c_t1'))
    except KeyError:
        print "platinum_rtd_c_t1 not responding"
    except:
        print "platinum_rtd_c_t1 unexpected error:", sys.exc_info()[0]
except:
    print "platinum_rtd_c_t1 unexpected error:", sys.exc_info()[0]
        
try:
    if drip.Get('platinum_rtd_c_t2')['final'][0] == '-':
        print "platinum_rtd_c_t2 reading negative temperature " + repr(drip.Get('platinum_rtd_c_t2'))
    elif drip.Get('platinum_rtd_c_t2')['final'][0] == '+':
        print "platinum_rtd_c_t2 ok " + repr(drip.Get('platinum_rtd_c_t2'))
    else:
        print "platinum_rtd_c_t2 reading unexpected value " + repr(drip.Get('platinum_rtd_c_t2'))
except KeyError:
    try:
        if drip.Get('platinum_rtd_c_t2')['final'][0] == '-':
            print "platinum_rtd_c_t2 reading negative temperature " + repr(drip.Get('platinum_rtd_c_t2'))
        elif drip.Get('platinum_rtd_c_t2')['final'][0] == '+':
            print "platinum_rtd_c_t2 ok " + repr(drip.Get('platinum_rtd_c_t2'))
        else:
            print "platinum_rtd_c_t2 reading unexpected value " + repr(drip.Get('platinum_rtd_c_t2'))
    except KeyError:
        print "platinum_rtd_c_t2 not responding"
    except:
        print "platinum_rtd_c_t2 unexpected error:", sys.exc_info()[0]
except:
    print "platinum_rtd_c_t2 unexpected error:", sys.exc_info()[0]
        
try:
    if drip.Get('platinum_rtd_c_t3')['final'][0] == '-':
        print "platinum_rtd_c_t3 reading negative temperature " + repr(drip.Get('platinum_rtd_c_t3'))
    elif drip.Get('platinum_rtd_c_t3')['final'][0] == '+':
        print "platinum_rtd_c_t3 ok " + repr(drip.Get('platinum_rtd_c_t3'))
    else:
        print "platinum_rtd_c_t3 reading unexpected value " + repr(drip.Get('platinum_rtd_c_t3'))
except KeyError:
    try:
        if drip.Get('platinum_rtd_c_t3')['final'][0] == '-':
            print "platinum_rtd_c_t3 reading negative temperature " + repr(drip.Get('platinum_rtd_c_t3'))
        elif drip.Get('platinum_rtd_c_t3')['final'][0] == '+':
            print "platinum_rtd_c_t3 ok " + repr(drip.Get('platinum_rtd_c_t3'))
        else:
            print "platinum_rtd_c_t3 reading unexpected value " + repr(drip.Get('platinum_rtd_c_t3'))
    except KeyError:
        print "platinum_rtd_c_t3 not responding"
    except:
        print "platinum_rtd_c_t3 unexpected error:", sys.exc_info()[0]
except:
    print "platinum_rtd_c_t3 unexpected error:", sys.exc_info()[0]
        
try:
    if drip.Get('platinum_rtd_c_t4')['final'][0] == '-':
        print "platinum_rtd_c_t4 reading negative temperature " + repr(drip.Get('platinum_rtd_c_t4'))
    elif drip.Get('platinum_rtd_c_t4')['final'][0] == '+':
        print "platinum_rtd_c_t4 ok " + repr(drip.Get('platinum_rtd_c_t4'))
    else:
        print "platinum_rtd_c_t4 reading unexpected value " + repr(drip.Get('platinum_rtd_c_t4'))
except KeyError:
    try:
        if drip.Get('platinum_rtd_c_t4')['final'][0] == '-':
            print "platinum_rtd_c_t4 reading negative temperature " + repr(drip.Get('platinum_rtd_c_t4'))
        elif drip.Get('platinum_rtd_c_t4')['final'][0] == '+':
            print "platinum_rtd_c_t4 ok " + repr(drip.Get('platinum_rtd_c_t4'))
        else:
            print "platinum_rtd_c_t4 reading unexpected value " + repr(drip.Get('platinum_rtd_c_t4'))
    except KeyError:
        print "platinum_rtd_c_t4 not responding"
    except:
        print "platinum_rtd_c_t4 unexpected error:", sys.exc_info()[0]
except:
    print "platinum_rtd_c_t4 unexpected error:", sys.exc_info()[0]
    
# ====================== Check Pump Valve Temperature =====================
try:
    if drip.Get('pump_valve_t')['final'][0] == '-':
        print "pump_valve_t reading negative temperature " + repr(drip.Get('pump_valve_t'))
    elif drip.Get('pump_valve_t')['final'][0] == '+':
        print "pump_valve_t ok " + repr(drip.Get('pump_valve_t'))
    else:
        print "pump_valve_t reading unexpected value " + repr(drip.Get('pump_valve_t'))
except KeyError:
    try:
        if drip.Get('pump_valve_t')['final'][0] == '-':
            print "pump_valve_t reading negative temperature " + repr(drip.Get('pump_valve_t'))
        elif drip.Get('pump_valve_t')['final'][0] == '+':
            print "pump_valve_t ok " + repr(drip.Get('pump_valve_t'))
        else:
            print "pump_valve_t reading unexpected value " + repr(drip.Get('pump_valve_t'))
    except KeyError:
        print "pump_valve_t not responding"
    except:
        print "pump_valve_t unexpected error:", sys.exc_info()[0]
except:
    print "pump_valve_t unexpected error:", sys.exc_info()[0]

# ====================== Check Vent Valve Temperature =====================
try:
    if drip.Get('vent_valve_t')['final'][0] == '-':
        print "vent_valve_t reading negative temperature " + repr(drip.Get('vent_valve_t'))
    elif drip.Get('vent_valve_t')['final'][0] == '+':
        print "vent_valve_t ok " + repr(drip.Get('vent_valve_t'))
    else:
        print "vent_valve_t reading unexpected value " + repr(drip.Get('vent_valve_t'))
except KeyError:
    try:
        if drip.Get('vent_valve_t')['final'][0] == '-':
            print "vent_valve_t reading negative temperature " + repr(drip.Get('vent_valve_t'))
        elif drip.Get('vent_valve_t')['final'][0] == '+':
            print "vent_valve_t ok " + repr(drip.Get('vent_valve_t'))
        else:
            print "vent_valve_t reading unexpected value " + repr(drip.Get('vent_valve_t'))
    except KeyError:
        print "vent_valve_t not responding"
    except:
        print "vent_valve_t unexpected error:", sys.exc_info()[0]
except:
    print "vent_valve_t unexpected error:", sys.exc_info()[0]
