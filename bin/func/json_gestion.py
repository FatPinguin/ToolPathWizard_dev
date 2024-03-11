from .Classes import cls_data_structure, cls_volume, cls_surfaces_grp, cls_surface, cls_operation, cls_curve, cls_point, cls_vector, cls_coordinates, cls_machine_parameters, default_machine_settings
from .environment import salome, gstools, gg
#(import ToolPathWizard_dev.bin.func.environment as env


def create_dict_of_datastruct_for_json_dump(studyAdress, dataStruct:cls_data_structure):
#def create_dict_of_datastruct_for_json_dump(studyAdress):
    param:cls_machine_parameters = dataStruct.machineParam
    dictMachineParam = create_dict_of_toolstruct_for_json_dump(param)
    dictGeneratedOperations = {}
    for i in range(len(dataStruct.generatedOperations)):
        dictGeneratedOperations[i] = dataStruct.generatedOperations[i]
    dictSortedOperations = {}
    for i in range(len(dataStruct.sortedOperations)):
        dictSortedOperations[i] = dataStruct.sortedOperations[i]
    dictVolumeList = {}
    volume:cls_volume
    for volume in dataStruct.volumeList:
        dictSurfGroups = {}
        surfaceGroups:cls_surfaces_grp
        for surfaceGroups in volume.surfaceGroupList:
            dictSurfaceList = {}
            if surfaceGroups.typeGenerated:
                groupName = "Layer"
            else:
                groupName = "Cutter"
            surface:cls_surface
            for surface in surfaceGroups.surfaceList:
                dictOperation = {}
                operation:cls_operation
                #opeCounter = 1
                for operation in surface.operationList:
                    dictCurves = {}
                    opeName = operation.name#__operation_name(operation.fabricationMode)
                    try:
                        opIndex = dataStruct.generatedOperations.index(opeName)  #Vérifie que l'opération soit présente dans la liste des op générées
                        importOpe = True
                    except ValueError:
                        importOpe = False
                        print(f"The operation -{opeName}- is not included in the generated list. The operation is ignored on layer {surface.surfaceId}.")
                        print(f"Op list : {dataStruct.generatedOperations}\n")
                    if importOpe:
                        curve:cls_curve
                        for curve in operation.curveList:
                            dictPoint = {}
                            point:cls_point
                            for point in curve.pointList:
                                dictCoordinates = {'x' : point.coordinates.x, 'y' : point.coordinates.y, 'z' : point.coordinates.z}
                                dictNormalVector = {'vx' : point.normalVector.vx, 'vy' : point.normalVector.vy, 'vz' : point.normalVector.vz}
                                dictTangentialVector = {'vx' : point.tangentialVector.vx, 'vy' : point.tangentialVector.vy, 'vz' : point.tangentialVector.vz}
                                dictPoint["Point %s"%(point.pointId)] = {
                                    'Point ID' : point.pointId,
                                    'Distance on curve' : point.distanceOnCurve,
                                    'Move type' : point.moveType,
                                    'Security surface ID' : point.securitySurfaceId,
                                    'Coordinates' : dictCoordinates,
                                    'Normal vector' : dictNormalVector,
                                    'Tangential vector' : dictTangentialVector,
                                    'Stop flag' : point.stopFlag,
                                    'Speed' : point.speed,
                                    'Dist from last point' : point.lstPtDist,
                                    '7th axis position' : point.pos7axis,
                                    'Tool head state' : point.ToolHeadState #dictToolHeadState,
                                }
                            dictCurves['Trajectory %s'%(curve.curveId)] = {
                                'Curve ID' : curve.curveId,
                                'Curve length' : curve.curveLength,
                                'Layer ID' : curve.layerId,
                                'Cutting Surface ID' : curve.cuttingSurfaceId,
                                'Discretisation increment' : curve.increment,
                                'Tool positioning' : curve.prePosTool,
                                'Point list' : dictPoint
                            }
                        dictOperation[opeName] = {'Fabrication mode' : operation.fabricationMode, 'Operation ID' : operation.ID, 'To be exported' : operation.tbe, 'Operation order' : operation.order, 'Curve list' : dictCurves}
                dictSurfaceList['%s %s'%(groupName, surface.surfaceId)] = {'Surface ID' : surface.surfaceId, 'Operation list' : dictOperation}
            dictSurfGroups['%s group %s'%(groupName, surfaceGroups.surfacesGrpId)] = {
                'Tool type' : surfaceGroups.typeGenerated, 
                'Group ID' : surfaceGroups.surfacesGrpId,
                'Original ID' : surfaceGroups.originalSurfaceId,
                'Increment' : surfaceGroups.increment,
                'Translation path ID' : surfaceGroups.translationPathId,
                'Surface list' : dictSurfaceList
            }
        dictVolumeList['Volume %s'%(volume.volumeId)] = {'Volume ID' : volume.volumeId, 'Surface groups' : dictSurfGroups}
    dictDataStruct = {'Study adress' : salome.salome_study.myStudyName, 'Machine parameters' : dictMachineParam, 'Volume liste' : dictVolumeList, 'Generated operations' : dictGeneratedOperations}
    return dictDataStruct


