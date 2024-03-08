import csv


from ..viz.user_com import message_error, update_progressBar
from .Classes import cls_data_structure, cls_volume, cls_surfaces_grp, cls_surface, cls_operation, cls_curve, cls_point
from .common_variables import SLICERVERSION, succes, fail, cfrDlfVersion, operationIsPellet, APPROACH, RETRACT, MACHINING, TRAVEL, WAIT, dictOfOperations, tapeLayingLaser
from .csv_headers import fabrication_header
import ToolPathWizard_dev.bin.func.environment as env
from .dlf7axis import dlf_7_axis_point_modification


def export_tool(data:cls_data_structure, fileAdress:str, exportInfillBeforePerimeter:bool, UiProgressBar, flag7axis, orthoVector=None): #TODO - si milling export dans le sens inverse checkBox --> message attention lors de la création de l'opération: la surface choisie sera la première à etre usinée.
    #Tri des opérations
    if data.sortedOperations == []:
        data.sortedOperations = data.generatedOperations
    sortedFabricationSteps, totalPointCounter, fabModes = __sort_operations(data)
    #Traitement 7eme axe DLF
    if flag7axis:
        for fm in fabModes :
            if fm == tapeLayingLaser :
                dlf_7_axis_point_modification(sortedFabricationSteps, orthoVector)
    #Création des lignes à exporter
    exportLines, totalDistanceActive = write_points(sortedFabricationSteps, totalPointCounter, UiProgressBar)
    fieldNames = Field_names(fabModes)
    try:
        print('\tFile creation...')
        with open(fileAdress, 'w', encoding='UTF8', newline='') as csvFile: 
            write = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            print('\t\tThe file has been successfully created.')
            write.writerows(fieldNames) #Export des entêtes du fichier
            write.writerows(exportLines)    #Export des lignes
            csvFile.close()
            print('\t\tThe points have been exported.')
            print('\t\tTotal active distance: %.3f'%(totalDistanceActive))
    except :#FileExistsError:#FileNotFoundError:
        #TODO - messageError GUI : File already exist
        print('\t\tCould not create the file.')
        message_error("Could not create the file.")
        return fail
    return succes


def Field_names(fabModes:list):
    fieldNames = []
    if fabModes == []:
        message_error("No known manufacturing method detected.\nCheck the CSV and pay attention to the behaviour of the machine.")
        fieldNames.append(["No known manufacturing method detected. Check the CSV and pay attention to the behaviour of the machine."])
    else:
        for code in fabModes:
            fieldNames.append(fabrication_header(code))
    #print("Fabrication modes detected : ", fabModes)
    return fieldNames


