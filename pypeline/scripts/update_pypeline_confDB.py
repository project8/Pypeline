#standard libs
from sys import version_info
if version_info[0] < 3:
    from Tkinter import Label, Entry, OptionMenu, Button, StringVar, BooleanVar, Checkbutton
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
        self.notebook.grid(row=1, column=0, columnspan=4, sticky='nsew')

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
            'properties':{
                'dripline':BooleanVar(),
                'pypeline':BooleanVar(),
                'get_active':BooleanVar(),
                'set_active':BooleanVar(),
                'logging':BooleanVar(),
                'dump':BooleanVar()
            }
        }
        conf_doc = self.pype.GetChannelDoc(chname)
            
        frame = Frame(self.notebook)
        frame.pack(side='top', fill='both', expand='y')
        rowi = 0
        for key in tkvars.keys():
            if key.startswith('_'):
                continue
            elif key == 'properties':
                for prop in tkvars['properties'].keys():
                    Checkbutton(frame, text=prop,
                                variable=tkvars[key][prop]
                                ).grid(row=rowi, column=0, sticky='ew')
                    tkvars[key][prop].set(conf_doc[key].count(prop))
                    rowi += 1
            else:
                Label(frame, text=key).grid(row=rowi, column=0)
                tkvars[key].set(conf_doc[key])
                Entry(frame, textvariable=tkvars[key]).grid(row=rowi, column=1,
                                                        columnspan=5)
                rowi +=1
        Button(frame, text="save", command=lambda: self.__update_channel(
                chname, tkvars)).grid(row=rowi, column=0)
        self.notebook.add(frame, text=chname)

    def __update_channel(self, chname, tkdict):
        '''
        '''
        props = []
        for key in tkdict.keys():
            if not key == 'properties':
                tkdict[key] = tkdict[key].get()
            else:
                for prop in tkdict['properties'].keys():
                    if tkdict['properties'][prop].get():
                        props.append(prop)
                tkdict[key] = props
      #  old_doc = Document(self.
        self.pype.UpdateChannel(chname, tkdict)