def create_dict_of_toolstruct_for_json_dump(param:cls_machine_parameters):
    dictMachineParam = {
        'Generic' : {
            'toolRotZ' : param.generics.toolRotZ, 
            'toolTiltY' : param.generics.toolTiltY,
            'axis7thPosition' : param.generics.axis7thPosition,
            'axis7thSpeed' : param.generics.axis7thSpeed,
            'toolSpeed' : param.generics.toolSpeed,
            'approachSpeed' : param.generics.approachSpeed,
            'retractSpeed' : param.generics.retractSpeed,
            'travelSpeed' : param.generics.travelSpeed,
            'securityDistance' : param.generics.securityDistance,
            'increment' : param.generics.incr
        },
        'FDM pellets' : {
            'screwSpeed' : param.fdmPellet.screwSpeed,
            'infillSpeed' : param.fdmPellet.infillSpeed,
            'perimeterSpeed' : param.fdmPellet.perimeterSpeed,
            'extruderTemp' : param.fdmPellet.extruderTemp,
            'distanceToRetract' : param.fdmPellet.distanceToRetract,
            'extrusionDiameter' : param.fdmPellet.extrusionDiameter
        },
        'FDM filament' : {
            'infillSpeed' : param.fdmFilament.infillSpeed,
            'perimeterSpeed' : param.fdmFilament.perimeterSpeed,
            'relativeFilamentSpeed' : param.fdmFilament.relativeFilamentSpeed,
            'filamentSpeed' : param.fdmFilament.filamentSpeed,
            'extruderTemp' : param.fdmFilament.extruderTemp,
            'extrusionDiameter' : param.fdmFilament.extrusionDiameter
        },
        'Milling' : {
            'toolSpeed' : param.milling.toolSpeed,
            'spindleSpeed' : param.milling.spindleSpeed,
            'toolDiameter' : param.milling.toolDiameter,
            'toolCorrection' : param.milling.toolCorrection
        },
        'Laser Tape' : {
            'minimumTrajectoryLength' : param.laserTape.minimumTrajectoryLength,
            'toolSpeed' : param.laserTape.toolSpeed,
            'laserStartingDistance' : param.laserTape.laserStartingDistance,
            'laserStopingDistance' : param.laserTape.laserStopingDistance,
            'cuttingDistance' : param.laserTape.cuttingDistance,
            'laserPower' : param.laserTape.laserPower,
            'offset' : param.laserTape.offset,
            'incr' : param.laserTape.incr,
            'layIncr' : param.laserTape.layIncr,
            'cutIncr' : param.laserTape.cutIncr
        },
        'Air Tape' : {
            'minimumTrajectoryLength' : param.airTape.minimumTrajectoryLength,
            'toolSpeed' : param.airTape.toolSpeed,
            'airStartingDistance' : param.airTape.airStartingDistance,
            'rollerDownDistance' : param.airTape.rollerDownDistance,
            'cuttingDistance' : param.airTape.cuttingDistance,
            'feedRate' : param.airTape.feedRate,
            'securityDiscretisation' : param.airTape.securityDiscretisation
        } 
    }
    return dictMachineParam