#def Field_names_old():
#    #fieldnames = [
#    #    "Operation Id", "Instruction",
#    #    "Operation Type", "Layer Id", "Curve Id", "Point Id",
#    #    "Point Coordinates X", "Point Coordinates Y", "Point Coordinates Z", 
#    #    "Normal Vector X", "Normal Vector Y", "Normal Vector Z", 
#    #    "Tangential Vector X", "Tangential Vector Y", "Tangential Vector Z", 
#    #    "Longitudinal Vector X", "Longitudinal Vector Y", "Longitudinal Vector Z", 
#    #    "Distance On Curve", "Total Strip Length", "Strip Feed", 
#    #    "Start and End Of Continuous Trajectory"
#    #    ]
#    if cfrDlfVersion: #operationIsTape:
#        fieldnames = ["Operation id", "Instruction", "Operation type", "Layer id", "Curve id", "Point id",
#                      "X coord (mm)", "Y coord (mm)", "Z coord (mm)",
#                      "Tangent vector X (mm)", "Tangent vector Y (mm)", "Tangent vector Z (mm)", 
#                      "Normal vector X (mm)", "Normal vector Y (mm)", "Normal vector Z (mm)", 
#                      "Tool rot Z (deg)", "Tool tilt Y (deg)", "7th axis pos (robots units)", "7th axis speed (robots units)",
#                      "Distance on curve (mm)", "Total distance (mm) (only active passes)", "Speed (mm/s)", "Stop flag: continuous/stop here (0/1)",
#                      "Laser state: off/on (0/1)", "Laser power (laser controller units)", "Cut flag: idle/cut (0/1)", "Aux output 1 (*)", "Version %s"%(SLICERVERSION)]
#        #old
#        #fieldnames = ["Operation id", "Instruction", "Operation type", "Layer id", "Curve id", "Point id",
#        #              "X coord (mm)", "Y coord (mm)", "Z coord (mm)",
#        #              "Tangent vector X (mm)", "Tangent vector Y (mm)", "Tangent vector Z (mm)", 
#        #              "Normal vector X (mm)", "Normal vector Y (mm)", "Normal vector Z (mm)", 
#        #              "Tool rot Z (deg)", "Tool tilt Y (deg)", "7th axis pos (robots units)", "7th axis speed (robots units)",
#        #              "Distance on curve (mm)", "Total distance (mm) (only active passes)", "Speed (robots units)", "Stop flag: continuous/stop here (0/1)",
#        #              "Feed length (mm)", "Feed rate (mm/s)", "Laser state: off/on (0/1)", "Laser power (laser controller units)", "Cut flag: idle/cut (0/1)", "Aux output 1 (*)", "Version %s"%(SLICERVERSION)]
#        return [fieldnames]
#    elif operationIsPellet:
#        fieldnames = ["Operation id", "Instruction", "Operation type", "Layer id", "Curve id", "Point id",
#                      "X coord (mm)", "Y coord (mm)", "Z coord (mm)",
#                      "Tangent vector X (mm)", "Tangent vector Y (mm)", "Tangent vector Z (mm)", 
#                      "Normal vector X (mm)", "Normal vector Y (mm)", "Normal vector Z (mm)", 
#                      "Tool rot Z (deg)", "Tool tilt Y (deg)", "7th axis pos (robots units)", "7th axis speed (robots units)",
#                      "Distance on curve (mm)", "Total distance (mm) (only active passes)", "Speed (robots units)", "Stop flag: continuous/stop here (0/1)",
#                      "Flow rate (mm3/s)", "Extruder temp (deg)", "Extrude: off/on (0/1)", "Direction: retract/push (0/1)", "Aux output 1 ", "Aux output 2 (*)"]
#        return [fieldnames]
#    else:
#        standardHeader = ["Operation id", "Instruction", "Operation type", "Layer id", "Curve id", "Point id",
#                      "X coord (mm)", "Y coord (mm)", "Z coord (mm)",
#                      "Tangent vector X (mm)", "Tangent vector Y (mm)", "Tangent vector Z (mm)", 
#                      "Normal vector X (mm)", "Normal vector Y (mm)", "Normal vector Z (mm)", 
#                      "Tool rot Z (deg)", "Tool tilt Y (deg)", "7th axis pos (robots units)", "7th axis speed (robots units)",
#                      "Distance on curve (mm)", "Total distance (mm) (only active passes)", "Speed (robots units)", "Stop flag: continuous/stop here (0/1)",
#                      "Tool state"]
#        genericHeader = ["-","-","General trajectory","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-",
#                         "No tool selected"]
#        #old
#        #laserFiberHeader = ["-","-","Laser assisted fiber placement","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-",
#        #                   "Feed length (mm)", "Feed rate (mm/s)", "Laser state: off/on (0/1)", "Laser power (laser controller units)", "Cut flag: idle/cut (0/1)", "Aux output 1 (*)", "Version %s"%(SLICERVERSION)]
#        laserFiberHeader = ["-","-","Laser assisted fiber placement","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-",
#                           "Laser state: off/on (0/1)", "Laser power (laser controller units)", "Cut flag: idle/cut (0/1)", "Aux output 1 (*)", "Version %s"%(SLICERVERSION)]
#        fdmHeader = ["-","-","3D printing filament","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-",
#                    "Relative Filament Feed (mm) [incremental]", "Filament feed speed (mm/s)", "Part cooling: off/on (0/1)", "Extruder temp (deg)", "Aux output 1 (*)", "Aux output 2 (*)"]
#        fdmPelletHeader = ["-","-","3D printing pellet","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-",
#                          "Flow rate (mm3/s)", "Extruder temp (deg)", "Extrude: off/on (0/1)", "Direction: retract/push (0/1)", "Aux output 1 ", "Aux output 2 (*)"]
#        millingHeader = ["-","-","Milling","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-",
#                         c]
#        airFiberHeader = ["-","-","Composite automated tape layup","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-",
#                         "Tape Feed (mm)", "Tape feed speed (mm/s)", "Heating: off/on (0/1)", "Heater power (0 to 1)", "Cut flag: off/on (0/1)", "Roller pressure (0 to 1)"]
#        fdmFiberHeader = ["-","-","Continuous fiber printing","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-",
#                         "Relative Filament Feed (mm) [incremental]", "Filament feed speed (mm/s)", "Part cooling: off/on (0/1)", "Extruder temp (deg)", "Cut: off/on (0/1)", "Aux output 2 (*)"]
#        #fieldnames = ["operation id", "instruction", "operation type", "layer id", "curve id", "point id",
#        #              "x coord (mm)", "y coord (mm)", "z coord (mm)",
#        #              "x tangent vector (mm)", "y tangent vector (mm)", "z tangent vector (mm)",
#        #              "x normal vector (mm)", "y normal vector (mm)", "z normal vector (mm)",
#        #              "Tool Rot Z (deg)", "Tool tilt Y (deg)",
#        #              "7th axis pos (robots units)", "7th axis speed (robots units)",
#        #              "Distance on curve (mm)", "Total distance (mm) (only active passes)",
#        #              "speed (robot’s units)",
#        #              "Stop flag: 0 = continuous, 1 = Stop here",
#        #              "Tool states..."] #TODO - Ajouter les noms pour chaque outil
#        #write.writerow(standardHeader)
#        #write.writerow(genericHeader)
#        #write.writerow(laserFiberHeader)
#        #write.writerow(fdmHeader)
#        #write.writerow(fdmPelletHeader)
#        #write.writerow(millingHeader)
#        #write.writerow(airFiberHeader)
#        #write.writerow(fdmFiberHeader)
#        fieldnames = [standardHeader, genericHeader, laserFiberHeader, fdmHeader, fdmPelletHeader, millingHeader, airFiberHeader, fdmFiberHeader]
#    return fieldnames


