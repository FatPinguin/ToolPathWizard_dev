"""Structure de données des éléments pour l'utilisation du slicer 6 axes et leur sauvegarde
"""
from .errors import Unfound_edge
#from ToolPathWizard_dev.lib.reloading import reloading

###__________________________________________________________________________________________________________________________________________________________________
class cls_generic:
    def __init__(self, speed:float, approachSpeed:float, retractSpeed:float, travelSpeed:float, securityDistance:float):
        self.toolRotZ = 0 #[°]
        self.toolTiltY = 0 #[°]
        self.axis7thPosition = 0
        self.axis7thSpeed = 0
        self.toolSpeed = speed
        self.approachSpeed = approachSpeed
        self.retractSpeed = retractSpeed
        self.travelSpeed = travelSpeed
        self.securityDistance = securityDistance
        #self.stopFlag = stopFlag #TODO - clarifier ce flag. Le déterminer à l'export ?

class cls_milling:
    def __init__(self, speed:float, spindleSpeed:float, toolDiameter:float, toolCorrection:bool):
        #Machining
        self.toolSpeed = speed
        #self.spindleState = spindleState
        self.spindleSpeed = spindleSpeed
        self.toolDiameter = toolDiameter
        self.toolCorrection = toolCorrection #bool

class cls_fdm_pellet:
    def __init__(self, screwSpeed:float, infillSpeed:float, perimeterSpeed:float, extruderTemp:float, distanceToRetract:float, extrusionDiameter:float):
        #FDM pellets extruder
        self.screwSpeed = screwSpeed
        self.infillSpeed = infillSpeed
        self.perimeterSpeed = perimeterSpeed
        self.extruderTemp = extruderTemp
        self.distanceToRetract = distanceToRetract #TODO-introduire dans endCurveDistance
        self.extrusionDiameter = extrusionDiameter

class cls_fdm_filament:
    def __init__(self, infillSpeed:float, perimeterSpeed:float, relativeFilamentSpeed:float, filamentSpeed:float, cooling:bool, extruderTemp:float, extrusionDiameter:float):
        #FDM filament
        self.infillSpeed = infillSpeed
        self.perimeterSpeed = perimeterSpeed
        self.relativeFilamentSpeed = relativeFilamentSpeed
        self.filamentSpeed = filamentSpeed
        #self.cooling = cooling
        self.extruderTemp = extruderTemp
        self.extrusionDiameter = extrusionDiameter

class cls_laser_tape:
    def __init__(self, speed:float, laserStartingDistance:float, laserStopingDistance:float):
        #Laser Assisted Fiber Placement
        self.minimumTrajectoryLength = 30#65   #mm
        self.toolSpeed = speed
        self.laserStartingDistance = 5  #mm laserStartingDistance from start
        self.laserStopingDistance = 5   #mm laserStopingDistance from end
        self.cuttingDistance = 44   #mm #From end     60???
        #self.preStartDist = 5 #mm : dépacement 5mm avant le 1er point d'une courbe
        #self.preStart = True
        #self.tapeFeed = None
        self.feedSpeed = 30#None
        #self.laserState = None
        self.laserPower = 80
        #self.cutFlag = None
        self.offset = 0 #mm Negative = compression / positive = spacing
        self.incr = 1   #mm
        self.layIncr = 0.135    #mm
        self.cutIncr = 3    #mm

class cls_air_tape:
    def __init__(self, speed:float):#, airStartingDistance:float, airStopingDistance:float, cuttingDistance:float):
        #Composite Automated Tape Layup
        self.toolSpeed = speed
        self.airStartingDistance = 10#airStartingDistance
        self.airStopingDistance =  5#airStopingDistance
        self.cuttingDistance = 49#cuttingDistance
        #self.tapeFeed = None
        self.feedSpeed = 20
        #self.heaterState = None
        #self.cutFlag = None
        #self.rollerPressure = None

class cls_machine_parameters:
    def __init__(self, dataParamGen:cls_generic, dataParamFdmPellet:cls_fdm_pellet, dataParamFdmFilament:cls_fdm_filament, dataParamMilling:cls_milling, dataParamTapeLaser:cls_laser_tape, dataParamTapeAirPulse:cls_air_tape):
        self.generics:cls_generic = dataParamGen
        self.fdmPellet:cls_fdm_pellet = dataParamFdmPellet
        self.fdmFilament:cls_fdm_filament = dataParamFdmFilament
        self.milling:cls_milling = dataParamMilling
        self.laserTape:cls_laser_tape = dataParamTapeLaser
        self.airTape:cls_air_tape = dataParamTapeAirPulse

###__________________________________________________________________________________________________________________________________________________________________
class cls_coordinates :
    def __init__(self, CoordArray:list) :
        [self.x, self.y, self.z] = CoordArray
        
    def __str__(self):
        return str(self.x) + ", " + str(self.y) + ", " + str(self.z)

