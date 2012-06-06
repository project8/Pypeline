#!/usr/bin/python3

import Pypeline

pype = Pypeline.Pypeline('http://p8portal.phys.washington.edu:5984')
print(pype.CheckHeartbeat())
