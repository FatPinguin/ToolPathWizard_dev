from .environment import geompy, salome
from .Classes import cls_surface, cls_operation, cls_curve
from ..viz.user_com import message_error
from .common_variables import generalContinuityTolerance, wireContinuityTolerance, succes, fail, fdmPerimeter, fdmInfill, milling, tapeLayingAirPulse, tapeLayingLaser, fdmPelletPerimeter, fdmPelletInfill, fdmFiberInfill, fdmFiberPerimeter, generic
import ToolPathWizard_dev.bin.func.environment as env

def operation_generator(fabricationMode:int, dataLayerList:list, dataToolList:list, evenUnevenOption:bool, skipOption:bool, uiProgressBar, positionTool):
    groupName = __operation_name(fabricationMode)
    env.dataStruct.generatedOperations.append(groupName)
    print("\tname: ", groupName)
    layerCount = 1
    dataLayer:cls_surface
    dataTool:cls_surface
    progressCount=0
    for dataLayer in dataLayerList:
        if skipOption:
            if evenUnevenOption == False and layerCount%2 == 1 : #1 pour impaire
                layerCount += 1
                continue
            elif evenUnevenOption == True and layerCount%2 == 0 : #0 pour paire
                layerCount += 1
                continue
        layer = salome.IDToObject(dataLayer.surfaceId)
        dataOperation = cls_operation(fabricationMode, None)
        wireGroupIsPublished = False
        wireCount = 0
        for dataTool in dataToolList:
            tool = salome.IDToObject(dataTool.surfaceId)
            try:
                edgeCompound = geompy.MakeSection(layer, tool)
            except RuntimeError:
                print(f"MakeSection failed on layer: {dataLayer.surfaceId} with cutter: {dataTool.surfaceId}")
                print(f"This wire will be skipped.")
                continue
            edgeList = geompy.ExtractShapes(edgeCompound, geompy.ShapeType["EDGE"], True)
            if wireGroupIsPublished == False and (len(edgeList) or str(edgeCompound.GetShapeType()) == "EDGE"):
                wireGroup = geompy.MakeCompound([])#geompy.CreateGroup(layer, geompy.ShapeType["WIRE"], "Trajectories")
                wireGroupId = geompy.addToStudyInFather(layer, wireGroup, groupName)#wireGroup.GetEntry()
                dataOperation.ID = wireGroupId
                dataOperation.name = groupName
                dataOperation.order = str(env.dataStruct.generatedOperations.index(groupName))
                wireGroupIsPublished = True
            if len(edgeList):
                try:
                    wire = geompy.MakeWire(edgeList, wireContinuityTolerance)#generalContinuityTolerance) #TODO Rendre parametrable la tolérance de continuité pour MakeWire
                except:
                    message_error(f"MakeWire failed. Could not build desired wire. \nLayer ID: {dataLayer.surfaceId} \nCutter ID: {dataTool.surfaceId} \nNumber of edges: {len(edgeList)}\nThis wire will be skipped.")
                    continue
                if wire == None and len(edgeList) != 0 :
                    print("Couldn't build a wire.") #TODO - Gérer les cas ou plusieurs wires sont à créer. Détecter les discontinuités, etc. Si ilots de faces détecters précédement peut-etre pas besoin. Supprimer alors un étage de liste.
                elif wire == None and len(edgeList) == 0 :
                    print("No intersection detected between layer : %s and tool : %s" %(dataLayer.surfaceId, dataTool.surfaceId))
                else :
                    wireId = geompy.addToStudyInFather(wireGroup, wire, "Wire_%d"%(wireCount))
                    wireLength = geompy.BasicProperties(wire)[0]
            elif str(edgeCompound.GetShapeType()) == "EDGE":
                wire = edgeCompound
                wireId = geompy.addToStudyInFather(wireGroup, wire, "Wire_%d"%(wireCount))
                wireLength = geompy.BasicProperties(wire)[0]
            else:
                continue
            dataOperation.add_curve_to_operation(cls_curve(wireId, wireLength, dataLayer.surfaceId, dataTool.surfaceId, positionTool))
            wireCount += 1
            progressCount +=1
            uiProgressBar.setValue(progressCount/(len(dataLayerList)*len(dataToolList))*100)
        dataLayer.add_operation_to_layer(dataOperation)
        uiProgressBar.setValue(layerCount/len(dataLayerList)*100)
        layerCount += 1
    print("\tOperation list: ", env.dataStruct.generatedOperations)
    return succes #For "succes" #TODO - Gérer les codes erreur (si possible)


def __operation_name(fabricationMode:int): #For folder name
    if fabricationMode == fdmPerimeter :
        return __increment_name("3D printing filament outline")
    elif fabricationMode == fdmInfill:
        return __increment_name("3D printing filament infill")
    elif fabricationMode == milling:
        return __increment_name("Milling")
    elif fabricationMode == tapeLayingLaser:
        return __increment_name("Laser assisted fiber placement")
    elif fabricationMode == tapeLayingAirPulse:
        return __increment_name("Composite automated tape layup")
    elif fabricationMode == fdmPelletPerimeter :
        return __increment_name("3D printing pellet outline")
    elif fabricationMode == fdmPelletInfill:
        return __increment_name("3D printing pellet infill")
    elif fabricationMode == fdmFiberInfill:
        return __increment_name("Continuous fiber printing infill")
    elif fabricationMode == fdmFiberPerimeter:
        return __increment_name("Continuous fiber printing outline")
    elif fabricationMode == generic:
        return __increment_name("General trajectory")
    else:
        message_error("Mode error")
        return __increment_name("No specification")
    

def __increment_name(name:str, index=0):#env.dataStruct.lastOperationIndex):
    nameIndexed = name + " %d"%(index)
    try :
        env.dataStruct.generatedOperations.index(nameIndexed)
        return __increment_name(name, index+1)  #Si l'opération est trouvée, on recherche avec l'index suivant
    except ValueError:
        return nameIndexed