class cls_vector :
    def __init__(self, vectorArray:list) :
        [self.vx, self.vy, self.vz] = vectorArray
    def __str__(self):
        return str(self.vx) + ", " + str(self.vy) + ", " + str(self.vz)



class cls_point :
    def __init__(self, dataPointCoord, pointEntry:str, distanceOnCurve:float, moveType:int, securitySurfaceEntry:str, dataNormalVector:cls_vector, dataTangentialVector:cls_vector, ToolHeadState:list, speed, stopFlag:bool, newIncr:float):
        self.pointId:str = pointEntry
        self.distanceOnCurve:float = distanceOnCurve
        self.moveType:int = moveType #Décrit si il s'agit d'un mouvement rapide ou un "usinage" --> 0 = op machine, 1 = approche, 2 = retrait
        self.securitySurfaceId:str = securitySurfaceEntry
        self.coordinates:cls_coordinates = dataPointCoord
        self.normalVector:cls_vector = dataNormalVector
        self.tangentialVector:cls_vector = dataTangentialVector
        self.speed = speed
        self.stopFlag:bool = stopFlag
        self.lstPtDist:float = newIncr  #Increment from last point to this point
        #self.incrToThisPoint = newIncr
        self.ToolHeadState:list = ToolHeadState #list
    
    def __str__(self):
        txt="cls_point: Id="+str(self.pointId)+", coordinates="+str(self.coordinates)+" distance="+str(self.distanceOnCurve)
        return txt

class cls_curve :
    def __init__(self, curveEntry:str, curveLength:float, layerEntry:str, cuttingSurfaceEntry:str, positionTool:bool):#, discretisationIncrement:float):
        self.curveId = curveEntry
        self.curveLength = curveLength
        self.layerId = layerEntry
        self.cuttingSurfaceId = cuttingSurfaceEntry
        self.increment = 0#discretisationIncrement
        self.steps = 0
        self.prePosTool = positionTool
        self.pointList = []
    
    def update_discretisation_increment(self, discretisationIncrement:float):
        self.increment = discretisationIncrement

    def add_point_to_curve(self, dataPoint:cls_point):
        self.pointList.append(dataPoint)
        return len(self.pointList)

class cls_operation :
    def __init__(self, fabricationMode:int, operationID:str) :
        self.fabricationMode = fabricationMode
        self.ID = operationID
        self.toolClearance = False
        self.tbe = 1 #To be exported 0/1
        self.order = '...'
        self.name = "None"
        self.curveList = []
    
    def add_curve_to_operation(self, dataCurve:cls_curve):
        curve:cls_curve
        for curve in self.curveList:
            if curve.curveId == dataCurve.curveId:
                print("Trajectoire deja ajoutee a l'operation") #TODO - Afficher un message d'erreur : proposer de skip, annuler toute l'operation, continuer ou tout ignorer
        self.curveList.append(dataCurve)

class cls_surface :
    def __init__(self, surfaceEntry:str) :
        self.surfaceId = surfaceEntry
        self.operationList = []
    
    def add_operation_to_layer(self, dataOperation:cls_operation):
        operation:cls_operation
        #for operation in self.operationList:
        #    if operation.fabricationMode == dataOperation.fabricationMode:
        #        print("Operation deja existante sur cette surface") #TODO - Afficher un message d'erreur : proposer de skip, annuler toute l'operation, continuer ou tout ignorer
        self.operationList.append(dataOperation)
    
    def sort_operations(self):
        operationListSorted = sorted(self.operationList, key = lambda x: x.fabricationMode, reverse=False)
        print("debug : ", self.operationList)
        print("debug sorted : ", operationListSorted)
        self.operationList = operationListSorted

class cls_surfaces_grp :
    def __init__(self, groupID, isLayersFlag:int, originalSurfaceID, increment:float, isCreatedByOffset:int, translationPathID) :
        self.typeGenerated = isLayersFlag # 0 = layers; 1 = cutting tool
        self.surfacesGrpId = groupID #groupFolderGeom.GetID()#GetEntry()
        self.originalSurfaceId = originalSurfaceID#originalSurfaceGeom.GetEntry()#GetID()#
        self.increment = increment
        self.translationPathId = translationPathID
        #if isCreatedByOffset == False : # False = mutitranslation - True = Offset
        #    self.translationPathId = translationPathGeom.GetEntry()#GetID()# #TODO - get mode from GUI informations #Si translation 
        self.surfaceList = []

    def add_surface_to_group(self, dataSurface:cls_surface):
        surface:cls_surface
        for surface in self.surfaceList:
            if surface.surfaceId == dataSurface.surfaceId:
                print("Surface deja ajoutee au groupe") #TODO - Afficher un message d'erreur : proposer de skip, annuler toute l'operation, continuer ou tout ignorer
        self.surfaceList.append(dataSurface)

