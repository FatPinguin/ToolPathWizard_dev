### Open in Conda environnement ###

import numpy as np
import matplotlib.pyplot as plt
import csv

#from ToolPathWizard_dev.lib.matplotlib import cm
#from ToolPathWizard_dev.lib.matplotlib.ticker import LinearLocator, FormatStrFormatter
#from ToolPathWizard_dev.lib.mpl_toolkits.mplot3d import Axes3D


#import lib.pandas as pd
#import lib.numpy as np
#import lib.matplotlib.pyplot as plt
#from matplotlib import cm
#from matplotlib.ticker import LinearLocator, FormatStrFormatter
#from mpl_toolkits.mplot3d import Axes3D
#from lib.tkinter import filedialog

#from common_variables import SLICERVERSION, cfrDlfVersion
SLICERVERSION = '2.46'  #Last modification : 11/12/23 #Deploy : xx/xx/2x
cfrDlfVersion = True   #False   #
defaultDir = "C:\\Salome-2019-w64-1.2\\WORK"

if cfrDlfVersion: #operationIsTape:
    fieldNames = ["Operation id", "Instruction", "Operation type", "Layer id", "Curve id", "Point id",
                  "X coord (mm)", "Y coord (mm)", "Z coord (mm)",
                  "Tangent vector X (mm)", "Tangent vector Y (mm)", "Tangent vector Z (mm)", 
                  "Normal vector X (mm)", "Normal vector Y (mm)", "Normal vector Z (mm)", 
                  "Tool rot Z (deg)", "Tool tilt Y (deg)", "7th axis pos (robots units)", "7th axis speed (robots units)",
                  "Distance on curve (mm)", "Total distance (mm) (only active passes)", "Speed (mm/s)", "Stop flag: continuous/stop here (0/1)",
                  "Laser state: off/on (0/1)", "Laser power (laser controller units)", "Cut flag: idle/cut (0/1)", "Aux output 1 (*)", "Version %s"%(SLICERVERSION)]
else:
    fieldnames = ["Operation id", "Instruction", "Operation type", "Layer id", "Curve id", "Point id",
                  "X coord (mm)", "Y coord (mm)", "Z coord (mm)",
                  "Tangent vector X (mm)", "Tangent vector Y (mm)", "Tangent vector Z (mm)", 
                  "Normal vector X (mm)", "Normal vector Y (mm)", "Normal vector Z (mm)", 
                  "Tool rot Z (deg)", "Tool tilt Y (deg)", "7th axis pos (robots units)", "7th axis speed (robots units)",
                  "Distance on curve (mm)", "Total distance (mm) (only active passes)", "Speed (robots units)", "Stop flag: continuous/stop here (0/1)",
                  "Flow rate (mm3/s)", "Extruder temp (deg)", "Extrude: off/on (0/1)", "Direction: retract/push (0/1)", "Aux output 1 ", "Aux output 2 (*)"]

def read_file(fileName, fields = fieldNames):
    try:
        with open('names.csv', newline='') as csvfile:
            df = csv.DictReader(csvfile)
        #df = pd.read_csv(fileName, delimiter=',', usecols = fields)
        print(df["X coord (mm)"])
        return df
    except:
        print("Failed to find folder. Terminate program...")
        #exit()

def set_axes_equal(ax: plt.Axes):
    """Set 3D plot axes to equal scale.

    Make axes of 3D plot have equal scale so that spheres appear as
    spheres and cubes as cubes.  Required since `ax.axis('equal')`
    and `ax.set_aspect('equal')` don't work on 3D.
    """
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])
    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    _set_axes_radius(ax, origin, radius)

def _set_axes_radius(ax, origin, radius):
    x, y, z = origin
    ax.set_xlim3d([x - radius, x + radius])
    ax.set_ylim3d([y - radius, y + radius])
    ax.set_zlim3d([z - radius, z + radius])

def plot(df):
    ## DataFrame from 2D-arrays
    #x = X.reshape(1600)
    #y = Y.reshape(1600)
    #z = Z.reshape(1600)
    #df = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=range(len(x)))
    # Plot using `.trisurf()`:
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(df["X coord (mm)"], df["Y coord (mm)"], df["Z coord (mm)"])
    ax.plot(df["X coord (mm)"], df["Y coord (mm)"], df["Z coord (mm)"], label='parametric curve')
    #ax.quiver(df["X coord (mm)"], df["Y coord (mm)"], df["Z coord (mm)"], u, v, w, length=0.1, normalize=True)
    ax.set_xlabel('X mm')
    ax.set_ylabel('Y mm')
    ax.set_zlabel('Z mm')
    ax.set_box_aspect([1,1,1])
    set_axes_equal(ax)
    plt.show()



    #ax = plt.figure().add_subplot(projection='3d')
    #ax.plot(x, y, z, label='parametric curve')
    #ax.legend()
    #
    #plt.show()


def open_graph():
    #filepath = filedialog.askopenfilename(title="Open a CSV File", filetypes=(("tab files","*.csv"), ("all files","*.*")), initialdir=defaultDir)
    filepath = "C:\\Salome-2019-w64-1.2\\WORK\\240109_ST\\240110_st.csv"
    df = read_file(filepath, fields=["X coord (mm)", "Y coord (mm)", "Z coord (mm)"])
    plot(df)
    return


#_____________________________________________________________________________________________________________________________________________________________________
if __name__ == "__main__":
    open_graph()
    print("Finito")