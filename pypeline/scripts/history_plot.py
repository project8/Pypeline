import matplotlib
matplotlib.use('TkAgg')

#standard libs
from sys import version_info, exit
if version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk
#3rd party libs
from numpy import arange, sin, cos, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.legend import Legend
#local libs



def destroy(e):
    exit()


class history_plot:
    '''
    '''

    def __init__(self, toplevel=False):
        '''
        '''
        if toplevel:
            self.toplevel = toplevel
        else:
            self.toplevel = Tk.Tk()
        self.MakePlot()
            

    def MakePlot(self):
        '''
        '''
        xdata = arange(0,1,.1)
        ydata = [sin(2*pi*x) for x in xdata]
        y2data = [cos(2*pi*x) for x in xdata]

        figurething = Figure()
        subfig = figurething.add_subplot(1,1,1)
        plot1=subfig.plot(xdata, ydata)
        subfig.set_title('ydata vs xdata')
        subfig.set_xlabel('xdata')
        subfig.set_ylabel('ydata')
        plot2=subfig.plot(xdata, y2data)
        #leg = Legend(subfig,[plot1,plot2],['a','b'])

        canvas = FigureCanvasTkAgg(figurething, master=self.toplevel)
        canvas.show()
        canvas.get_tk_widget().grid(row=0, column=0)
        Tk.Label(self.toplevel, text="This is just something").grid(row=0, column=1)
        Tk.Label(self.toplevel, text="This is another something").grid(row=1, column=0)

    def Update(self):
        '''
        '''
        #Figure.clf() clears the window so that can draw updated
        pass


if __name__ == "__main__":
    root = Tk.Tk()
    root.wm_title("Embedding in TK")
    top_level = Tk.Toplevel()
    top_level.grid()
    foo = history_plot(toplevel=top_level)
    Tk.mainloop()
