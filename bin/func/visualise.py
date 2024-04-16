""" Need to install and update several modules :
    0?) Run "C:\SALOME-9.10.0\env_launch.bat"
    1) Run "C:\SALOME-9.10.0\run_salome_shell.bat"
    2) if needed $python -m pip install --upgrade pip
    3) $python -m pip install --upgrade matplotlib
    4) $python -m pip uninstall pandas
    5) $python -m pip install pandas
    """

from PyQt5 import QtWidgets
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt #Use pyqtgraph ?
import pandas as pd


from .common_variables import SLICERVERSION, cfrDlfVersion, defaultDir
#SLICERVERSION = '2.46'  #Last modification : 11/12/23 #Deploy : xx/xx/2x
#cfrDlfVersion = True   #False   #

if cfrDlfVersion: #operationIsTape:
    fieldNames = ["Operation id", "Instruction", "Operation type", "Layer id", "Curve id", "Point id",
                  "X coord (mm)", "Y coord (mm)", "Z coord (mm)",
                  "Tangent vector X (mm)", "Tangent vector Y (mm)", "Tangent vector Z (mm)", 
                  "Normal vector X (mm)", "Normal vector Y (mm)", "Normal vector Z (mm)", 
                  "Tool rot Z (deg)", "Tool tilt Y (deg)", "7th axis pos (robots units)", "7th axis speed (robots units)",
                  "Distance on curve (mm)", "Total distance (mm) (only active passes)", "Speed (mm/s)", "Stop flag: continuous/stop here (0/1)",
                  "Laser state: off/on (0/1)", "Laser power (laser controller units)", "Cut flag: idle/cut (0/1)", "Aux output 1 (*)", "Version %s"%(SLICERVERSION)]
else:
    fieldNames = ["Operation id", "Instruction", "Operation type", "Layer id", "Curve id", "Point id",
                  "X coord (mm)", "Y coord (mm)", "Z coord (mm)",
                  "Tangent vector X (mm)", "Tangent vector Y (mm)", "Tangent vector Z (mm)", 
                  "Normal vector X (mm)", "Normal vector Y (mm)", "Normal vector Z (mm)", 
                  "Tool rot Z (deg)", "Tool tilt Y (deg)", "7th axis pos (robots units)", "7th axis speed (robots units)",
                  "Distance on curve (mm)", "Total distance (mm) (only active passes)", "Speed (robots units)", "Stop flag: continuous/stop here (0/1)",
                  "Flow rate (mm3/s)", "Extruder temp (deg)", "Extrude: off/on (0/1)", "Direction: retract/push (0/1)", "Aux output 1 ", "Aux output 2 (*)"]

def read_file(fileName, fields):# = fieldNames):
    try:
        df = pd.read_csv(fileName, delimiter=',')#, usecols = fields)
        print(df["X coord (mm)"])
        return df
    except:
        print("Failed to find folder. Terminate program...")
        exit()

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
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(df["X coord (mm)"], df["Y coord (mm)"], df["Z coord (mm)"])
    ax.plot(df["X coord (mm)"], df["Y coord (mm)"], df["Z coord (mm)"], label='parametric curve')
    ax.set_xlabel('X mm')
    ax.set_ylabel('Y mm')
    ax.set_zlabel('Z mm')
    ax.set_box_aspect([1,1,1])
    set_axes_equal(ax)
    plt.show()


def open_graph():
    try: 
        filepath, typ = QtWidgets.QFileDialog.getOpenFileName(None, 'Select [.csv] file' ,defaultDir ,"Data export slicer (*.csv)")
        df = read_file(filepath, fields=["X coord (mm)", "Y coord (mm)", "Z coord (mm)"])
        print("Open graph")
        plot(df)
        #plt.close()
    except:
        print("Error occured while trying to open a CSV")
    return




#_____________________________________________________________________________________________________________________________________________________________________
if __name__ == "__main__":
    open_graph()
    print("Finito")