# This is a script designed to show how to create a simple plot and make a basic
# fit. Because of the nature of some of the commands, it cannot be run as a
# script and must instead be entered into the python interpreter line by line

# The first step is to import pypeline. pypeline contains all the different
# classes used to interact with CouchDB and dripline.
import pypeline

# You can get more information about what is located in this package by asking
# for help: help(pypeline)

# The next step is to create an instance of LoggedDataHandler. It needs the URL
# of Couch database to create the object.
logg = pypeline.LoggedDataHandler('http://p8portal.phys.washington.edu:5984')

# You can also ask for help from logg to get the help file for the
# LoggedDataHandler class: help(logg)

# If you ask for a plot with no arguments, pypeline will give you a list of all
# loggers with data from the last 3 hours.
logg.Plot()

# You can then create a plot of one from that list.
logg.Plot('right_gas_line_upper_t')
# The plot opens as dynamically updating by default. If you want to close it,
# you need to type Ctrl-C in the terminal, and then close the plot.

# If you want to change the time limits, you can pass arguments to the "start"
# and "stop" variables. These can accept python datetime objects or CouchDB
# formatted timestamps.
logg.Plot('right_gas_line_upper_t', start='2012-09-06 10:00:00',
          stop='2012-09-06 11:00:00')

# You can also fit data to an arbitrary function. A linear fit is attemped by
# default.
logg.Fit('right_gas_line_upper_t')

# An exponential fit can also be used with the keyword 'exponential'.
logg.Fit('right_gas_line_upper_t','exponential')

# Finally, an arbitrary function can be specified in the following manner:
func = lambda p, x: p[0] + p[1]*x + p[2]*x**2
p0 = [0, 1, 1] #You also have to specify a set of guess parameters.
logg.Fit('right_gas_line_upper_t', func, p0)
