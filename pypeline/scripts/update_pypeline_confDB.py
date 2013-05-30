#standard libs
from sys import version_info
if version_info[0] < 3:
    from Tkinter import Label, Entry, OptionMenu, Button, StringVar
from ttk import Notebook, Frame
#3rd party libs
#local libs

class update_pypeline_confDB:
    '''
    '''
    
    def __init__(self, pype, toplevel):
        '''
            Provides a gui form for interfacing with the pypeline_conf database.
        '''
        self.pype = pype
        self.toplevel = toplevel
        self.BuildGui()

    def BuildGui(self):
        '''
        '''
        #select channel section
        newchname = StringVar(value='')
        oldchname = StringVar(value='')
        Entry(self.toplevel, textvariable=newchname).grid(row=0, column=0)
        Button(self.toplevel, text="Create New",
               command=lambda: self._AddTab(newchname.get())
               ).grid(row=0, column=1)
        existing = self.pype.ListOfChannels()
        OptionMenu(self.toplevel, oldchname, *existing).grid(row=0,
                                                                  column=2)
        Button(self.toplevel, text="Update Existing",
               command=lambda: self._AddTab(oldchname.get())
               ).grid(row=0, column=3)

        #tabs of forms
        self.notebook = Notebook(self.toplevel)
        self.notebook.grid(row=1, column=1, columnspan=4, sticky='nsew')

    def _AddTab(self, chname):
        '''
        '''
#        conf_dict = {
#            'channel':chname,
#            'description':"",
#            'result_units':"",
#            'final_units':"",
#            'properties':[]
#        }
        tkvars = {
            'channel':StringVar(),
            'description':StringVar(),
            'result_units':StringVar(),
            'final_units':StringVar(),
            'properties':StringVar()
        }
        conf_doc = self.pype.GetChannelDoc(chname)
            
        frame = Frame(self.notebook)
        frame.pack(side='top', fill='both', expand='y')
        for rowi,key in enumerate(conf_dict.keys()):
            Label(frame, text=key).grid(row=rowi, column=0)
            Entry(frame, textvariable=tkvars[key]).grid(row=rowi, column=1)
        self.notebook.add(frame, text=chname)