def convert_dict_to_data_structure(dictDataStruct:dict):
    dataStruct = cls_data_structure("", default_machine_settings())
    dataStruct.studyAdress = dictDataStruct['Study adress']
    import_dict_tool_in_tool_struct(dataStruct, dictDataStruct)
    print("\tNb keys:%d\t"%(len(dictDataStruct['Generated operations'].keys())), dictDataStruct['Generated operations'].keys())
    for opeKey in dictDataStruct['Generated operations'].keys():
        dataStruct.generatedOperations.append(dictDataStruct['Generated operations'][opeKey])
    print("\tOperation list:", dataStruct.generatedOperations)
    for volumeKey in dictDataStruct['Volume liste'].keys():
        volume = cls_volume(None)
        dictVolume = dictDataStruct['Volume liste'][volumeKey]
        volume.volumeId = dictVolume['Volume ID']
        for surfGroupKey in dictVolume['Surface groups'].keys():
            surfGroup = cls_surfaces_grp(None, None, None, None, None, None)
            dictSurfGroup = dictVolume['Surface groups'][surfGroupKey]
            surfGroup.typeGenerated = dictSurfGroup['Tool type']
            surfGroup.surfacesGrpId = dictSurfGroup['Group ID']
            surfGroup.originalSurfaceId = dictSurfGroup['Original ID']
            surfGroup.increment = dictSurfGroup['Increment']
            surfGroup.translationPathId = dictSurfGroup['Translation path ID']
            for surfKey in dictSurfGroup['Surface list'].keys():
                surface = cls_surface(None)
                dictSurf = dictSurfGroup['Surface list'][surfKey]
                surface.surfaceId = dictSurf['Surface ID']
                for opeKey in dictSurf['Operation list'].keys():
                    try:
                        opIndex = dataStruct.generatedOperations.index(opeKey)  #Vérifie que l'opération soit présente dans la liste des op générées
                        importOpe = True
                    except ValueError:
                        importOpe = False
                        print('\tThe operation --%s-- is not included in the generated list. The operation is ignored.'%(opeKey))
                    if importOpe:
                        operation = cls_operation(None, None)
                        dictOpe = dictSurf['Operation list'][opeKey]
                        operation.fabricationMode = dictOpe['Fabrication mode']
                        operation.ID = dictOpe['Operation ID']
                        operation.tbe = dictOpe['To be exported']
                        operation.name = opeKey
                        operation.order = dictOpe['Operation order']
                        for curveKey in dictOpe['Curve list'].keys():
                            curve = cls_curve(None, None, None, None, None)
                            dictCurve = dictOpe['Curve list'][curveKey]
                            curve.curveId = dictCurve['Curve ID']
                            curve.curveLength = dictCurve['Curve length']
                            curve.layerId = dictCurve['Layer ID']
                            curve.cuttingSurfaceId = dictCurve['Cutting Surface ID']
                            curve.increment = dictCurve['Discretisation increment']
                            curve.prePosTool = dictCurve['Tool positioning']
                            for pointKey in dictCurve['Point list'].keys():
                                point = cls_point(None, None, None, None, None, None, None, None, None, None, None)
                                dictPoint = dictCurve['Point list'][pointKey]
                                point.pointId = dictPoint['Point ID']
                                point.distanceOnCurve = dictPoint['Distance on curve']
                                point.moveType = dictPoint['Move type']
                                point.securitySurfaceId = dictPoint['Security surface ID']
                                point.stopFlag = dictPoint['Stop flag']
                                point.speed = dictPoint['Speed']
                                point.lstPtDist = dictPoint['Dist from last point']
                                point.pos7axis = dictPoint['7th axis position']
                                point.coordinates = cls_coordinates([dictPoint['Coordinates']['x'], dictPoint['Coordinates']['y'], dictPoint['Coordinates']['z']])
                                point.normalVector = cls_vector([dictPoint['Normal vector']['vx'], dictPoint['Normal vector']['vy'], dictPoint['Normal vector']['vz']])
                                point.tangentialVector = cls_vector([dictPoint['Tangential vector']['vx'], dictPoint['Tangential vector']['vy'], dictPoint['Tangential vector']['vz']])
                                point.ToolHeadState = dictPoint['Tool head state']
                                curve.pointList.append(point)
                            operation.curveList.append(curve)
                        surface.operationList.append(operation)
                surfGroup.surfaceList.append(surface)
            volume.surfaceGroupList.append(surfGroup)
        dataStruct.volumeList.append(volume)
    return dataStruct