class cls_volume :
    def __init__(self, volumeId) :
        #self.volume = volumeGeom
        self.volumeId = volumeId
        self.surfaceGroupList = []

    def add_grp_surface_to_volume(self, dataSurfaceGroup:cls_surfaces_grp):
        surfGrp:cls_surfaces_grp
        for surfGrp in self.surfaceGroupList:
            if surfGrp.originalSurfaceId == dataSurfaceGroup.originalSurfaceId:
                print("Un groupe genere à partir de cette surface existe deja") #TODO - Afficher un message d'erreur : proposer de skip, annuler toute l'operation, continuer ou tout ignorer
        self.surfaceGroupList.append(dataSurfaceGroup)

class cls_data_structure :
    def __init__(self, studyAdress, machineParam:cls_machine_parameters) :
        self.studyAdress = studyAdress
        self.machineParam = machineParam
        self.volumeList = []
        self.generatedOperations = []
        #self.lastOperationIndex:int = 0
        self.sortedOperations = []
    
    def update_machines_parameters(self, machineParam:cls_machine_parameters):
        self.machineParam = machineParam
    
    def add_volume_to_data_struct(self, dataVolume:cls_volume):
        if self.volumeList != []:
            tagVerif = False
            volume:cls_volume
            for volume in self.volumeList:
                if volume.volumeId == dataVolume.volumeId:
                    print("Volume deja existant dans la structure de donnees") #TODO - Afficher un message d'erreur : proposer de skip, annuler toute l'operation, continuer ou tout ignorer
                    tagVerif = True
                    return volume
            if tagVerif == False:
                self.volumeList.append(dataVolume)
                return dataVolume
        else:
            self.volumeList.append(dataVolume)
            return dataVolume
###__________________________________________________________________________________________________________________________________________________________________
class cls_edge:
    def __init__(self, geom, length:float) -> None:
        self.geom = geom
        self.length = length


class cls_points_of_interest:
    def __init__(self, start:float, stop:float, edgeList:list) -> None:
        self.nb = 2
        self.count = 0
        self.start = self.info_point(start, "start", edgeList, True, 0)
        self.stop = self.info_point(stop, "stop", edgeList, True, 0)
        self.op = []    #[[distance on curve, decriptor, edgeGeom], ...]
    

    def add_point(self, distOnWire:float, descriptor:str, edgeList:list, increment:float):
        self.op.append(self.info_point(distOnWire, descriptor, edgeList, False, increment))
        #self.nb = len(self.op)+2
        self.nb += 1
    

    class info_point:
        def __init__(self, distOnWire:float, descriptor:str, edgeList:list, stop:bool, increment:float) -> None:
            self.distOnWire = distOnWire
            self.descriptor = descriptor
            self.distOnEdge, self.edgeGeom = self.get_edge_for_distance(edgeList)
            self.stop = stop
            self.increment = increment  #Increment from last point #mm
        
        #@reloading
        def get_edge_for_distance(self, edgeList:list):
            distRange = 0   #Distance to the end of the current edge
            edge:cls_edge
            for edge in edgeList:
                distFromLast = distRange
                distRange += edge.length
                if self.distOnWire <= distRange:
                    edgeGeom = edge.geom
                    distOnEdge = self.distOnWire - distFromLast
                    return distOnEdge, edgeGeom
            raise Unfound_edge(f"No edge found for {self.distOnWire}mm on wire")

###__________________________________________________________________________________________________________________________________________________________________
def default_machine_settings():
    dataParamGen = cls_generic(speed=50, approachSpeed=30, retractSpeed=100, travelSpeed=200, securityDistance=50)
    dataParamFdmPellet = cls_fdm_pellet(screwSpeed=4, infillSpeed=50, perimeterSpeed=50, extruderTemp=195, distanceToRetract=10, extrusionDiameter=4)
    dataParamFdmFilament = cls_fdm_filament(infillSpeed=80, perimeterSpeed=60, relativeFilamentSpeed=50, filamentSpeed=60, cooling=True, extruderTemp=195, extrusionDiameter=0.4)
    dataParamMilling = cls_milling(speed=20, spindleSpeed=3000, toolDiameter=8, toolCorrection=True)
    dataParamTapeLaser = cls_laser_tape(speed=20, laserStartingDistance=2, laserStopingDistance=1)
    dataParamTapeAirPulse = cls_air_tape(speed=20)
    return cls_machine_parameters(dataParamGen, dataParamFdmPellet, dataParamFdmFilament, dataParamMilling,dataParamTapeLaser, dataParamTapeAirPulse)