def moveType_interpreter(moveType):
    if moveType == APPROACH:
        return 'Approach'
    elif moveType == RETRACT:
        return 'Withdrawal'
    elif moveType == MACHINING:
        return 'Work'
    elif moveType == TRAVEL:
        return 'Travel'
    elif moveType == WAIT:
        return 'Wait'
    else:
        return 'No information'


def write_points(sortedFabricationSteps, totalPointCounter, UiProgressBar):
    try:
        print('\tExporting points...')
        totalDistanceActive = 0
        progressCount = 0
        exportLines = []
        curve:cls_curve
        point:cls_point
        for step in sortedFabricationSteps:
            [curveList, surfaceId, fabricationMode, operationID] = step
            for curve in curveList:
                curveId = curve.curveId
                for point in curve.pointList:
                    #progressCount+=1
                    #UiProgressBar.setValue(progressCount/totalPointCounter*100)
                    if point.moveType == MACHINING:
                        totalDistanceActive += point.lstPtDist
                    line = __format_data_in_string(point, surfaceId, fabricationMode, curveId, totalDistanceActive, operationID, moveType_interpreter(point.moveType))
                    if line == None or line == []:
                        print(f"Line point: {point.pointId}", line)
                        raise ValueError('Empty line to writte in CSV')
                    if (cfrDlfVersion == False) or (moveType_interpreter(point.moveType) != 'Travel' and cfrDlfVersion) :   #Point Travel inutile pour le pré-prossecing Rohs
                        exportLines.append(line)
                    progressCount+=1
                    update_progressBar(UiProgressBar, progressCount/totalPointCounter*100)
        return exportLines, totalDistanceActive
    except :
        message_error("Could not export the points.")


