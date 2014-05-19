import subprocess


class Gnuplot:

    def __init__(self):
        self.g = subprocess.Popen(
            "gnuplot", stdin=subprocess.PIPE, shell=False)

    # send a message straight to the command line of gnuplot
    # no automatic carriage return
    def gppartial(self, myargs):
        self.g.stdin.write(myargs)

    # send a message straight to the command line of gnuplot
    # automatic carriare return
    def gp(self, myargs):
        self.gppartial(myargs)
        self.gppartial("\n")

    # pass data to gnuplot assuming you used just the plot '-' option
    # dataset is in the form of [ [1,2], [2,3], [3,4] ] etc.
    def sendData(self, dataset):
        for entry in dataset:
            for elem in entry:
                self.g.stdin.write(str(elem) + " ")
            self.g.stdin.write("\n")
        self.g.stdin.write("e\n")

    # shortcut to plot 1d data with arguments, example:
    # plot1d([[1,2],[2,3]]," with lines title "lame-o plot")
    def plot1d(self, dataset, myargs):
        self.plotMany([dataset], [myargs])
#        self.gp("plot '-' "+myargs)
 #       sendData(dataset)

    def plotMany(self, datasets, argsets):
        self.gppartial("plot")
        onstart = True
        for argset in argsets:
            if onstart is not True:
                self.gppartial(" ,")
            self.gppartial(" '-' " + argset)
            onstart = False
        self.gppartial("\n")
        for dataset in datasets:
            self.sendData(dataset)
