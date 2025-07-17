# Creation of Helical Curves and Surfaces, oriented along Z axis, center at origin
#  J.Cugnoni HEIG-VD 2025
#  
import salome
salome.salome_init_without_session()
import GEOM
import math
from salome.geom import geomBuilder
geompy = geomBuilder.New()

from PyQt5.QtWidgets import  QLineEdit, QDialogButtonBox, QFormLayout, QDialog
from typing import List

class CustomInputDialog(QDialog):
    def __init__(self, labels:List[str], parent=None):
        super().__init__(parent)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        layout = QFormLayout(self)
        
        self.inputs = []
        for lab in labels:
            self.inputs.append(QLineEdit(self))
            layout.addRow(lab, self.inputs[-1])
        
        layout.addWidget(buttonBox)
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
    
    def getInputs(self):
        return tuple(input.text() for input in self.inputs)
    
def MakeHelixGUI():
    dialog=CustomInputDialog(['name','radius (mm)','height (mm)','pitch (mm)','helix dir [-1/1]','stepAngle [°]'])
    if dialog.exec():
        print('MakeHelix started, parameters=radius, height, pitch, helix dir (-1,1)')
        print(dialog.getInputs())
        try:
             inputs = dialog.getInputs()
             name = inputs[0]
             radius = float(inputs[1])
             height = float(inputs[2])
             pitch = float(inputs[3])
             direction = float(inputs[4])
             stepAngle = float(inputs[5])
             stepAngle = stepAngle / 180.0 * 2.0 * math.pi
             rotation = height/pitch*math.pi*2.0
             helix = MakeHelix(radius, height, rotation, direction, stepAngle)
             geompy.addToStudy(helix, name)
             if salome.sg.hasDesktop():
                 salome.sg.updateObjBrowser()
        except:
            print('Exception in MakeHelix')
            pass

def MakeHelix(radius, height, rotation, direction, stepAngle=math.pi/4):
    #  - create a helix -
    radius = 1.0 * radius
    height = 1.0 * height
    rotation = 1.0 * rotation
    nb_steps = int(rotation / stepAngle)
    
    if nb_steps < 1:
        nb_steps = 2 

    if direction > 0:
        direction = +1
    else:
        direction = -1

    from math import sqrt
    z_step = height / nb_steps
    angle_step = rotation / nb_steps
    z = 0.0
    angle = 0.0
    helix_points = []
    for n in range(nb_steps+1):
        from math import cos, sin
        x = radius * cos(angle)
        y = radius * sin(angle)
        p = geompy.MakeVertex(x, y, z)
        helix_points.append( p )
        z += z_step
        angle += direction * angle_step
        pass
    helix = geompy.MakeInterpol(helix_points)
    return helix

def MakeHelixAccurate(radius, height, rotation, direction):
    #  - create a helix -
    radius = 1.0 * radius
    height = 1.0 * height
    rotation = 1.0 * rotation
    if direction > 0:
        direction = +1
    else:
        direction = -1
        pass
    from math import sqrt
    length_z  = height
    length_xy = radius*rotation
    length = sqrt(length_z*length_z + length_xy*length_xy)
    nb_steps = 1
    epsilon = 1.0e-6
    while 1:
        z_step = height / nb_steps
        angle_step = rotation / nb_steps
        z = 0.0
        angle = 0.0
        helix_points = []
        for n in range(nb_steps+1):
            from math import cos, sin
            x = radius * cos(angle)
            y = radius * sin(angle)
            p = geompy.MakeVertex(x, y, z)
            helix_points.append( p )
            z += z_step
            angle += direction * angle_step
            pass
        helix = geompy.MakeInterpol(helix_points)
        length_test = geompy.BasicProperties(helix)[0]
        prec = abs(length-length_test)/length
        # print nb_steps, length_test, prec
        if prec < epsilon:
            break
        nb_steps *= 2
        pass
    return helix

def MakeHelicalSurfaceGUI():
    dialog=CustomInputDialog(['name','radius 1 (mm)','radius 2 (mm)','height (mm)','pitch (mm)','twist (°)','helix dir [-1/1]','step angle °','partition 0/1'])
    if dialog.exec():
        print('MakeHelicalSurface started, parameters=radius1 & 2, height, pitch, helix dir (-1,1)')
        print(dialog.getInputs())
        try:
             inputs = dialog.getInputs()
             name = inputs[0]
             radius1 = float(inputs[1])
             radius2 = float(inputs[2])
             height = float(inputs[3])
             pitch = float(inputs[4])
             twist = float(inputs[5]) * math.pi / 180.0
             direction = float(inputs[6])
             rotation = height / pitch * math.pi * 2.0
             stepAngle = float(inputs[7])
             stepAngle = stepAngle / 180.0 * 2.0 * math.pi
             partition = int(inputs[8])
             helisurf = MakeHelicalSurface(radius1, radius2, height, rotation, twist, direction, stepAngle)
             # optionally partition  helix to be more manageable during boolean operations
             if partition < 1: 
                geompy.addToStudy(helisurf, name )
             else:
                vx=geompy.MakeVectorDXDYDZ(1.0, 0.0, 0.0)
                vy=geompy.MakeVectorDXDYDZ(0.0, 1.0, 0.0)
                orig=geompy.MakeVertex(0.0, 0.0, 0.0)
                planesize=max(4*radius2,4*height)
                planeYZ=geompy.MakePlane(orig,vx,planesize)
                planeXZ=geompy.MakePlane(orig,vy,planesize)
                helisurf=geompy.MakePartition([helisurf],[planeXZ,planeYZ]) 
                geompy.addToStudy(helisurf, name )

             if salome.sg.hasDesktop():
                salome.sg.updateObjBrowser()
        except Exception as e:
            print('Exception in MakeHelicalSurface')
            print(e)
            pass


def MakeHelicalSurface(radius1, radius2, height, rotation, twist, direction, stepAngle):
    #build 2 helix by interpolation
    helix1 = MakeHelix(radius1, height, rotation, direction, stepAngle)
    helix2 = MakeHelix(radius2, height, rotation, direction, stepAngle)

    # shift helix 2 to create pitch angle
    p2z = math.tan(twist) * (radius2 - radius1)
    helix2=geompy.TranslateDXDYDZ(helix2,0.0, 0.0, p2z)

    # build surface by filling between the two helix
    try:
        helisurf = geompy.MakeFilling([helix1,helix2])
    except:
        helisurf = geompy.MakeFilling([helix1,helix2],isApprox=1)

    # old code using Pipe, not robust because of orientation issue
    # p1 = geompy.MakeVertex(radius1, 0.0, 0.0)
    # p2 = geompy.MakeVertex(radius2, 0.0, p2z)
    # line = geompy.MakeLineTwoPnt(p1,p2)
    # vz = geompy.MakeVectorDXDYDZ(0.0, 0.0, 1.0)
    # helisurf = geompy.MakePipeBiNormalAlongVector(line,helix,vz)

    return helisurf