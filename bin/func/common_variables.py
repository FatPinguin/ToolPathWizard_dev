#https://docs.salome-platform.org/latest/tui/KERNEL/kernel_salome.html
from .environment import geompy

#Dir
defaultDir = "C:\\Salome-2019-w64-1.2\\WORK"


#Constantes d'execution
SLICERVERSION = '2.48'  #Last modification : 06/03/24 #Last deploy : 11/01/24
cfrDlfVersion = False   #True   #
operationIsTape = False
operationIsPellet = False
debugFlag = False
doNotPublishPointInStudy = True #False#True   #Bug


#valeurs de communication :
succes = True
fail = False


#Operation mode :
generic = 0
fdmPelletPerimeter = 1
fdmPelletInfill = 2
milling = 3
fdmPerimeter = 4
fdmInfill = 5
tapeLayingLaser = 6
tapeLayingAirPulse = 7
fdmFiberInfill = 8
fdmFiberPerimeter = 9
dictOfOperations = {fdmPerimeter:"3D printing filament outline", fdmInfill:"3D printing filament infill", 
                    milling:"Milling", 
                    tapeLayingLaser:"Laser assisted fiber placement", 
                    tapeLayingAirPulse:"Composite automated tape layup", 
                    fdmPelletPerimeter:"3D printing pellet outline", fdmPelletInfill:"3D printing pellet infill", 
                    fdmFiberInfill:"Continuous fiber printing infill", fdmFiberPerimeter:"Continuous fiber printing outline", 
                    generic:"General trajectory"}
normalFabOrder = [generic, fdmPelletPerimeter, fdmPelletInfill, fdmPerimeter, fdmInfill, milling, tapeLayingLaser, tapeLayingAirPulse]
infillBeforePerimFabOrder = [generic, fdmPelletInfill, fdmPelletPerimeter, fdmInfill, fdmPerimeter, milling, tapeLayingLaser, tapeLayingAirPulse]


#pour : MoveType
MACHINING = 0
APPROACH = 1
RETRACT = 2
TRAVEL = 3
WAIT = 4


#Constantes
generalContinuityTolerance = 1e-3


#Types por utilisation de QtreeWidget
qtVolumeType = "Volume"
qtGroupType = "Groupe de couches"
qtOperationType = "Operation"
qtSurfaceType = "Surface"
qtOpeModeDict = {fdmPerimeter:'FDM perimetre', fdmInfill:'FDM remplissage', milling:'Usinage', tapeLayingLaser:'Tape Laying Laser', tapeLayingAirPulse:'Tape Laying Air Pulse', fdmPelletPerimeter:'FDM granule perimetre', fdmPelletInfill:'FDM granule remplissage', generic:'Generique'}


volumesTypesList = ["COMPOUND", "COMPSOLID", "SOLID"]
surfacesTypesList = ["COMPOUND", "SHELL", "FACE"]
vectorTypesList = ["WIRE", "EDGE"]
layerAnCutterGroupType = geompy.ShapeType["FACE"]
groupType = ["COMPOUND"]
securityType = ["FACE"]