#def __sort_operations_dev(data:cls_data_structure):
#    totalPointCounter = 0
#    #Tri des opérations
#    try:
#        print('\tSorting of operations...')
#        activeStep="Open data structure"
#        sortedFabricationSteps = []
#        #Selection de l'ordre de fabrication
#        fabOrder = data.sortedOperations
#        activeStep = "Fabrication order:" + str(fabOrder)
#        for opeName in fabOrder:
#            volume:cls_volume
#            for volume in data.volumeList:
#                activeStep = "Volume: %s"%(volume.volumeId)
#                volumeId = volume.volumeId
#                surfaceGrp:cls_surfaces_grp
#                for surfaceGrp in volume.surfaceGroupList:
#                    activeStep = "Surface group: %s"%(surfaceGrp.surfacesGrpId)
#                    tmpSurfaceList = surfaceGrp.surfaceList
#                    #if mode == milling: #commence par la dernière couche crée pour rentrer dans la matière
#                    #    tmpSurfaceList.reverse()
#                    surface:cls_surface
#                    for surface in tmpSurfaceList:
#                        activeStep = "Surface: %s"%(surface.surfaceId)
#                        surfaceId = surface.surfaceId
#                        operation:cls_operation
#                        for operation in surface.operationList:
#                            if operation.tbe:
#                                activeStep = "Surface: %s Operation: %s"%(surface.surfaceId, operation.fabricationMode)
#                                fabricationMode = operation.fabricationMode
#                                if operation.name == opeName:
#                                    order = operation.order.split('.')
#                                    sortedFabricationSteps.append([operation.curveList, surfaceId, fabricationMode, operation.ID, order])
#                                    curve:cls_curve
#                                    activeStep = "Operation name: %s Fabrication mode: %s"%(opeName, fabricationMode)
#                                    for curve in operation.curveList:
#                                        activeStep = "Operation name: %s Curve: %s"%(opeName, curve.curveId)
#                                        point:cls_point
#                                        for point in curve.pointList:
#                                            activeStep = "Point: %s"%(point.pointId)
#                                            totalPointCounter+=1
#        
#        
#        #sortedFabricationSteps.sort(key=lambda x:x[4])  #sort selon order
#        
#        print('\t\tThe operations have been sorted.')
#        print('\t\tNumber of points detected: %d'%(totalPointCounter))
#    except :
#        print('\t\tCould not sort out the operations. Active step: %s'%(activeStep))
#        message_error("Could not sort out the operations.")
#    return sortedFabricationSteps, totalPointCounter
#
#
#def __sort_layer_and_order(sortedFabricationSteps):
#    # trier les layers order=[col,line] par colonne et 
#    tableauExport = []
#    for step in sortedFabricationSteps:
#        pass
        

def __sort_operations(data:cls_data_structure):
    totalPointCounter = 0
    #Tri des opérations
    try:
        print('\tSorting of operations...')
        sortedFabricationSteps = []
        fabModes = []
        #Selection de l'ordre de fabrication
        volume:cls_volume
        surfaceGrp:cls_surfaces_grp
        surface:cls_surface
        operation:cls_operation
        curve:cls_curve
        point:cls_point
        for volume in data.volumeList:
            for surfaceGrp in volume.surfaceGroupList:
                tmpSurfaceList = surfaceGrp.surfaceList
                #if mode == milling: #commence par la dernière couche crée pour rentrer dans la matière
                #    tmpSurfaceList.reverse()
                for surface in tmpSurfaceList:
                    surfaceId = surface.surfaceId
                    for operation in surface.operationList:
                        if operation.tbe:
                            sortedFabricationSteps.append([operation.curveList, surfaceId, operation.fabricationMode, operation.ID])
                            try:
                                fabModes.index(operation.fabricationMode)
                            except ValueError:
                                fabModes.append(operation.fabricationMode)
                            for curve in operation.curveList:
                                for point in curve.pointList:
                                    totalPointCounter+=1
        print('\t\tThe operations have been sorted.')
        print('\t\tNumber of points detected: %d'%(totalPointCounter))
    except :
        message_error("Could not sort out the operations.")
    lstFM = []
    for fm in fabModes:
        lstFM.append(dictOfOperations[fm])
    print("\tFabrication modes detected : ", lstFM)
    return sortedFabricationSteps, totalPointCounter, fabModes


#def __OLDsort_operations(data:cls_data_structure):
#    totalPointCounter = 0
#    #Tri des opérations
#    try:
#        print('\tSorting of operations...')
#        #activeStep="Open data structure"
#        sortedFabricationSteps = []
#        #Selection de l'ordre de fabrication
#        fabOrder = data.sortedOperations
#        #activeStep = "Fabrication order:" + str(fabOrder)
#        for opeName in fabOrder:
#            volume:cls_volume
#            for volume in data.volumeList:
#                #activeStep = "Volume: %s"%(volume.volumeId)
#                volumeId = volume.volumeId
#                surfaceGrp:cls_surfaces_grp
#                for surfaceGrp in volume.surfaceGroupList:
#                    #activeStep = "Surface group: %s"%(surfaceGrp.surfacesGrpId)
#                    tmpSurfaceList = surfaceGrp.surfaceList
#                    #if mode == milling: #commence par la dernière couche crée pour rentrer dans la matière
#                    #    tmpSurfaceList.reverse()
#                    surface:cls_surface
#                    for surface in tmpSurfaceList:
#                        #activeStep = "Surface: %s"%(surface.surfaceId)
#                        surfaceId = surface.surfaceId
#                        operation:cls_operation
#                        for operation in surface.operationList:
#                            if operation.tbe:
#                                #activeStep = "Surface: %s Operation: %s"%(surface.surfaceId, operation.fabricationMode)
#                                fabricationMode = operation.fabricationMode
#                                if operation.name == opeName:
#                                    sortedFabricationSteps.append([operation.curveList, surfaceId, fabricationMode, operation.ID])
#                                    curve:cls_curve
#                                    #activeStep = "Operation name: %s Fabrication mode: %s"%(opeName, fabricationMode)
#                                    for curve in operation.curveList:
#                                        #activeStep = "Operation name: %s Curve: %s"%(opeName, curve.curveId)
#                                        point:cls_point
#                                        for point in curve.pointList:
#                                            #activeStep = "Point: %s"%(point.pointId)
#                                            totalPointCounter+=1
#        print('\t\tThe operations have been sorted.')
#        print('\t\tNumber of points detected: %d'%(totalPointCounter))
#    except :
#        #print('\t\tCould not sort out the operations. Active step: %s'%(activeStep))
#        message_error("Could not sort out the operations.")
#    return sortedFabricationSteps, totalPointCounter


