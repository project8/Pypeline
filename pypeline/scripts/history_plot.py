import matplotlib
matplotlib.use('TkAgg')

#standard libs
from sys import version_info, exit
if version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk
#3rd party libs
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure
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

        f = Figure(figsize=(5,4), dpi=100)
        a = f.add_subplot(111)
        t = arange(0.0,3.0,0.01)
        s = sin(2*pi*t)
        
        a.plot(t,s)
        a.set_title('Tk embedding')
        a.set_xlabel('X axis label')
        a.set_ylabel('Y label')

        # a tk.DrawingArea
        canvas = FigureCanvasTkAgg(f, master=root)
        canvas.show()
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        
        #toolbar = NavigationToolbar2TkAgg( canvas, root )
        #toolbar.update()
        canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        
        button = Tk.Button(master=root, text='Quit', command=exit)
        button.pack(side=Tk.BOTTOM)
        if toplevel:
            

    def MakePlot(self):
        '''
        '''
        xdata = arange(0,1,.1)
        ydata = [sin(2*pi*x) for x in xdata]

        figurething = Figure(figsize=(5,4), dpi=100)
        subfig = figurething.add_subplot(1,1,1)
        subfig.plot(xdata, ydata)
        subfig.set_title('ydata vs xdata')
        subfig.set_xlabel('xdata')
        subfig.set_ylabel('ydata')

        canvas = FigureCanvasTkAgg(figurething, master=self.toplevel)
        canvas.show()
        canvas.get_tk_widget().grid(row=0, column=0)
        Tk.Label(self.toplevel, text="This is just something").grid(row=0, column=1)
        Tk.Label(self.toplevel, text="This is another something").grid(row=1, column=0)


if __name__ == "__main__":
    root = Tk.Tk()
    root.wm_title("Embedding in TK")
    top_level = Tk.Toplevel()
    top_level.grid()
    foo = history_plot(toplevel=top_level)
    Tk.mainloop()
