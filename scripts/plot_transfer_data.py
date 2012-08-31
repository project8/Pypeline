#system
import sys
#3rd party
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def plot_transfer_data(filename):
    
    f = open(filename,'r')
    data = eval(f.read())
    f.close()
    x = []
    y = []
    z = []
    for i in data:
        x.append(i[0])
        y.append(i[1])
        z.append(i[2])

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #plt.xlabel('HF Peak (MHz)')
    #plt.ylabel('LO Frequency (MHz)')
    #plt.zlabel('Power (dBm)')
    plt.title('Transfer Function of Receiver Chain')
    surf = ax.plot_surface(x,y,z,rstride=5,cstride=25,cmap=cm.jet)
    plt.show()

if __name__ == "__main__":
    plot_transfer_data(sys.argv[1])
