from ..func.environment import salome, gstools, geompy
#import ToolPathWizard_dev.bin.func.environment as env
#from .main_viz import mainWindow

from PyQt5 import QtCore, QtWidgets

from ...assets.Interface_QT.Layers_creator import Ui_Dialog_layersAndCutters
from .generic_viz import hide_object, selection_method, get_value_in_line_edit, selection_indicator
from ..func.common_variables import volumesTypesList, surfacesTypesList, vectorTypesList, cfrDlfVersion
#from ..func.Classes import cls_surfaces_grp, cls_volume, cls_surface
from .user_com import update_progressBar, message_information_no_main
from ..func.surfaces import main_surfaces
from ..func.environment import machineParameters

class tool_create_layersAndCutters:
    def __init__(self, mainApp):
        #self.mainApp:mainWindow=mainApp
        self.mainApp=mainApp
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog_layersAndCutters()
        self.ui.setupUi(self.window)
        self.ui.pushButton_Validation.clicked.connect(self.__main)
        self.ui.pushButton_return.clicked.connect(self.__close_window)
        self.advancement = 0
        self.ui.progressBar.setValue(self.advancement)
        self.ui.radioButton_createLayers.clicked.connect(self.__layers_method)
        self.ui.radioButton_createCuttingTools.clicked.connect(self.__cutters_method)
        self.ui.radioButton_offset.clicked.connect(self.__offset_method)
        self.ui.radioButton_translation.clicked.connect(self.__translation_method)
        self.ui.radioButton_noOption.clicked.connect(self.__start_at_first_increment_method)
        self.ui.radioButton_refIsFirst.clicked.connect(self.__ref_is_first_layer_method)
        self.ui.radioButton_firstIsHalfStep.clicked.connect(self.__first_is_half_increment_method)
        self.ui.pushButton_setectVolume.clicked.connect(self.__select_volume)
        self.ui.pushButton_selectSurface.clicked.connect(self.__select_surfaces)
        self.ui.pushButton_translationTrajectory.clicked.connect(self.__select_trajectory)
        self.ui.lineEdit_increment.editingFinished.connect(self.__get_increment)
        self.ui.lineEdit_numberOfSurfaces.editingFinished.connect(self.__get_number_of_elements)
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        button_group_tool = QtWidgets.QButtonGroup(self.window)
        button_group_tool.setExclusive(True)
        button_group_tool.addButton(self.ui.radioButton_createLayers)
        button_group_tool.addButton(self.ui.radioButton_createCuttingTools)
        button_group_method = QtWidgets.QButtonGroup(self.window)
        button_group_method.setExclusive(True)
        button_group_method.addButton(self.ui.radioButton_offset)
        button_group_method.addButton(self.ui.radioButton_translation)
        button_group_firstL = QtWidgets.QButtonGroup(self.window)
        button_group_firstL.setExclusive(True)
        button_group_firstL.addButton(self.ui.radioButton_refIsFirst)
        button_group_firstL.addButton(self.ui.radioButton_firstIsHalfStep)
        button_group_firstL.addButton(self.ui.radioButton_noOption)
        objectListToHide = [self.ui.progressBar, self.ui.radioButton_offset, self.ui.radioButton_translation,
            self.ui.radioButton_noOption, self.ui.radioButton_refIsFirst, self.ui.radioButton_firstIsHalfStep,
            self.ui.label_volume, self.ui.pushButton_setectVolume, self.ui.label_volumValidation, self.ui.label_volumeEntry,
            self.ui.label_referntialSurface, self.ui.pushButton_selectSurface, self.ui.label_surfaceValidation, self.ui.label_surfaceEntry,
            self.ui.label_increment, self.ui.lineEdit_increment, self.ui.label_incrementValidation,
            self.ui.label_numberOfSurfaces, self.ui.lineEdit_numberOfSurfaces, self.ui.label_numberOfSurfacesValidation,
            self.ui.label_translationTrajectory, self.ui.pushButton_translationTrajectory, self.ui.label_translationTrajectoryValidation, self.ui.label_translationTrajectoryEntry
            ]
        self.uiParameters = [self.ui.label_volume, self.ui.pushButton_setectVolume, self.ui.label_volumValidation, self.ui.label_volumeEntry,
            self.ui.label_referntialSurface, self.ui.pushButton_selectSurface, self.ui.label_surfaceValidation, self.ui.label_surfaceEntry,
            self.ui.label_increment, self.ui.lineEdit_increment, self.ui.label_incrementValidation,
            self.ui.label_numberOfSurfaces, self.ui.lineEdit_numberOfSurfaces, self.ui.label_numberOfSurfacesValidation,
            self.ui.label_translationTrajectory, self.ui.pushButton_translationTrajectory, self.ui.label_translationTrajectoryValidation, self.ui.label_translationTrajectoryEntry]
        hide_object(objectListToHide, True)
        self.volumes:list = None
        self.volumesIds:list = None
        self.shells:list = None
        self.shellsIds:list = None
        self.trajectory:list = None
        self.trajectoryId:list = None
        self.isLayersFlag:bool = None    #layers = True, cutters = False
        self.isCreatedByOffset:bool = None    #offset = True, translation = False
        self.firstLayerMethod:int = None    #start at first increment = 0, include ref as first surface = 1, first is half increment = 2
        self.increment:float = None
        self.numberOfElements:int = None
        self.numberOfOperations = None
        self.opCount = 0


    def __main(self):
        if self.volumes != None and self.shells != None:
            hide_object([self.ui.progressBar], False)
            main_surfaces(self)#self.increment, self.volumes, self.volumesIds, self.shells, self.trajectory, self.numberOfElements, self.isCreatedByOffset, self.isLayersFlag, self.ui.progressBar, self.firstLayerMethod)
            #self.numberOfOperations = len(self.volumes)*len(self.shells)*self.numberOfElements
            #for i in range(len(self.volumes)):
            #    volume = self.volumes[i]
            #    volumeID = self.volumesIds[i]
            #    #dataVolume = cls_volume(volumeID)
            #    dataVolume:cls_volume = env.dataStruct.add_volume_to_data_struct(cls_volume(volumeID))
            #    if self.isLayersFlag:
            #        groupName = "Layer group"
            #        self.surfaceName = "Layer"
            #    else:
            #        groupName = "Cutter group"
            #        self.surfaceName = "Cutter"
            #    group = geompy.MakeCompound([])
            #    groupId = geompy.addToStudyInFather(volume, group, groupName)
            #    for shell in self.shells:
            #        if self.isCreatedByOffset == False:
            #            dataSurfaceGroup = cls_surfaces_grp(groupId, self.isLayersFlag, shell.GetEntry(), self.increment, self.isCreatedByOffset, self.trajectory[0].GetEntry())
            #        else:
            #            dataSurfaceGroup = cls_surfaces_grp(groupId, self.isLayersFlag, shell.GetEntry(), self.increment, self.isCreatedByOffset, None)
            #        surfacesList, dataSurfaceGroup = self.__generate_surfaces(group, volume, shell, dataSurfaceGroup)
            #        dataVolume.add_grp_surface_to_volume(dataSurfaceGroup)
            self.__close_window()
        else:
            message_information_no_main("Aucune donnée à traiter")


    def __close_window(self):
        print("End of layers and cutters creation.")
        print("______________________________________________________________________________\n")
        if salome.sg.hasDesktop():
            salome.sg.updateObjBrowser()
        self.mainApp.win.show()
        self.window.close()


    def __select_volume(self):
        self.volumes, self.volumesIds, check = selection_method(self.mainApp, self.ui.label_volumValidation, self.ui.label_volumeEntry, volumesTypesList)
    

    def __select_surfaces(self):
        self.shells, self.shellsIds, check = selection_method(self.mainApp, self.ui.label_surfaceValidation, self.ui.label_surfaceEntry, surfacesTypesList)
        if len(self.shells)>1:
            shell = geompy.MakeShell(self.shells)
            if str(shell.GetShapeType()) == "COMPOUND":
                self.shells = geompy.ExtractShapes(shell, geompy.ShapeType["SHELL"], True)
            else:
                self.shells = [shell]
            self.shellsIds = []
            for obj in self.shells:
                self.shellsIds.append(obj.GetEntry())
    

    def __select_trajectory(self):
        self.trajectory, self.trajectoryId, check = selection_method(self.mainApp, self.ui.label_translationTrajectoryValidation, self.ui.label_translationTrajectoryEntry, vectorTypesList)


    def __get_increment(self):
        self.increment = get_value_in_line_edit(self.mainApp, self.ui.lineEdit_increment, self.ui.label_incrementValidation)
    

    def __get_number_of_elements(self):
        tmp = get_value_in_line_edit(self.mainApp, self.ui.lineEdit_numberOfSurfaces, self.ui.label_numberOfSurfacesValidation)
        if tmp != None:
            self.numberOfElements = int(tmp)
    

    def __layers_method(self):
        self.isLayersFlag = True
        hide_object([self.ui.radioButton_offset, self.ui.radioButton_translation], False)
        if cfrDlfVersion:
            self.increment = machineParameters.laserTape.layIncr
            self.ui.lineEdit_increment.setText(str(self.increment))
            selection_indicator(self.ui.label_incrementValidation, True)
        return


    def __cutters_method(self):
        self.isLayersFlag = False
        hide_object([self.ui.radioButton_offset, self.ui.radioButton_translation], False)
        if cfrDlfVersion:
            self.increment = machineParameters.laserTape.cutIncr
            self.ui.lineEdit_increment.setText(str(self.increment))
            selection_indicator(self.ui.label_incrementValidation, True)
        return
    

    def __hide_trajectory_selection(self):
        if self.isCreatedByOffset:
            hide_object([self.ui.label_translationTrajectory, self.ui.pushButton_translationTrajectory, self.ui.label_translationTrajectoryValidation, self.ui.label_translationTrajectoryEntry], True)


    def __offset_method(self):
        self.isCreatedByOffset = True
        hide_object([self.ui.radioButton_noOption, self.ui.radioButton_refIsFirst, self.ui.radioButton_firstIsHalfStep], False)
    

    def __translation_method(self):
        self.isCreatedByOffset = False
        hide_object([self.ui.radioButton_noOption, self.ui.radioButton_refIsFirst, self.ui.radioButton_firstIsHalfStep], False)
    

    def __start_at_first_increment_method(self):
        self.firstLayerMethod = 0
        hide_object(self.uiParameters, False)
        self.__hide_trajectory_selection()
    

    def __ref_is_first_layer_method(self):
        self.firstLayerMethod = 1
        hide_object(self.uiParameters, False)
        self.__hide_trajectory_selection()
    

    def __first_is_half_increment_method(self):
        self.firstLayerMethod = 2
        hide_object(self.uiParameters, False)
        self.__hide_trajectory_selection()


    #def __generate_surfaces(self, folder, volume, shell, dataSurfaceGroup:cls_surfaces_grp):
    #    surfacesList = []
    #    step = self.__first_layer_increment()
    #    for stepNumber in range(self.numberOfElements):
    #        if step == 0:
    #            newSurfList = [geompy.MakeCommon(volume, shell, False)] #, theName='toBeDeleted_first'
    #        else:
    #            newSurfList = self.__new_surface(volume, shell, step)
    #        if newSurfList != None:
    #            surfCount = 1
    #            for newSurf in newSurfList:
    #                if len(newSurfList) > 1:
    #                    surfName = "%s_%d.%d"%(self.surfaceName, stepNumber, surfCount)
    #                    surfCount+=1
    #                else:
    #                    surfName = "%s_%d"%(self.surfaceName, stepNumber)
    #                objID = geompy.addToStudyInFather(folder, newSurf, surfName)
    #                #destroy_temporary_object(newSurf)
    #                newSurf=salome.IDToObject(objID)
    #                dataSurfaceGroup.add_surface_to_group(cls_surface(objID))
    #                surfacesList.append(newSurf)
    #                if step == 0 and str(newSurf.GetShapeType()) == "FACE":
    #                    vnorm = geompy.GetNormal(newSurf)
    #                    if vnorm is None:
    #                        print(f"GetNormal(face:{newSurf.GetEntry()}) failed")
    #                        raise RuntimeError
    #                    else:
    #                        geompy.addToStudyInFather(newSurf, vnorm, f"Normale to face {newSurf.GetEntry()}")
    #                        gstools.displayShapeByEntry(newSurf.GetEntry(), color=[0,255,0])
    #                        message_information_no_main("Remember to check the first layer orientation.\nIf needed use change orientation tool on it without creating a copy.", "Reminder:", "info")
    #        self.opCount += 1
    #        update_progressBar(self.ui.progressBar, self.opCount/self.numberOfOperations*100)
    #        step += self.increment
    #    return surfacesList, dataSurfaceGroup
    #
    #
    #def __first_layer_increment(self):
    #    if self.firstLayerMethod == 0:    #start at first increment = 0, include ref as first surface = 1, first is half increment = 2
    #        return self.increment
    #    elif self.firstLayerMethod == 1:
    #        return 0
    #    elif self.firstLayerMethod == 2:
    #        return self.increment/2
    #
    #
    #def __new_surface(self, volume, obj, step):
    #    if self.isCreatedByOffset:
    #        surf = geompy.Offset(obj, step, True)
    #    else:
    #        surf = geompy.TranslateVectorDistance(obj, self.trajectory[0], step, True)
    #    newSurf = geompy.MakeCommon(volume, surf, False)    #, theName='toBeDeleted'
    #    if geompy.NumberOfSubShapes(newSurf, geompy.ShapeType["SHELL"]) > 1:
    #        newSurfList = geompy.ExtractShapes(newSurf, geompy.ShapeType["SHELL"], True)
    #        return newSurfList
    #    if geompy.BasicProperties(newSurf)[1]: #Surface de l'objet --> vérifie qu'il éxiste
    #        return [newSurf]
    #    else:
    #        return None