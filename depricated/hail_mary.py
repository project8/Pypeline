import Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def Pray():
	tFrequencies = []
	tAreasActive = []
	tAreasSuppressed = []

	with open("./dpph_frequencies.txt") as tFrequencyFile:
		for tLine in tFrequencyFile:
			tFrequencies.append(float(tLine))

	with open("./dpph_enabled.txt") as tEnabledFile:
		for tLine in tEnabledFile:
			tAreasActive.append(float(tLine))

	with open("./dpph_suppressed.txt") as tSuppressedFile:
		for tLine in tSuppressedFile:
			tAreasSuppressed.append(float(tLine))

	tAreasCompared = [ (tAreasActive[tIndex] - tAreasSuppressed[tIndex])/tAreasSuppressed[tIndex] for tIndex in range( len( tFrequencies ) ) ]

	tPlotWindow = Tkinter.Toplevel()
	tPlotWindow.title( "p8 dpph raw display" )
	tPlotWindow.grid()        
	tFigure = Figure()
	tAxes = tFigure.add_subplot( 1, 1, 1 )
	tLine, = tAxes.plot( tFrequencies, tAreasSuppressed, "bo" )
	tLine, = tAxes.plot( tFrequencies, tAreasActive, "ro" )
	tCanvas = FigureCanvasTkAgg( tFigure, master = tPlotWindow )
	tCanvas.show()
	tCanvas.get_tk_widget().grid( column = 0, row = 1 )

	tPlotWindow = Tkinter.Toplevel()
	tPlotWindow.title( "p8 dpph subtracted display" )
	tPlotWindow.grid()        
	tFigure = Figure()
	tAxes = tFigure.add_subplot( 1, 1, 1 )
	tLine, = tAxes.plot( tFrequencies, tAreasCompared, "go" )
	tCanvas = FigureCanvasTkAgg( tFigure, master = tPlotWindow )
	tCanvas.show()
	tCanvas.get_tk_widget().grid( column = 0, row = 1 )

	return

tWindow = Tkinter.Tk()
tWindow.grid()
tButton = Tkinter.Button( tWindow, text=u"Pray", command = Pray )
tButton.grid( row = 0, column = 0, sticky = "EW" )
tWindow.title( "defiler" )
tWindow.mainloop()