def import_dict_tool_in_tool_struct(dataStruct:cls_data_structure, dictDataStruct:dict):
    ###Generic tool
    dataStruct.machineParam.generics.toolRotZ = dictDataStruct['Machine parameters']['Generic']['toolRotZ']
    dataStruct.machineParam.generics.toolTiltY = dictDataStruct['Machine parameters']['Generic']['toolTiltY']
    dataStruct.machineParam.generics.axis7thPosition = dictDataStruct['Machine parameters']['Generic']['axis7thPosition']
    dataStruct.machineParam.generics.axis7thSpeed = dictDataStruct['Machine parameters']['Generic']['axis7thSpeed']
    dataStruct.machineParam.generics.toolSpeed = dictDataStruct['Machine parameters']['Generic']['toolSpeed']
    dataStruct.machineParam.generics.approachSpeed = dictDataStruct['Machine parameters']['Generic']['approachSpeed']
    dataStruct.machineParam.generics.retractSpeed = dictDataStruct['Machine parameters']['Generic']['retractSpeed']
    dataStruct.machineParam.generics.travelSpeed = dictDataStruct['Machine parameters']['Generic']['travelSpeed']
    dataStruct.machineParam.generics.securityDistance = dictDataStruct['Machine parameters']['Generic']['securityDistance']
    dataStruct.machineParam.generics.incr = dictDataStruct['Machine parameters']['Generic']['increment']
    ###Pellets FDM
    dataStruct.machineParam.fdmPellet.screwSpeed = dictDataStruct['Machine parameters']['FDM pellets']['screwSpeed']
    dataStruct.machineParam.fdmPellet.infillSpeed = dictDataStruct['Machine parameters']['FDM pellets']['infillSpeed']
    dataStruct.machineParam.fdmPellet.perimeterSpeed = dictDataStruct['Machine parameters']['FDM pellets']['perimeterSpeed']
    dataStruct.machineParam.fdmPellet.extruderTemp = dictDataStruct['Machine parameters']['FDM pellets']['extruderTemp']
    dataStruct.machineParam.fdmPellet.distanceToRetract = dictDataStruct['Machine parameters']['FDM pellets']['distanceToRetract']
    dataStruct.machineParam.fdmPellet.extrusionDiameter = dictDataStruct['Machine parameters']['FDM pellets']['extrusionDiameter']
    ###Filament FDM
    dataStruct.machineParam.fdmFilament.infillSpeed = dictDataStruct['Machine parameters']['FDM filament']['infillSpeed']
    dataStruct.machineParam.fdmFilament.perimeterSpeed = dictDataStruct['Machine parameters']['FDM filament']['perimeterSpeed']
    dataStruct.machineParam.fdmFilament.relativeFilamentSpeed = dictDataStruct['Machine parameters']['FDM filament']['relativeFilamentSpeed']
    dataStruct.machineParam.fdmFilament.filamentSpeed = dictDataStruct['Machine parameters']['FDM filament']['filamentSpeed']
    dataStruct.machineParam.fdmFilament.extruderTemp = dictDataStruct['Machine parameters']['FDM filament']['extruderTemp']
    dataStruct.machineParam.fdmFilament.extrusionDiameter = dictDataStruct['Machine parameters']['FDM filament']['extrusionDiameter']
    ###Milling
    dataStruct.machineParam.milling.toolSpeed = dictDataStruct['Machine parameters']['Milling']['toolSpeed']
    dataStruct.machineParam.milling.spindleSpeed = dictDataStruct['Machine parameters']['Milling']['spindleSpeed']
    dataStruct.machineParam.milling.toolDiameter = dictDataStruct['Machine parameters']['Milling']['toolDiameter']
    dataStruct.machineParam.milling.toolCorrection = dictDataStruct['Machine parameters']['Milling']['toolCorrection']
    ###Laser tape
    dataStruct.machineParam.laserTape.minimumTrajectoryLength = dictDataStruct['Machine parameters']['Laser Tape']['minimumTrajectoryLength']
    dataStruct.machineParam.laserTape.toolSpeed = dictDataStruct['Machine parameters']['Laser Tape']['toolSpeed']
    dataStruct.machineParam.laserTape.laserStartingDistance = dictDataStruct['Machine parameters']['Laser Tape']['laserStartingDistance']
    dataStruct.machineParam.laserTape.laserStopingDistance = dictDataStruct['Machine parameters']['Laser Tape']['laserStopingDistance']
    dataStruct.machineParam.laserTape.cuttingDistance = dictDataStruct['Machine parameters']['Laser Tape']['cuttingDistance']
    dataStruct.machineParam.laserTape.laserPower = dictDataStruct['Machine parameters']['Laser Tape']['laserPower']
    dataStruct.machineParam.laserTape.offset = dictDataStruct['Machine parameters']['Laser Tape']['offset']
    dataStruct.machineParam.laserTape.incr = dictDataStruct['Machine parameters']['Laser Tape']['incr']
    dataStruct.machineParam.laserTape.layIncr = dictDataStruct['Machine parameters']['Laser Tape']['layIncr']
    dataStruct.machineParam.laserTape.cutIncr = dictDataStruct['Machine parameters']['Laser Tape']['cutIncr']
    ###Air tape
    dataStruct.machineParam.airTape.minimumTrajectoryLength = dictDataStruct['Machine parameters']['Air Tape']['minimumTrajectoryLength']
    dataStruct.machineParam.airTape.toolSpeed = dictDataStruct['Machine parameters']['Air Tape']['toolSpeed']
    dataStruct.machineParam.airTape.airStartingDistance = dictDataStruct['Machine parameters']['Air Tape']['airStartingDistance']
    dataStruct.machineParam.airTape.rollerDownDistance = dictDataStruct['Machine parameters']['Air Tape']['rollerDownDistance']
    dataStruct.machineParam.airTape.cuttingDistance = dictDataStruct['Machine parameters']['Air Tape']['cuttingDistance']
    dataStruct.machineParam.airTape.feedRate = dictDataStruct['Machine parameters']['Air Tape']['feedRate']
    dataStruct.machineParam.airTape.securityDiscretisation = dictDataStruct['Machine parameters']['Air Tape']['securityDiscretisation']
    return


