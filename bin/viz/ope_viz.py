from ..func.environment import salome
import ToolPathWizard_dev.bin.func.environment as env
#from .main_viz import mainWindow

from PyQt5 import QtCore, QtWidgets

from ...assets.Interface_QT.Operation_generator import Ui_Dialog_operations


from .generic_viz import hide_object, selection_method, search_group_in_volumes


from ..func.common_variables import cfrDlfVersion, generic, fdmPelletPerimeter, fdmPelletInfill, fdmPerimeter, fdmInfill, milling, tapeLayingAirPulse, tapeLayingLaser, groupType
from ..func.Classes import cls_surfaces_grp, cls_volume
from .user_com import message_information_no_main
from ..func.operation import operation_generator

class tool_create_operations:
    def __init__(self, mainApp):
        self.mainApp = mainApp
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog_operations()
        self.ui.setupUi(self.window)
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.ui.pushButton_Validation.clicked.connect(self.__main)
        self.ui.pushButton_return.clicked.connect(self.__close_window)
        self.ui.pushButton_selectLayers.clicked.connect(self.__get_layer_group)
        self.ui.pushButton_selectCuttingTool.clicked.connect(self.__get_cutting_tool_group)
        self.ui.checkBox_partialSurfaceSelectionOption.toggled.connect(self.__get_skip_option)
        self.ui.radioButton_even.clicked.connect(self.__get_even_option)
        self.ui.radioButton_uneven.clicked.connect(self.__get_uneven_option)
        self.ui.comboBox_fabricationMode.activated[str].connect(self.__get_fabrication_mode)
        self.ui.progressBar.hide()
        self.layerGroup = None
        self.layerGroupId = None
        self.cutterGroup = None
        self.cutterGroupId = None
        self.fabricationMode:int = None
        self.skipOption:bool = False
        self.evenUnevenOption:bool = None
        self.positionTool:bool = False
        if cfrDlfVersion:
            self.__clear_combobox()
            self.fabricationMode = tapeLayingLaser
            #Fonctionnalité plus neccesaire
            #self.ui.checkBox_toolPositioning.setEnabled(True)   
            #self.ui.checkBox_toolPositioning.toggled.connect(self.__get_tool_positioning)
    
    def __main(self):
        hide_object([self.ui.progressBar], False)
        dataLayerGroup:cls_surfaces_grp = search_group_in_volumes(self.layerGroupId[0])
        dataCutterGroup:cls_surfaces_grp = search_group_in_volumes(self.cutterGroupId[0])
        #if cfrDlfVersion:
        #    self.fabricationMode = tapeLayingLaser
        if self.fabricationMode == None:
            message_information_no_main("Veuillez selctionner un mode de fabrication.")
        else:
            if dataLayerGroup != None and dataCutterGroup != None:
                succes = operation_generator(self.fabricationMode, dataLayerGroup.surfaceList, dataCutterGroup.surfaceList, self.evenUnevenOption, self.skipOption, self.ui.progressBar, self.positionTool)
                #succes = FCT.operation_generator(self.fabricationMode, dataLayerGroup.surfaceList, dataCutterGroup.surfaceList, self.evenUnevenOption, self.skipOption, self.ui.progressBar, self.positionTool)
                self.__close_window()
            else:
                message_information_no_main("Un des groupes n'a pas été trouvé dans la structure de données.")
            

    def __close_window(self):
        print("End of operations creation.")
        print("______________________________________________________________________________\n")
        if salome.sg.hasDesktop():
            salome.sg.updateObjBrowser()
        self.mainApp.win.show()
        self.window.close()

    def __get_fabrication_mode(self):
        if not cfrDlfVersion:
            combobox = self.ui.comboBox_fabricationMode.currentText()
            if combobox == self.ui.comboBox_fabricationMode.itemText(0):
                self.fabricationMode = None
            elif combobox == self.ui.comboBox_fabricationMode.itemText(1):
                self.fabricationMode = generic
            elif combobox == self.ui.comboBox_fabricationMode.itemText(2):
                self.fabricationMode = fdmPelletPerimeter
            elif combobox == self.ui.comboBox_fabricationMode.itemText(3):
                self.fabricationMode = fdmPelletInfill
            elif combobox == self.ui.comboBox_fabricationMode.itemText(4):
                self.fabricationMode = fdmPerimeter
            elif combobox == self.ui.comboBox_fabricationMode.itemText(5):
                self.fabricationMode = fdmInfill
            elif combobox == self.ui.comboBox_fabricationMode.itemText(6):
                self.fabricationMode = milling
            elif combobox == self.ui.comboBox_fabricationMode.itemText(7):
                self.fabricationMode = tapeLayingAirPulse
            elif combobox == self.ui.comboBox_fabricationMode.itemText(8):
                self.fabricationMode = tapeLayingLaser
        else:
            self.fabricationMode = tapeLayingLaser

    def __clear_combobox(self):
        self.ui.comboBox_fabricationMode.setItemText(0, QtCore.QCoreApplication.translate("Dialog_operations", "Dépose de bande laser"))
        self.ui.comboBox_fabricationMode.removeItem(8)
        self.ui.comboBox_fabricationMode.removeItem(7)
        self.ui.comboBox_fabricationMode.removeItem(6)
        self.ui.comboBox_fabricationMode.removeItem(5)
        self.ui.comboBox_fabricationMode.removeItem(4)
        self.ui.comboBox_fabricationMode.removeItem(3)
        self.ui.comboBox_fabricationMode.removeItem(2)
        self.ui.comboBox_fabricationMode.removeItem(1)

    def __get_skip_option(self):
        self.skipOption = self.ui.checkBox_partialSurfaceSelectionOption.isChecked()
    
    def __get_tool_positioning(self):
        self.positionTool = self.ui.checkBox_toolPositioning.isChecked()

    def __get_even_option(self):
        self.evenUnevenOption = True

    def __get_uneven_option(self):
        self.evenUnevenOption = False

    def __get_layer_group(self):
        self.layerGroup, self.layerGroupId, check = selection_method(self.mainApp, self.ui.label_layersValidation, self.ui.label_layersEntry, groupType)

    def __get_cutting_tool_group(self):
        self.cutterGroup, self.cutterGroupId, check = selection_method(self.mainApp, self.ui.label_cuttingToolValidation, self.ui.label_cuttingToolEntry, groupType)

    def __search_group_in_volumes(self, groupId:str):
        volume:cls_volume
        group:cls_surfaces_grp
        for volume in env.dataStruct.volumeList:
            for group in volume.surfaceGroupList:
                if group.surfacesGrpId == groupId:
                    return group
        return None