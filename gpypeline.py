from Tkinter import *
from datetime import datetime

class App:
    def __init__(self, master):
        self.master = master
        self.time = StringVar()
        self.time.set(datetime.now())


        self.frame = Frame(master)
        self.frame.grid()

        self.setup_grid()

    def setup_grid(self):
        '''
            Create all of the permanent text, should only need to call this once
        '''
        # Text labels
        self.timelabel = Label(self.frame, text="The time is:", relief=RAISED)
        self.timelabel.grid(row=0, sticky=W)

        self.currenttime = Label(self.frame, textvariable=self.time, relief=SUNKEN)
        self.currenttime.grid(row=0, column=1)
       
        # Buttons
        self.button = Button(self.frame, text="QUIT", fg="red", command=self.frame.quit)
        self.button.grid(row=1)

        self.hi_there = Button(self.frame, text="Hello", command=self.say_hi)
        self.hi_there.grid(row=1, column=1, sticky=W)

        self.update = Button(self.frame, text="Update", command=self.update_values)
        self.update.grid(row=1, column=2, sticky=E)


    def update_values(self):
        '''
            Update displayed values
        '''
        self.time.set(str(datetime.now()))
        self.timelabel.after(200, self.update_values)

    def say_hi(self):
        print("hi there, everyone!")

root = Tk()
app=App(root)
root.mainloop()