def display_objects_from_dataStruct(objectStr:str, uiProgressBar, dataStruct:cls_data_structure):
#def display_objects_from_dataStruct(objectStr:str, uiProgressBar):
    pointCount = 0
    curveCount = 0
    surfaceCount = 0
    volume:cls_volume
    surfaceGroups:cls_surfaces_grp
    surface:cls_surface
    operation:cls_operation
    curve:cls_curve
    point:cls_point
    for volume in dataStruct.volumeList:
        for surfaceGroups in volume.surfaceGroupList:
            if surfaceGroups.typeGenerated: # = "Layers"
                surfaceCount+=len(surfaceGroups.surfaceList)
            for surface in surfaceGroups.surfaceList:
                for operation in surface.operationList:
                        curveCount+=len(operation.curveList)
                        for curve in operation.curveList:
                                pointCount+=len(curve.pointList)
    count = 0
    if objectStr == "layers" and surfaceCount:
        for volume in dataStruct.volumeList:
            for surfaceGroups in volume.surfaceGroupList:
                if surfaceGroups.typeGenerated:
                    for surface in surfaceGroups.surfaceList:
                        try:
                            gstools.displayShapeByEntry(surface.surfaceId)#, color=[0,255,0])
                        except:
                            print("Didn't find surface %s in study"%(surface.surfaceId))
                        count+=1
                        uiProgressBar.setValue(count/surfaceCount*100)
    elif objectStr == "trajectoires" and curveCount:
        for volume in dataStruct.volumeList:
            for surfaceGroups in volume.surfaceGroupList:
                if surfaceGroups.typeGenerated: # = "Layers"
                    for surface in surfaceGroups.surfaceList:
                        for operation in surface.operationList:
                                for curve in operation.curveList:
                                    try:
                                        gstools.displayShapeByEntry(curve.curveId, color=[255,0,0])
                                        gg.setVectorsMode(curve.curveId, True)
                                    except:
                                        print("Didn't find curve %s in study"%(curve.curveId))
                                    count+=1
                                    uiProgressBar.setValue(count/curveCount*100)
    elif objectStr == "points" and pointCount:
        for volume in dataStruct.volumeList:
            for surfaceGroups in volume.surfaceGroupList:
                if surfaceGroups.typeGenerated: # = "Layers"
                    for surface in surfaceGroups.surfaceList:
                        for operation in surface.operationList:
                                for curve in operation.curveList:
                                    for point in curve.pointList:
                                        try:
                                            gstools.displayShapeByEntry(point.pointId, color=[0,0,255])
                                        except:
                                            print("Didn't find point %s in study"%(point.pointId))
                                        count+=1
                                        uiProgressBar.setValue(count/pointCount*100)
    return