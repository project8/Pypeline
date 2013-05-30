'''
    This script checks the functionality of all channels in pypeline:

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
# system
import sys
# custom
from pypeline import DripInterface

drip = DripInterface('http://p8portal.phys.washington.edu:5984')


# ================ Check Bore Pressure ===================
val = False
tries = 0
while not val and tries < 2:
    try:
        bore_p = drip.Get('bore_pressure').Wait()['final']
        val = True
        if bore_p[0].isdigit():
            if float(bore_p.split()[0]) < 1000:
                print "bore_pressure ok " + str(bore_p)
            else:
                print "bore_pressure malfunction " + str(bore_p)
        else:
            print "bore_pressure reading unexpected value " + str(bore_p)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "bore_pressure unexpected error", sys.exc_info()[0]
if not val:
    print "bore_pressure not responding"

# ============== Check bypass valve temp =================
val = False
tries = 0
while not val and tries < 2:
    try:
        bypass = drip.Get('bypass_valve_t').Wait()['final']
        val = True
        if bypass[0] == '-':
            print "bypass_valve_t reading negative temperature " + str(bypass)
        elif bypass[0] == '+':
            print "bypass_valve_t ok " + str(bypass)
        else:
            print "bypass_valve_t reading unexpected value " + str(bypass)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "bypass_valve_t unexpected error:", sys.exc_info()[0]
if not val:
    print "bypass_valve_t not responding"

# =========== Check cernox temperature sensors on cable A ================
val = False
tries = 0
while not val and tries < 2:
    try:
        cernox1 = drip.Get('cernox_a_t1').Wait()['final']
        val = True
        if cernox1[0].isdigit():
            print "cernox_a_t1 ok " + str(cernox1)
        else:
            print "cernox_a_t1 reading unexpected value " + str(cernox1)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "cernox_a_t1 unexpected error:", sys.exc_info()[0]
if not val:
    print "cernox_a_t1 not responding"

val = False
tries = 0
while not val and tries < 2:
    try:
        cernox2 = drip.Get('cernox_a_t2').Wait()['final']
        val = True
        if cernox2[0].isdigit():
            print "cernox_a_t2 ok " + str(cernox2)
        else:
            print "cernox_a_t2 reading unexpected value " + str(cernox2)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "cernox_a_t2 unexpected error:", sys.exc_info()[0]
if not val:
    print "cernox_a_t2 not responding"

val = False
tries = 0
while not val and tries < 2:
    try:
        cernox3 = drip.Get('cernox_a_t3').Wait()['final']
        val = True
        if cernox3[0].isdigit():
            print "cernox_a_t3 ok " + str(cernox3)
        else:
            print "cernox_a_t3 reading unexpected value " + str(cernox3)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "cernox_a_t3 unexpected error:", sys.exc_info()[0]
if not val:
    print "cernox_a_t3 not responding"

val = False
tries = 0
while not val and tries < 2:
    try:
        cernox4 = drip.Get('cernox_a_t4').Wait()['final']
        val = True
        if cernox4[0].isdigit():
            print "cernox_a_t4 ok " + str(cernox4)
        else:
            print "cernox_a_t4 reading unexpected value " + str(cernox4)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "cernox_a_t4 unexpected error:", sys.exc_info()[0]
if not val:
    print "cernox_a_t4 not responding"

# ============== Check getter valve temp =================
val = False
tries = 0
while not val and tries < 2:
    try:
        getter = drip.Get('getter_valve_t').Wait()['final']
        val = True
        if getter[0] == '-':
            print "getter_valve_t reading negative temperature " + str(getter)
        elif getter[0] == '+':
            print "getter_valve_t ok " + str(getter)
        else:
            print "getter_valve_t reading unexpected value " + str(getter)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "getter_valve_t unexpected error:", sys.exc_info()[0]
if not val:
    print "getter_valve_t not responding"

# =========================== Check Hall Probe ================================
val = False
tries = 0
while not val and tries < 2:
    try:
        hall = drip.Get('hall_probe_voltage').Wait()['final']
        val = True
        if hall[0] == '-':
            print "hall_probe_voltage reading negative voltage " + str(hall)
        elif hall[0] == '+':
            print "hall_valve_t ok " + str(hall)
        else:
            print "hall_probe_voltage reading unexpected value " + str(hall)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "hall_probe_voltage unexpected error:", sys.exc_info()[0]
if not val:
    print "hall_probe_voltage not responding"

# ========================= Check high frequency ==============================
val = False
tries = 0
while not val and tries < 2:
    try:
        drip.Set('hf_cw_freq', '25000')
        hf_cw = int(drip.Get('hf_cw_freq').Wait()['final'])
        val = True
        if hf_cw != 25000000000:
            print "error setting hf_cw_freq to 25 GHz " + str(hf_cw)
        else:
            print "hf_cw_freq ok " + str(hf_cw)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "hf_cw_freq unexpected error:", sys.exc_info()[0]
if not val:
    print "hf_cw_freq not responding"

val = False
tries = 0
while not val and tries < 2:
    try:
        drip.Set('hf_sweep_start', '24000')
        hf_sweep_start = int(drip.Get('hf_sweep_start').Wait()['final'])
        val = True
        if hf_sweep_start != 24000000000:
            print "error setting hf_sweep_start to 24 GHz " + str(hf_sweep_start)
        else:
            print "hf_sweep_start ok " + str(hf_sweep_start)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "hf_sweep start unexpected error:", sys.exc_info()[0]
if not val:
    print "hf_sweep_start not responding"

val = False
tries = 0
while not val and tries < 2:
    try:
        drip.Set('hf_sweep_stop', '25000')
        hf_sweep_stop = int(drip.Get('hf_sweep_stop').Wait()['final'])
        val = True
        if hf_sweep_stop != 25000000000:
            print "error setting hf_sweep_stop to 25 GHz " + str(hf_sweep_stop)
        else:
            print "hf_sweep_stop ok " + str(hf_sweep_stop)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "hf_sweep_stop unexpected error:", sys.exc_info()[0]
if not val:
    print "hf_sweep_stop not responding"

val = False
tries = 0
while not val and tries < 2:
    try:
        drip.Set('hf_sweep_time', '1000')
        hf_sweep_time = float(drip.Get('hf_sweep_time').Wait()['final'])
        val = True
        if hf_sweep_time != 1:
            print "error setting hf_sweep_time to 1000 ms " + str(hf_sweep_time)
        else:
            print "hf_sweep_time ok " + str(hf_sweep_time)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "hf_sweep_time unexpected error:", sys.exc_info()[0]
if not val:
    print "hf_sweep_time not responding"

val = False
tries = 0
while not val and tries < 2:
    try:
        drip.Set('hf_sweeper_power', '-40')
        hf_sweeper_power = float(drip.Get('hf_sweeper_power').Wait()['final'])
        val = True
        if hf_sweeper_power != -40:
            print "error setting hf_sweeper_power to -40 dB " + str(hf_sweeper_power)
        else:
            print "hf_sweeper_power ok " + str(hf_sweeper_power)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "hf_sweeper_power unexpected error:", sys.exc_info()[0]
if not val:
    print "hf_sweeper_power not responding"

# ======================== Check Ignatius Data Disk =======================
val = False
tries = 0
while not val and tries < 2:
    try:
        data = drip.Get('ignatius_data_disk').Wait()['final']
        print "ignatius_data_disk ok " + '\n' + str(data)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "ignatius_data_disk unexpected error", sys.exc_info()[0]
if not val:
    print "ignatius_data_disk not responding"

# ========================= Check Inlet Pressure ==========================
val = False
tries = 0
while not val and tries < 2:
    try:
        inlet_p = drip.Get('inlet_pressure').Wait()['final']
        val = True
        if inlet_p[0].isdigit():
            if float(inlet_p.split()[0]) < 1000:
                print "inlet_pressure ok " + str(inlet_p)
            else:
                print "inlet_pressure malfunction " + str(inlet_p)
        else:
            print "inlet_pressure reading unexpected value " + str(inlet_p)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "inlet_pressure unexpected error", sys.exc_info()[0]
if not val:
    print "inlet_pressure not responding"

# ========================= Check Linear Encoder ==========================
val = False
tries = 0
while not val and tries < 2:
    try:
        linenc = drip.Get('linear_encoder').Wait()['final']
        val = True
        if linenc[0].isdigit():
            print "linear_encoder ok " + str(linenc)
        else:
            print "linear_encoder reading unexpected value " + str(linenc)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "linear_encoder unexpected error:", sys.exc_info()[0]
if not val:
    print "linear_encoder not responding"

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
val = False
tries = 0
while not val and tries < 2:
    try:
        outlet_p = drip.Get('outlet_pressure').Wait()['final']
        val = True
        if outlet_p[0].isdigit():
            if float(outlet_p.split()[0]) < 1000:
                print "outlet_pressure ok " + str(outlet_p)
            else:
                print "outlet_pressure malfunction " + str(outlet_p)
        else:
            print "outlet_pressure reading unexpected value " + str(outlet_p)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "outlet_pressure unexpected error", sys.exc_info()[0]
if not val:
    print "outlet_pressure not responding"

# ======================== Check p8portal Root Disk =======================
val = False
tries = 0
while not val and tries < 2:
    try:
        root = drip.Get('p8portal_root_disk').Wait()['final']
        print "p8portal ok " + '\n' + str(root)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "p8portal_root_disk unexpected error", sys.exc_info()[0]
if not val:
    print "p8portal_root_disk not responding"

# ============== Check Pt temperature sensors on cable C ==================
val = False
tries = 0
while not val and tries < 2:
    try:
        pt1 = drip.Get('platinum_rtd_c_t1').Wait()['final']
        val = True
        if pt1[0] == '-':
            print "platinum_rtd_c_t1 reading negative temperature " + str(pt1)
        elif pt1[0] == '+':
            print "platinum_rtd_c_t1 ok " + str(pt1)
        else:
            print "platinum_rtd_c_t1 reading unexpected value " + str(pt1)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "platinum_rtd_c_t1 unexpected error:", sys.exc_info()[0]
if not val:
    print "platinum_rtd_c_t1 not responding"

val = False
tries = 0
while not val and tries < 2:
    try:
        pt2 = drip.Get('platinum_rtd_c_t2').Wait()['final']
        val = True
        if pt2[0] == '-':
            print "platinum_rtd_c_t2 reading negative temperature " + str(pt2)
        elif pt2[0] == '+':
            print "platinum_rtd_c_t2 ok " + str(pt2)
        else:
            print "platinum_rtd_c_t2 reading unexpected value " + str(pt2)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "platinum_rtd_c_t2 unexpected error:", sys.exc_info()[0]
if not val:
    print "platinum_rtd_c_t2 not responding"

val = False
tries = 0
while not val and tries < 2:
    try:
        pt3 = drip.Get('platinum_rtd_c_t3').Wait()['final']
        val = True
        if pt3[0] == '-':
            print "platinum_rtd_c_t3 reading negative temperature " + str(pt3)
        elif pt3[0] == '+':
            print "platinum_rtd_c_t3 ok " + str(pt3)
        else:
            print "platinum_rtd_c_t3 reading unexpected value " + str(pt3)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "platinum_rtd_c_t3 unexpected error:", sys.exc_info()[0]
if not val:
    print "platinum_rtd_c_t3 not responding"

val = False
tries = 0
while not val and tries < 2:
    try:
        pt4 = drip.Get('platinum_rtd_c_t4').Wait()['final']
        val = True
        if pt4[0] == '-':
            print "platinum_rtd_c_t4 reading negative temperature " + str(pt4)
        elif pt4[0] == '+':
            print "platinum_rtd_c_t4 ok " + str(pt4)
        else:
            print "platinum_rtd_c_t4 reading unexpected value " + str(pt4)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "platinum_rtd_c_t4 unexpected error:", sys.exc_info()[0]
if not val:
    print "platinum_rtd_c_t4 not responding"

# ====================== Check Pump Valve Temperature =====================
val = True
tries = 0
while not val and tries < 2:
    try:
        pvt = drip.Get('pump_valve_t').Wait()['final']
        val = True
        if pvt[0] == '-':
            print "pump_valve_t reading negative temperature " + str(pvt)
        elif pvt[0] == '+':
            print "pump_valve_t ok " + str(pvt)
        else:
            print "pump_valve_t reading unexpected value " + str(pvt)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "pump_valve_t unexpected error:", sys.exc_info()[0]
if not val:
    print "pump_valve_t not responding"

# ====================== Check Vent Valve Temperature =====================
val = False
tries = 0
while not val and tries < 2:
    try:
        vvt = drip.Get('vent_valve_t').Wait()['final']
        val = True
        if vvt[0] == '-':
            print "vent_valve_t reading negative temperature " + str(vvt)
        elif vvt[0] == '+':
            print "vent_valve_t ok " + str(vvt)
        else:
            print "vent_valve_t reading unexpected value " + str(vvt)
    except KeyError:
        tries += 1
        continue
    except:
        val = True
        print "vent_valve_t unexpected error:", sys.exc_info()[0]
if not val:
    print "vent_valve_t not responding"
