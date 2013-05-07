import DripInterface
import CommandMonitor
import LoggedDataMonitor

import time
import numpy
import scipy
import Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GUI( Tkinter.Tk ):
    def __init__( self, aParent ):
        Tkinter.Tk.__init__( self, aParent )
        
        self.fParent = aParent
        self.InitializePypeline()
        self.InitializeWindow()
	self.olddpph=[]
        self.last_sweep=[]
        
    def InitializePypeline( self ):
        self.fDrip = DripInterface.DripInterface( 'http://p8portal.phys.washington.edu:5984' )
        pass
    
    def InitializeWindow( self ):
        self.grid()
        
        self.InitializeSweeperWidgets()
        self.InitializeOscillatorWidgets()
        self.InitializeDigitizationWidgets()
        
        self.resizable( False, False )
        
    def InitializeSweeperWidgets( self ):
        self.fSweeperLabelText = Tkinter.StringVar()
        self.fSweeperLabelText.set( "sweeper" )        
        self.fSweeperLabel = Tkinter.Label( self, textvariable = self.fSweeperLabelText, anchor = "w", fg = "red", bg = "light gray" )
        self.fSweeperLabel.grid( column = 0, row = 0, sticky = "EW" )

        self.fSweeperPowerLabelText = Tkinter.StringVar()
        self.fSweeperPowerLabelText.set( "power [dBm]" )
        self.fSweeperPowerLabel = Tkinter.Label( self, textvariable = self.fSweeperPowerLabelText, anchor = "w", fg = "black", bg = "light gray" )
        self.fSweeperPowerLabel.grid( column = 0, row = 1, sticky = "EW" )        
        self.fSweeperPowerEntryText = Tkinter.StringVar()
        self.fSweeperPowerEntryText.set( "-30" )
        self.fSweeperPowerEntry = Tkinter.Entry( self, textvariable = self.fSweeperPowerEntryText )
        self.fSweeperPowerEntry.grid( column = 1, row = 1, sticky = "EW" )

        self.fSweeperPowerButton = Tkinter.Button( self, text = u"set power", command = self.SetSweeperPower )
        self.fSweeperPowerButton.grid( column = 2, row = 1, sticky = "EW" )
        
        self.fSweeperCenterFrequencyLabelText = Tkinter.StringVar()
        self.fSweeperCenterFrequencyLabelText.set( "center frequency [MHz]" )
        self.fSweeperCenterFrequencyLabel = Tkinter.Label( self, textvariable = self.fSweeperCenterFrequencyLabelText, anchor = "w", fg = "black", bg = "light gray" )
        self.fSweeperCenterFrequencyLabel.grid( column = 0, row = 2, sticky = "EW" )        
        self.fSweeperCenterFrequencyEntryText = Tkinter.StringVar()
        self.fSweeperCenterFrequencyEntryText.set( "25550" )        
        self.fSweeperCenterFrequencyEntry = Tkinter.Entry( self, textvariable = self.fSweeperCenterFrequencyEntryText )
        self.fSweeperCenterFrequencyEntry.grid( column = 1, row = 2, sticky = "EW" )
        
        self.fSweeperStaticModeButton = Tkinter.Button( self, text = u"set static mode", command = self.SetSweeperStaticMode )
        self.fSweeperStaticModeButton.grid( column = 2, row = 2, sticky = "EW" )
        
        self.fSweeperStartFrequencyLabelText = Tkinter.StringVar()
        self.fSweeperStartFrequencyLabelText.set( "start frequency [MHz]" )
        self.fSweeperStartFrequencyLabel = Tkinter.Label( self, textvariable = self.fSweeperStartFrequencyLabelText, anchor = "w", fg = "black", bg = "light gray" )
        self.fSweeperStartFrequencyLabel.grid( column = 0, row = 3, sticky = "EW" )        
        self.fSweeperStartFrequencyEntryText = Tkinter.StringVar()
        self.fSweeperStartFrequencyEntryText.set( "(unset)" )        
        self.fSweeperStartFrequencyEntry = Tkinter.Entry( self, textvariable = self.fSweeperStartFrequencyEntryText )
        self.fSweeperStartFrequencyEntry.grid( column = 1, row = 3, sticky = "EW" )
        
        self.fSweeperStopFrequencyLabelText = Tkinter.StringVar()
        self.fSweeperStopFrequencyLabelText.set( "stop frequency [MHz]" )
        self.fSweeperStopFrequencyLabel = Tkinter.Label( self, textvariable = self.fSweeperStopFrequencyLabelText, anchor = "w", fg = "black", bg = "light gray" )
        self.fSweeperStopFrequencyLabel.grid( column = 0, row = 4, sticky = "EW" )        
        self.fSweeperStopFrequencyEntryText = Tkinter.StringVar()
        self.fSweeperStopFrequencyEntryText.set( "(unset)" )        
        self.fSweeperStopFrequencyEntry = Tkinter.Entry( self, textvariable = self.fSweeperStopFrequencyEntryText )
        self.fSweeperStopFrequencyEntry.grid( column = 1, row = 4, sticky = "EW" )
        
        self.fSweeperSweepTimeLabelText = Tkinter.StringVar()
        self.fSweeperSweepTimeLabelText.set( "sweep time [ms]" )
        self.fSweeperSweepTimeLabel = Tkinter.Label( self, textvariable = self.fSweeperSweepTimeLabelText, anchor = "w", fg = "black", bg = "light gray" )
        self.fSweeperSweepTimeLabel.grid( column = 0, row = 5, sticky = "EW" )        
        self.fSweeperSweepTimeEntryText = Tkinter.StringVar()
        self.fSweeperSweepTimeEntryText.set( "(unset)" )        
        self.fSweeperSweepTimeEntry = Tkinter.Entry( self, textvariable = self.fSweeperSweepTimeEntryText )
        self.fSweeperSweepTimeEntry.grid( column = 1, row = 5, sticky = "EW" )
        
        self.fSweeperSweepingModeButton = Tkinter.Button( self, text = u"set sweeping mode", command = self.SetSweeperSweepingMode )
        self.fSweeperSweepingModeButton.grid( column = 2, row = 5, sticky = "EW" )
        
    def InitializeOscillatorWidgets( self ):
        self.fOscillatorLabelText = Tkinter.StringVar()
        self.fOscillatorLabelText.set( "oscillator" )        
        self.fOscillatorLabel = Tkinter.Label( self, textvariable = self.fOscillatorLabelText, anchor = "w", fg = "red", bg = "light gray" )
        self.fOscillatorLabel.grid( column = 0, row = 6, sticky = "EW" )
        
        self.fOscillatorFrequencyLabelText = Tkinter.StringVar()
        self.fOscillatorFrequencyLabelText.set( "oscillator frequency [MHz]" )
        self.fOscillatorFrequencyLabel = Tkinter.Label( self, textvariable = self.fOscillatorFrequencyLabelText, anchor = "w", fg = "black", bg = "light gray" )
        self.fOscillatorFrequencyLabel.grid( column = 0, row = 7, sticky = "EW" )        
        self.fOscillatorFrequencyEntryText = Tkinter.StringVar()
        self.fOscillatorFrequencyEntryText.set( "1000" )
        self.fOscillatorFrequencyEntry = Tkinter.Entry( self, textvariable = self.fOscillatorFrequencyEntryText )
        self.fOscillatorFrequencyEntry.grid( column = 1, row = 7, sticky = "EW" )
        
        self.fOscillatorFrequencyButton = Tkinter.Button( self, text = u"set oscillator frequency", command = self.SetOscillatorFrequency )
        self.fOscillatorFrequencyButton.grid( column = 2, row = 7, sticky = "EW" )
        
    def InitializeDigitizationWidgets( self ):
        self.fDigitizationLabelText = Tkinter.StringVar()
        self.fDigitizationLabelText.set( "digitization" )        
        self.fDigitizationLabel = Tkinter.Label( self, textvariable = self.fDigitizationLabelText, anchor = "w", fg = "red", bg = "light gray" )
        self.fDigitizationLabel.grid( column = 0, row = 8, sticky = "EW" )
        
        self.fDigitizationRateLabelText = Tkinter.StringVar()
        self.fDigitizationRateLabelText.set( "digitization rate [MHz]" )
        self.fDigitizationRateLabel = Tkinter.Label( self, textvariable = self.fDigitizationRateLabelText, anchor = "w", fg = "black", bg = "light gray" )
        self.fDigitizationRateLabel.grid( column = 0, row = 9, sticky = "EW" )        
        self.fDigitizationRateEntryText = Tkinter.StringVar()
        self.fDigitizationRateEntryText.set( "200" )
        self.fDigitizationRateEntry = Tkinter.Entry( self, textvariable = self.fDigitizationRateEntryText )
        self.fDigitizationRateEntry.grid( column = 1, row = 9, sticky = "EW" )
        
        self.fDigitizationDurationLabelText = Tkinter.StringVar()
        self.fDigitizationDurationLabelText.set( "digitization duration [ms]" )
        self.fDigitizationDurationLabel = Tkinter.Label( self, textvariable = self.fDigitizationDurationLabelText, anchor = "w", fg = "black", bg = "light gray" )
        self.fDigitizationDurationLabel.grid( column = 0, row = 10, sticky = "EW" )        
        self.fDigitizationDurationEntryText = Tkinter.StringVar()
        self.fDigitizationDurationEntryText.set( "1000" )
        self.fDigitizationDurationEntry = Tkinter.Entry( self, textvariable = self.fDigitizationDurationEntryText )
        self.fDigitizationDurationEntry.grid( column = 1, row = 10, sticky = "EW" )
        
        self.fDigitizationSamplesLabelText = Tkinter.StringVar()
        self.fDigitizationSamplesLabelText.set( "digitization samples [#]" )
        self.fDigitizationSamplesLabel = Tkinter.Label( self, textvariable = self.fDigitizationSamplesLabelText, anchor = "w", fg = "black", bg = "light gray" )
        self.fDigitizationSamplesLabel.grid( column = 0, row = 11, sticky = "EW" )        
        self.fDigitizationSamplesEntryText = Tkinter.StringVar()
        self.fDigitizationSamplesEntryText.set( "32768" )
        self.fDigitizationSamplesEntry = Tkinter.Entry( self, textvariable = self.fDigitizationSamplesEntryText )
        self.fDigitizationSamplesEntry.grid( column = 1, row = 11, sticky = "EW" )
        
        self.fDigitizationPowerSpectrumButton = Tkinter.Button( self, text = u"do spectrum", command = self.DoSpectrum )
        self.fDigitizationPowerSpectrumButton.grid( column = 2, row = 11, sticky = "EW" )
        
        self.fDigitizationNoiseMinLabelText = Tkinter.StringVar()
        self.fDigitizationNoiseMinLabelText.set( "noise min frequency [MHz]" )
        self.fDigitizationNoiseMinLabel = Tkinter.Label( self, textvariable = self.fDigitizationNoiseMinLabelText, anchor = "w", fg = "black", bg = "light gray" )
        self.fDigitizationNoiseMinLabel.grid( column = 0, row = 12, sticky = "EW" )        
        self.fDigitizationNoiseMinEntryText = Tkinter.StringVar()
        self.fDigitizationNoiseMinEntryText.set( "48" )
        self.fDigitizationNoiseMinEntry = Tkinter.Entry( self, textvariable = self.fDigitizationNoiseMinEntryText )
        self.fDigitizationNoiseMinEntry.grid( column = 1, row = 12, sticky = "EW" )
        
        self.fDigitizationNoiseMaxLabelText = Tkinter.StringVar()
        self.fDigitizationNoiseMaxLabelText.set( "noise max frequency [MHz]" )
        self.fDigitizationNoiseMaxLabel = Tkinter.Label( self, textvariable = self.fDigitizationNoiseMaxLabelText, anchor = "w", fg = "black", bg = "light gray" )
        self.fDigitizationNoiseMaxLabel.grid( column = 0, row = 13, sticky = "EW" )        
        self.fDigitizationNoiseMaxEntryText = Tkinter.StringVar()
        self.fDigitizationNoiseMaxEntryText.set( "49" )
        self.fDigitizationNoiseMaxEntry = Tkinter.Entry( self, textvariable = self.fDigitizationNoiseMaxEntryText )
        self.fDigitizationNoiseMaxEntry.grid( column = 1, row = 13, sticky = "EW" )
        
        self.fDigitizationPeakMinLabelText = Tkinter.StringVar()
        self.fDigitizationPeakMinLabelText.set( "peak min frequency [MHz]" )
        self.fDigitizationPeakMinLabel = Tkinter.Label( self, textvariable = self.fDigitizationPeakMinLabelText, anchor = "w", fg = "black", bg = "light gray" )
        self.fDigitizationPeakMinLabel.grid( column = 0, row = 14, sticky = "EW" )        
        self.fDigitizationPeakMinEntryText = Tkinter.StringVar()
        self.fDigitizationPeakMinEntryText.set( "49" )
        self.fDigitizationPeakMinEntry = Tkinter.Entry( self, textvariable = self.fDigitizationPeakMinEntryText )
        self.fDigitizationPeakMinEntry.grid( column = 1, row = 14, sticky = "EW" )
        
        self.fDigitizationPeakMaxLabelText = Tkinter.StringVar()
        self.fDigitizationPeakMaxLabelText.set( "peak max frequency [MHz]" )
        self.fDigitizationPeakMaxLabel = Tkinter.Label( self, textvariable = self.fDigitizationPeakMaxLabelText, anchor = "w", fg = "black", bg = "light gray" )
        self.fDigitizationPeakMaxLabel.grid( column = 0, row = 15, sticky = "EW" )        
        self.fDigitizationPeakMaxEntryText = Tkinter.StringVar()
        self.fDigitizationPeakMaxEntryText.set( "51" )
        self.fDigitizationPeakMaxEntry = Tkinter.Entry( self, textvariable = self.fDigitizationPeakMaxEntryText )
        self.fDigitizationPeakMaxEntry.grid( column = 1, row = 15, sticky = "EW" )
        
        self.fDigitizationPeakWidthLabelText = Tkinter.StringVar()
        self.fDigitizationPeakWidthLabelText.set( "peak width [MHz]" )
        self.fDigitizationPeakWidthLabel = Tkinter.Label( self, textvariable = self.fDigitizationPeakWidthLabelText, anchor = "w", fg = "black", bg = "light gray" )
        self.fDigitizationPeakWidthLabel.grid( column = 0, row = 16, sticky = "EW" )        
        self.fDigitizationPeakWidthEntryText = Tkinter.StringVar()
        self.fDigitizationPeakWidthEntryText.set( "0.5" )
        self.fDigitizationPeakWidthEntry = Tkinter.Entry( self, textvariable = self.fDigitizationPeakWidthEntryText )
        self.fDigitizationPeakWidthEntry.grid( column = 1, row = 16, sticky = "EW" )
        
        self.fDigitizationPowerSpectrumButton = Tkinter.Button( self, text = u"do peak", command = self.DoPeak )
        self.fDigitizationPowerSpectrumButton.grid( column = 2, row = 16, sticky = "EW" )
        
        #self.fDPPHButton = Tkinter.Button( self, text = u"do dpph", command = self.DoDPPH )
        #self.fDPPHButton = Tkinter.Button( self, text = u"do dpph", command = self.DoDPPHbg )
        self.fDPPHButton = Tkinter.Button( self, text = u"do dpph", command = self.DoDPPHsweep )
        self.fDPPHButton.grid( column = 2, row = 17, sticky = "EW" )

    def SetSweeperPower( self ):
        print( "setting power..." )
        self.fDrip.Set( "hf_sweeper_power", self.fSweeperPowerEntryText.get(), True )
        print( "ready." )
    
    def SetSweeperStaticMode( self ):
        print( "setting frequency..." )
        self.fDrip.Set( "hf_cw_freq", self.fSweeperCenterFrequencyEntryText.get(), True )
        print( "ready." )
        
    def SetSweeperSweepingMode( self ):
        print( "setting frequencies..." )
        self.fDrip.Set( "hf_sweep_start", self.fSweeperStartFrequencyEntryText.get(), True )
        self.fDrip.Set( "hf_sweep_stop", self.fSweeperStopFrequencyEntryText.get(), True )
        self.fDrip.Set( "hf_sweep_time", self.fSweeperSweepTimeEntryText.get(), True )
        print( "ready." )
        
    def SetOscillatorFrequency( self ) :
        print( "setting frequency..." )
        self.fDrip.Set( "lo_cw_freq", self.fOscillatorFrequencyEntryText.get(), True )
        print( "ready." )

    def DoSpectrum( self ):
        print( "running mantis..." )
        tMantisOut = self.fDrip.RunMantis( output = "/data/temp_gui_digitization.egg", rate = self.fDigitizationRateEntryText.get(), duration = self.fDigitizationDurationEntryText.get(), mode = 1, length = 4194304, count = 640 ).Wait( 60 )["result"]
        print( "running powerline..." )
        tPowerlineOut = eval( self.fDrip.RunPowerline( points = self.fDigitizationSamplesEntryText.get(), events = 8192, input = "/data/temp_gui_digitization.egg" ).Wait( 60 )["result"] )
        tSamplingRate = tPowerlineOut["sampling_rate"]
        tYData = tPowerlineOut["data"]
        tLength = len( tYData )
        tXData = [ tSamplingRate * tVariable / ( 2.0 * tLength ) for tVariable in range( tLength ) ]

        tPeakMin = float( self.fDigitizationPeakMinEntryText.get() )
        tPeakMax = float( self.fDigitizationPeakMaxEntryText.get() )
        if tPeakMax < tPeakMin:
            print( "error: peak max frequency is less than peak min frequency" )
            return
        
        tXToPlot = []
        tYToPlot = []
        for tIndex in range( len( tYData ) ):
            if tXData[tIndex] > tPeakMin:
                if tXData[tIndex] < tPeakMax:
                    tXToPlot.append( tXData[tIndex] )
                    tYToPlot.append( tYData[tIndex] )
                
        print( "plotting..." )        
        tPlotWindow = Tkinter.Toplevel()
        tPlotWindow.title( "p8 power spectrum" )
        tPlotWindow.grid()        
        tFigure = Figure()
        tAxes = tFigure.add_subplot( 1, 1, 1 )
        tLine, = tAxes.plot( tXToPlot, tYToPlot, "ro" )
        tCanvas = FigureCanvasTkAgg( tFigure, master = tPlotWindow )
        tCanvas.show()
        tCanvas.get_tk_widget().grid( column = 0, row = 1 )
        print( "ready." )
        
    def DoPeak( self ):
        
        # check that inputs make sense
        
        tNoiseMin = float( self.fDigitizationNoiseMinEntryText.get() )
        tNoiseMax = float( self.fDigitizationNoiseMaxEntryText.get() )
        if tNoiseMax < tNoiseMin:
            print( "error: noise max frequency is less than noise min frequency" )
            return
        
        tPeakMin = float( self.fDigitizationPeakMinEntryText.get() )
        tPeakMax = float( self.fDigitizationPeakMaxEntryText.get() )
        if tPeakMax < tPeakMin:
            print( "error: peak max frequency is less than peak min frequency" )
            return
        
        tPeakWidth = float( self.fDigitizationPeakWidthEntryText.get() ) / 2.
        if tPeakWidth < 0.0:
            print( "error: peak width is less than zero" )
            return       
        
        # calculate the power spectrum
            
        print( "running mantis..." )
        tMantisOut = self.fDrip.RunMantis( output = "/data/temp_gui_digitization.egg", rate = self.fDigitizationRateEntryText.get(), duration = self.fDigitizationDurationEntryText.get(), mode = 1, length = 4194304, count = 640 ).Wait( 60 )["result"]
        print( "running powerline..." )
        tPowerlineOut = eval( self.fDrip.RunPowerline( points = self.fDigitizationSamplesEntryText.get(), events = 1024, input = "/data/temp_gui_digitization.egg" ).Wait( 60 )["result"] )
        tSamplingRate = tPowerlineOut["sampling_rate"]
        tYData = tPowerlineOut["data"]
        tLength = len( tYData )
        tXData = [ tSamplingRate * tVariable / ( 2.0 * tLength ) for tVariable in range( tLength ) ]
        
        # figure out the peak parameters
        
        tPeakPower = -1000.0
        tPeakFrequency = 0.0
        tPeakIndex = -1
        for tIndex in range( tLength ):
            if tXData[tIndex] > tPeakMin:
                if tXData[tIndex] < tPeakMax:
                    if tYData[tIndex] > tPeakPower:
                        tPeakPower = tYData[tIndex]
                        tPeakFrequency = tXData[tIndex]
                        tPeakIndex = tIndex
        
        # figure out noise parameters
        
        tNoise = []
        for tIndex in range( tLength ):
            if tXData[tIndex] > tNoiseMin:
                if tXData[tIndex] < tNoiseMax:
                    tNoise.append( tYData[tIndex] )
        tNoisePower = numpy.mean( tNoise )
        
        # just sum the area

        tArea = 0.
        for tIndex in range( -4, 5 ):
            tArea = tArea + ( tYData[tPeakIndex + tIndex] - tNoisePower )
        
        #summarize
            
        print( "peak power was {0} at {1} MHz in bin {2} with area {3} on noise of {4}" ).format( tPeakPower, tPeakFrequency, tPeakIndex, tArea, tNoisePower )
        
        return

    def DoDPPH( self ):        
        
        print( "starting in two seconds..." )
        time.sleep( 2 )
                
        tStartFreq = 24900.
        tEndFreq = 26100.
        tDeltaFreq = 2.
        
        tDigRate = 200.
        tDigDuration = 1000
        tDigPoints = 32768
        tDigAverages = 4096
        
        tNoiseMin = 48.
        tNoiseMax = 49.
        tPeakMin = 49.
        tPeakMax = 51. 
        
        tInternalFreq = 24500.       
        tTargetFreq = 50.
        
        tFrequencies = []
        tAreasActive = []
        tAreasSuppressed = []
        tAreasCompared = []
        
        #################
        # activate dpph #
        #################

        self.fDrip.Set( "dpph_current", "0A", True )
        time.sleep( 1000 )

        tCurrentHighFreq = tStartFreq
        tCurrentLowFreq = tStartFreq - tInternalFreq - tTargetFreq
        while tCurrentHighFreq <= tEndFreq:
            
            print( "analyzing at {0} MHz with oscillator at {1} MHz" ).format( tCurrentHighFreq, tCurrentLowFreq )
            
            ###################
            # set oscillators #
            ###################
            
            self.fDrip.Set( "hf_cw_freq", str( tCurrentHighFreq ), True )
            time.sleep( 1 )
            self.fDrip.Set( "hf_sweeper_power", "-50", True )
            time.sleep( 1 )
            self.fDrip.Set( "hf_sweeper_power", "-35", True )
            time.sleep( 1 )
            self.fDrip.Set( "lo_cw_freq", str( tCurrentLowFreq ), True )           
            
            # calculate the power spectrum
            
            print( "running mantis..." )
            
            while True:
                tMantisOut = self.fDrip.RunMantis( output = "/data/temp_gui_digitization.egg", rate = tDigRate, duration = tDigDuration, mode = "1", length = "4194304", count = "48" ).Wait( 60 )
                try:
                    tDecider = tMantisOut["result"]
                    break
                except KeyError:
                    print( "mantis barfed..." )
                    print( tMantisOut )

            print( "running powerline..." )
            
            tPowerlineOut = eval( self.fDrip.RunPowerline( points = tDigPoints, events = tDigAverages, input = "/data/temp_gui_digitization.egg" ).Wait( 60 )["result"] )
            tSamplingRate = tPowerlineOut["sampling_rate"]
            tYData = tPowerlineOut["data"]
            tLength = len( tYData )
            tXData = [ tSamplingRate * tVariable / ( 2.0 * tLength ) for tVariable in range( tLength ) ]
            
            # figure out the peak parameters
            
            tPeakPower = -1000.0
            tPeakFrequency = 0.0
            tPeakIndex = -1
            for tIndex in range( tLength ):
                if tXData[tIndex] > tPeakMin:
                    if tXData[tIndex] < tPeakMax:
                        if tYData[tIndex] > tPeakPower:
                            tPeakPower = tYData[tIndex]
                            tPeakFrequency = tXData[tIndex]
                            tPeakIndex = tIndex
            
            # figure out noise parameters
            
            tNoise = []
            for tIndex in range( tLength ):
                if tXData[tIndex] > tNoiseMin:
                    if tXData[tIndex] < tNoiseMax:
                        tNoise.append( tYData[tIndex] )
            tNoisePower = numpy.mean( tNoise )
            
            # just sum the area
    
            tAreaActive = 0.
            for tIndex in range( -4, 5 ):
                tAreaActive = tAreaActive + ( tYData[tPeakIndex + tIndex] - tNoisePower )
            tAreasActive.append( tAreaActive )
            tFrequencies.append( tCurrentHighFreq )
            
            #summarize
            
            print( "enabled peak power was {0} at {1} MHz in bin {2} with area {3} on noise of {4}" ).format( tPeakPower, tPeakFrequency, tPeakIndex, tAreaActive, tNoisePower )
            tCurrentHighFreq = tCurrentHighFreq + tDeltaFreq
            tCurrentLowFreq = tCurrentLowFreq + tDeltaFreq
            

            
        #################
        # suppress dpph #
        #################         
            
        self.fDrip.Set( "dpph_current", "2A", True )
        time.sleep( 1000 )
            
        tCurrentHighFreq = tStartFreq
        tCurrentLowFreq = tStartFreq - tInternalFreq - tTargetFreq
        while tCurrentHighFreq <= tEndFreq:
            
            print( "analyzing at {0} MHz with oscillator at {1} MHz" ).format( tCurrentHighFreq, tCurrentLowFreq )
            
            ###################
            # set oscillators #
            ###################
            
            self.fDrip.Set( "hf_cw_freq", str( tCurrentHighFreq ), True )
            time.sleep( 1 )
            self.fDrip.Set( "hf_sweeper_power", "-50", True )
            time.sleep( 1 )
            self.fDrip.Set( "hf_sweeper_power", "-35", True )
            time.sleep( 1 )
            self.fDrip.Set( "lo_cw_freq", str( tCurrentLowFreq ), True )

            # calculate the power spectrum
            
            print( "running mantis..." )
            
            while True:
                tMantisOut = self.fDrip.RunMantis( output = "/data/temp_gui_digitization.egg", rate = tDigRate, duration = tDigDuration, mode = "1", length = "4194304", count = "48" ).Wait( 60 )
                try:
                    tDecider = tMantisOut["result"]
                    break
                except KeyError:
                    print( "mantis barfed..." )
                    print( tMantisOut )

            print( "running powerline..." )
            
            tPowerlineOut = eval( self.fDrip.RunPowerline( points = tDigPoints, events = tDigAverages, input = "/data/temp_gui_digitization.egg" ).Wait( 60 )["result"] )
            tSamplingRate = tPowerlineOut["sampling_rate"]
            tYData = tPowerlineOut["data"]
            tLength = len( tYData )
            tXData = [ tSamplingRate * tVariable / ( 2.0 * tLength ) for tVariable in range( tLength ) ]
            
            # figure out the peak parameters
            
            tPeakPower = -1000.0
            tPeakFrequency = 0.0
            tPeakIndex = -1
            for tIndex in range( tLength ):
                if tXData[tIndex] > tPeakMin:
                    if tXData[tIndex] < tPeakMax:
                        if tYData[tIndex] > tPeakPower:
                            tPeakPower = tYData[tIndex]
                            tPeakFrequency = tXData[tIndex]
                            tPeakIndex = tIndex
            
            # figure out noise parameters
            
            tNoise = []
            for tIndex in range( tLength ):
                if tXData[tIndex] > tNoiseMin:
                    if tXData[tIndex] < tNoiseMax:
                        tNoise.append( tYData[tIndex] )
            tNoisePower = numpy.mean( tNoise )
            
            # just sum the area
    
            tAreaSuppressed = 0.
            for tIndex in range( -5, 6 ):
                tAreaSuppressed = tAreaSuppressed + ( tYData[tPeakIndex + tIndex] - tNoisePower )
            tAreasSuppressed.append( tAreaSuppressed )
            tAreasCompared.append( (tAreaActive - tAreaSuppressed) / tAreaSuppressed )
            
            # summarize
            
            print( "suppressed peak power was {0} at {1} MHz in bin {2} with area {3} on noise of {4}" ).format( tPeakPower, tPeakFrequency, tPeakIndex, tAreaSuppressed, tNoisePower )
            tCurrentHighFreq = tCurrentHighFreq + tDeltaFreq
            tCurrentLowFreq = tCurrentLowFreq + tDeltaFreq
            
        #now plot results
            
        print( "plotting..." )        
        
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
        tPlotWindow.title( "p8 dpph compared display" )
        tPlotWindow.grid()        
        tFigure = Figure()
        tAxes = tFigure.add_subplot( 1, 1, 1 )
        tLine, = tAxes.plot( tFrequencies, tAreasCompared, "go" )
        tCanvas = FigureCanvasTkAgg( tFigure, master = tPlotWindow )
        tCanvas.show()
        tCanvas.get_tk_widget().grid( column = 0, row = 1 )

        self.fDrip.Set( "dpph_current", "0A", True )
        
        print( "ready." )        
        
        return

    def DoDPPHbg( self ):

        tFrequencies = []
        tAreasActive = []
 
        tStartFreq = 24700.
        tEndFreq = 24900.
        tDeltaFreq = 4.

        tDigRate = 200.
        tNoiseMin = 48.
        tNoiseMax = 49.
        tPeakMin = 49.
        tPeakMax = 51. 
        
        tInternalFreq = 24200.       
        tTargetFreq = 50.
 
        tDigDuration = 1000
        tDigPoints = 32768
        tDigAverages = 4096
        tCurrentHighFreq = tStartFreq
        tCurrentLowFreq = tStartFreq - tInternalFreq - tTargetFreq
        self.fDrip.Set( "hf_sweeper_power", "-75", True )
        while tCurrentHighFreq <= tEndFreq:
            print( "analyzing at {0} MHz with oscillator at {1} MHz" ).format( tCurrentHighFreq, tCurrentLowFreq )
            self.fDrip.Set( "hf_cw_freq", str( tCurrentHighFreq ), True )
            self.fDrip.Set( "lo_cw_freq", str( tCurrentLowFreq ), True )           
            print( "running mantis..." )
            while True:
                tMantisOut = self.fDrip.RunMantis( output = "/data/temp_gui_digitization.egg", rate = tDigRate, duration = tDigDuration, mode = "1", length = "4194304", count = "48" ).Wait( 60 )
                try:
                    tDecider = tMantisOut["result"]
                    break
                except KeyError:
                    print( "mantis barfed..." )
                    print( tMantisOut )

            print( "running powerline..." )
            
            tPowerlineOut = eval( self.fDrip.RunPowerline( points = tDigPoints, events = tDigAverages, input = "/data/temp_gui_digitization.egg" ).Wait( 60 )["result"] )
            tSamplingRate = tPowerlineOut["sampling_rate"]
            tYData = tPowerlineOut["data"]
            tLength = len( tYData )
            tXData = [ tSamplingRate * tVariable / ( 2.0 * tLength ) for tVariable in range( tLength ) ]
            
            # figure out the peak parameters
            
            tPeakPower = -1000.0
            tPeakFrequency = 0.0
            tPeakIndex = -1
            for tIndex in range( tLength ):
                if tXData[tIndex] > tPeakMin:
                    if tXData[tIndex] < tPeakMax:
                        if tYData[tIndex] > tPeakPower:
                            tPeakPower = tYData[tIndex]
                            tPeakFrequency = tXData[tIndex]
                            tPeakIndex = tIndex
            
            # figure out noise parameters
            
            tNoise = []
            for tIndex in range( tLength ):
                if tXData[tIndex] > tNoiseMin:
                    if tXData[tIndex] < tNoiseMax:
                        tNoise.append( tYData[tIndex] )
            tNoisePower = numpy.mean( tNoise )
            
            # just sum the area
    
            tAreaActive = 0.
            for tIndex in range( -4, 5 ):
                tAreaActive = tAreaActive + ( tYData[tPeakIndex + tIndex] - tNoisePower )
            tAreasActive.append( tAreaActive )
            tFrequencies.append( tCurrentHighFreq )
            
            #summarize
            
            print( "enabled peak power was {0} at {1} MHz in bin {2} with area {3} on noise of {4}" ).format( tPeakPower, tPeakFrequency, tPeakIndex, tAreaActive, tNoisePower )
            tCurrentHighFreq = tCurrentHighFreq + tDeltaFreq
            tCurrentLowFreq = tCurrentLowFreq + tDeltaFreq
        print( "plotting..." )        
        
        tPlotWindow = Tkinter.Toplevel()
        tPlotWindow.title( "p8 dpph raw display" )
        tPlotWindow.grid()        
        tFigure = Figure()
        tAxes = tFigure.add_subplot( 1, 1, 1 )
        #tLine, = tAxes.plot( tFrequencies, tAreasSuppressed, "bo" )
        tLine, = tAxes.plot( tFrequencies, tAreasActive, "ro" )
        tCanvas = FigureCanvasTkAgg( tFigure, master = tPlotWindow )
        tCanvas.show()
        tCanvas.get_tk_widget().grid( column = 0, row = 1 )
        
	if len(self.olddpph) != 0:
            tAreasCompared=[]
            for x in range(len(self.olddpph)):
                tAreasCompared.append( (self.olddpph[x]-tAreasActive[x])/(self.olddpph[x]) )
            tPlotWindow = Tkinter.Toplevel()
            tPlotWindow.title( "p8 dpph compared display" )
            tPlotWindow.grid()        
            tFigure = Figure()
            tAxes = tFigure.add_subplot( 1, 1, 1 )
            tLine, = tAxes.plot( tFrequencies, tAreasCompared, "go" )
            tCanvas = FigureCanvasTkAgg( tFigure, master = tPlotWindow )
            tCanvas.show()
            tCanvas.get_tk_widget().grid( column = 0, row = 1 )

	self.olddpph=tAreasActive

        print( "ready." )        
        
        return

    def DoDPPHsweep( self ):

        tFrequencies = []
        tAreasActive = []

 
        tStartFreq = 24700.
        tEndFreq = 24790.
        tDeltaFreq = 80.

        tDigRate = 200.
        tNoiseMin = 48.
        tNoiseMax = 49.
        tPeakMin = 49.
        tPeakMax = 51. 

        
        tInternalFreq = 24200.       
        tTargetFreq = 50.
 
        tDigDuration = 1000
        tDigPoints = 256
        tDigAverages =1048578*4

        trim_points_front=int(tDigPoints*(10.)/tDigRate)
        trim_points_back=int(tDigPoints*(10.)/tDigRate)

        tCurrentHighFreq = tStartFreq
        tCurrentLowFreq = tStartFreq - tInternalFreq - tTargetFreq
        tXDataSet=[]
        tYDataSet=[]

        tPlotWindow = Tkinter.Toplevel()
        tPlotWindow.title( "p8 dpph raw sweep display" )
        tPlotWindow.grid()        
        tFigure = Figure()
        tAxes = tFigure.add_subplot( 1, 1, 1 )
        self.fDrip.Set( "hf_sweeper_power", "-50", True )
        self.fDrip.Set("hf_sweep_time","0.05",True)
        

        while tCurrentHighFreq <= tEndFreq:
            print("analyzing at {0}").format(tCurrentHighFreq);
            tLOFreq=tCurrentHighFreq-tInternalFreq
            self.fDrip.Set("hf_sweep_start",str(tCurrentHighFreq),True);
            self.fDrip.Set("hf_sweep_stop",str(tCurrentHighFreq+100),True);
            print("LO to "+str(tLOFreq))
            self.fDrip.Set( "lo_cw_freq", str(tLOFreq), True )           
            time.sleep(1)
            while True:
                tMantisOut = self.fDrip.RunMantis( output = "/data/temp_gui_digitization.egg", rate = tDigRate, duration = tDigDuration, mode = "1", length = "4194304", count = "48" ).Wait( 60 )
                try:
                    tDecider = tMantisOut["result"]
                    break
                except KeyError:
                    print( "mantis barfed..." )
                    print( tMantisOut )

            print( "running sweepline..." )
            tSweeplineOut = eval( self.fDrip.RunPowerline( points = tDigPoints, events = tDigAverages, input = "/data/temp_gui_digitization.egg" ).Wait( 60 )["result"] )
            tSamplingRate = tSweeplineOut["sampling_rate"]
            tYData = tSweeplineOut["data"]
            tLength = len( tYData )
            tXData = [ tLOFreq+tSamplingRate * tVariable / ( 2.0 * tLength ) for tVariable in range( tLength ) ]
            for i in range(trim_points_front):
                tYData.pop(0)
                tXData.pop(0)
            for i in range(trim_points_back):
                tYData.pop()
                tXData.pop()
            tXDataSet.append(tXData)
            tYDataSet.append(tYData)
            tLine, = tAxes.plot( tXData, tYData, "ro" )
            tCanvas = FigureCanvasTkAgg( tFigure, master = tPlotWindow )
            tCanvas.show()
            tCanvas.get_tk_widget().grid( column = 0, row = 1 )
            tCurrentHighFreq=tCurrentHighFreq+tDeltaFreq
        if len(self.last_sweep)!=0:
            tPlotWindow = Tkinter.Toplevel()
            tPlotWindow.title( "p8 dpph compared display" )
            tPlotWindow.grid()        
            tFigure = Figure()
            tAxes = tFigure.add_subplot( 1, 1, 1 )
            for i in range(len(tYDataSet)):
                dif=[]
                for x in range(len(tYDataSet[i])):
                    dif.append( (tYDataSet[i][x]-self.last_sweep[i][x])/(0.5*(tYDataSet[i][x]+self.last_sweep[i][x])))
                tLine, = tAxes.plot( tXDataSet[i], dif, "go" )
            tCanvas = FigureCanvasTkAgg( tFigure, master = tPlotWindow )
            tCanvas.show()
            tCanvas.get_tk_widget().grid( column = 0, row = 1 )

        self.last_sweep=tYDataSet
        print( "ready." )        
        
        return