def __format_data_in_string(dataPoint:cls_point, layerID:str, fabricationMode:int, curveID:str, totalDistanceActive:float, operationId:str, instruction:str):
    #vitesse selon le mode de fabrication et le type de mouvement
    #if dataPoint.moveType == approach:
    #    pointSpeed = dataStruct.machineParam.generics.approachSpeed
    #elif dataPoint.moveType == retract:
    #    pointSpeed = dataStruct.machineParam.generics.retractSpeed
    #else:
    #    if fabricationMode == fdmPerimeter:
    #        pointSpeed = dataStruct.machineParam.fdmFilament.perimeterSpeed
    #    elif fabricationMode == fdmInfill:
    #        pointSpeed = dataStruct.machineParam.fdmFilament.infillSpeed
    #    elif fabricationMode == milling :
    #        pointSpeed = dataStruct.machineParam.milling.toolSpeed
    #    elif fabricationMode == tapeLayingLaser:
    #        pointSpeed = dataStruct.machineParam.laserTape.toolSpeed
    #    elif fabricationMode == tapeLayingAirPulse:
    #        pointSpeed = dataStruct.machineParam.airTape.toolSpeed
    #    elif fabricationMode == fdmPelletPerimeter:
    #        pointSpeed = dataStruct.machineParam.fdmPellet.perimeterSpeed
    #    elif fabricationMode == fdmPelletInfill:
    #        pointSpeed = dataStruct.machineParam.fdmPellet.infillSpeed
    #    else:
    #        pointSpeed = dataStruct.machineParam.generics.toolSpeed

    #print("debug")
    #for word in [operationId, instruction, dictOfOperations[fabricationMode], layerID, curveID, dataPoint.pointId,dataPoint.coordinates.x, dataPoint.coordinates.y, dataPoint.coordinates.z,dataPoint.tangentialVector.vx, dataPoint.tangentialVector.vy, dataPoint.tangentialVector.vz,dataPoint.normalVector.vx, dataPoint.normalVector.vy, dataPoint.normalVector.vz,dataStruct.machineParam.generics.toolRotZ, dataStruct.machineParam.generics.toolTiltY,dataStruct.machineParam.generics.axis7thPosition, dataStruct.machineParam.generics.axis7thSpeed,dataPoint.distanceOnCurve, totalDistanceActive, dataPoint.speed,int(dataPoint.stopFlag)]:
    #    print(word)
    #print("fin debug")
    exportString = [
        operationId, instruction, dictOfOperations[fabricationMode], layerID, curveID, dataPoint.pointId,
        dataPoint.coordinates.x, dataPoint.coordinates.y, dataPoint.coordinates.z,
        dataPoint.tangentialVector.vx, dataPoint.tangentialVector.vy, dataPoint.tangentialVector.vz,
        dataPoint.normalVector.vx, dataPoint.normalVector.vy, dataPoint.normalVector.vz,
        env.dataStruct.machineParam.generics.toolRotZ, env.dataStruct.machineParam.generics.toolTiltY,
        #env.dataStruct.machineParam.generics.axis7thPosition, env.dataStruct.machineParam.generics.axis7thSpeed,
        dataPoint.pos7axis, env.dataStruct.machineParam.generics.axis7thSpeed,
        dataPoint.distanceOnCurve, totalDistanceActive,
        #old
        #pointSpeed,
        dataPoint.speed,
        int(dataPoint.stopFlag)
        ]
    #print("debug param")
    #print("tool state : ", dataPoint.ToolHeadState)
    for param in dataPoint.ToolHeadState:
        exportString.append(param)
    #    print(param)
    #print("fin debug param")
    return exportString