import pypeline

pype = pypeline.DripInterface('http://p8portal.phys.washington.edu:5984')
pypeline.scripts.check_pulse.check_pulse(pype)
