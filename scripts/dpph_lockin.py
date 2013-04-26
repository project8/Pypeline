from pypeline import DripInterface, dpph_lockin
pype = DripInterface('http://p8portal.phys.washington.edu:5984')
dpph_lockin(pype)
