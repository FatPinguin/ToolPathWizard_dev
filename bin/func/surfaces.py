from ..func.environment import salome, gstools, geompy
import ToolPathWizard_dev.bin.func.environment as env
from ..func.Classes import cls_surfaces_grp, cls_volume, cls_surface
from ..viz.user_com import update_progressBar, message_error, message_information_no_main


def main_surfaces(self):#increment, volumes, volumesIds, shells, trajectory, numberOfElements, isCreatedByOffset, isLayersFlag, UIprogress, firstLayerMethod):
    opCount = 0
    numberOfOperations = len(self.volumes)*len(self.shells)*self.numberOfElements
    for i in range(len(self.volumes)):
        volume = self.volumes[i]
        volumeID = self.volumesIds[i]
        dataVolume:cls_volume = env.dataStruct.add_volume_to_data_struct(cls_volume(volumeID))
        groupName, surfaceName = surface_denomination(self.isLayersFlag)
        group = geompy.MakeCompound([])
        groupId = geompy.addToStudyInFather(volume, group, groupName)
        for shell in self.shells:
            if self.isCreatedByOffset == False:
                dataSurfaceGroup = cls_surfaces_grp(groupId, self.isLayersFlag, shell.GetEntry(), self.increment, self.isCreatedByOffset, self.trajectory[0].GetEntry())
            else:
                dataSurfaceGroup = cls_surfaces_grp(groupId, self.isLayersFlag, shell.GetEntry(), self.increment, self.isCreatedByOffset, None)
            surfacesList, dataSurfaceGroup, opCount = __generate_surfaces(group, volume, shell, dataSurfaceGroup, numberOfOperations, self.numberOfElements, surfaceName, self.increment, self.ui.progressBar, opCount, self.firstLayerMethod, self.isCreatedByOffset, self.trajectory)
            dataVolume.add_grp_surface_to_volume(dataSurfaceGroup)
    return


def surface_denomination(isLayersFlag:bool):
    if isLayersFlag:
        groupName = "Layer group"
        surfaceName = "Layer"
    else:
        groupName = "Cutter group"
        surfaceName = "Cutter"
    return groupName, surfaceName


def __generate_surfaces(folder, volume, shell, dataSurfaceGroup:cls_surfaces_grp, numberOfOperations:int, numberOfElements:int, surfaceName, increment, UIprogress, opCount, firstLayerMethod, isCreatedByOffset, trajectory):
    surfacesList = []
    step = __first_layer_increment(firstLayerMethod, increment)
    for stepNumber in range(numberOfElements):
        if step == 0:
            newSurfList = [geompy.MakeCommon(volume, shell, False)] #, theName='toBeDeleted_first'
        else:
            newSurfList = __new_surface(isCreatedByOffset, trajectory, volume, shell, step)
        if newSurfList != None:
            surfCount = 1
            for newSurf in newSurfList:
                if len(newSurfList) > 1:
                    surfName = "%s_%d.%d"%(surfaceName, stepNumber, surfCount)
                    surfCount+=1
                else:
                    surfName = "%s_%d"%(surfaceName, stepNumber)
                objID = geompy.addToStudyInFather(folder, newSurf, surfName)
                #destroy_temporary_object(newSurf)
                newSurf=salome.IDToObject(objID)
                dataSurfaceGroup.add_surface_to_group(cls_surface(objID))
                surfacesList.append(newSurf)
                if step == 0 and str(newSurf.GetShapeType()) == "FACE":
                    vnorm = geompy.GetNormal(newSurf)
                    if vnorm is None:
                        print(f"GetNormal(face:{newSurf.GetEntry()}) failed")
                        raise RuntimeError
                    else:
                        geompy.addToStudyInFather(newSurf, vnorm, f"Normale to face {newSurf.GetEntry()}")
                        gstools.displayShapeByEntry(newSurf.GetEntry(), color=[0,255,0])
                        message_information_no_main("Remember to check the first layer orientation.\nIf needed use change orientation tool on it without creating a copy.", "Reminder:", "info")
        opCount += 1
        update_progressBar(UIprogress, opCount/numberOfOperations*100)
        step += increment
    return surfacesList, dataSurfaceGroup, opCount


def __first_layer_increment(firstLayerMethod, increment):
    if firstLayerMethod == 0:    #start at first increment = 0, include ref as first surface = 1, first is half increment = 2
        return increment
    elif firstLayerMethod == 1:
        return 0
    elif firstLayerMethod == 2:
        return increment/2


def __new_surface(isCreatedByOffset, trajectory, volume, obj, step):
    if isCreatedByOffset:
        surf = geompy.Offset(obj, step, True)
    else:
        surf = geompy.TranslateVectorDistance(obj, trajectory[0], step, True)
    newSurf = geompy.MakeCommon(volume, surf, False)    #, theName='toBeDeleted'
    if geompy.NumberOfSubShapes(newSurf, geompy.ShapeType["SHELL"]) > 1:
        newSurfList = geompy.ExtractShapes(newSurf, geompy.ShapeType["SHELL"], True)
        return newSurfList
    if geompy.BasicProperties(newSurf)[1]: #Surface de l'objet --> vérifie qu'il éxiste
        return [newSurf]
    else:
        return None