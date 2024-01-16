from PyQt5 import QtCore, QtWidgets

from ..func.environment import salome
from ...assets.Interface_QT.Discretisation import Ui_Dialog_discretisation
from .generic_viz import hide_object, selection_method, get_value_in_line_edit, search_group_in_volumes, disable_objects, selection_indicator
from ..func.common_variables import groupType, securityType, cfrDlfVersion
from .user_com import message_information_no_main, message_error
from ..func.discretize import discretisation_tool
from ..func.environment import machineParameters


class tool_discretise:
    def __init__(self, mainApp):
        #self.mainApp:mainWindow = mainApp
        self.mainApp = mainApp
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog_discretisation()
        self.ui.setupUi(self.window)
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.ui.pushButton_validation.clicked.connect(self.__main)
        self.ui.pushButton_return.clicked.connect(self.__close_window)
        self.ui.pushButton_machineParameters.clicked.connect(self.mainApp.show_tools_parameters)
        self.ui.pushButton_selectLayers.clicked.connect(self.__get_layer_group_in_data)
        self.ui.pushButton_selectSecurityFace.clicked.connect(self.__get_security_geom)
        self.ui.lineEdit_discretisationStep.editingFinished.connect(self.__get_increment)
        self.ui.checkBox_avoidingVolume.toggled.connect(self.__generate_security_traj_option)
        self.ui.checkBox_approach_retract.toggled.connect(self.__generate_approach_retract)
        #self.ui.progressBar.hide()
        self.dataLayerGroup=None
        self.generateSecurityTrajOpt=False
        self.generateAproRectractTrajOpt=False
        self.securityGeom=None
        self.increment=None
        self.objectListToHide = [self.ui.label_SecurityFace, self.ui.pushButton_selectSecurityFace, self.ui.label_securityFaceValidation, self.ui.label_securityFaceEntry]
        self.barList = [self.ui.progressBar_lay, self.ui.label_lay, self.ui.progressBar_curves, self.ui.label_curves, self.ui.progressBar_pts, self.ui.label_pts]
        hide_object(self.objectListToHide, True)
        hide_object(self.barList, True)
        self.ui.checkBox_avoidingVolume.setDisabled(True)
        if cfrDlfVersion:
            self.increment = machineParameters.laserTape.incr
            self.ui.lineEdit_discretisationStep.setText(str(self.increment))
            selection_indicator(self.ui.label_discretisationStepValidation, True)
        return
    

    def __main(self):
        if self.dataLayerGroup != None and self.increment != None:
            #if (self.generateSecurityTrajOpt == True and self.securityGeom != None) or self.generateSecurityTrajOpt == False:
            #self.ui.progressBar.show()
                #FCT.discretisation_tool(dataLayerGroup=self.dataLayerGroup, generateSecurityTrajOpt=self.generateSecurityTrajOpt, securityGeom=self.securityGeom, increment=self.increment, UiProgressBar=self.ui.progressBar)
                #DIS.discretisation_tool(dataLayerGroup=self.dataLayerGroup, increment=self.increment, UiProgressBar=self.ui.progressBar)
            hide_object(self.barList, False)
            discretisation_tool(self.dataLayerGroup, self.increment, self.ui.progressBar_lay, self.ui.progressBar_curves, self.ui.progressBar_pts, self.ui.label_lay, self.ui.label_curves, self.ui.label_pts, self.generateSecurityTrajOpt, self.generateAproRectractTrajOpt, self.securityGeom)
            self.__close_window()
            #else:
            #    message_information_no_main("Veuillez selectionner une surface de sécurité.")
        else:
            #message_information_no_main("Missing information")
            message_error("Missing information", self.mainApp)
        

    def __get_layer_group_in_data(self):
        layerGroup, layerGroupId = selection_method(self.mainApp, self.ui.label_layersValidation, self.ui.label_layersEntry, groupType)
        self.dataLayerGroup = search_group_in_volumes(layerGroupId[0])  #FIXME --> bug list indes out of range
        if self.dataLayerGroup == None:
            message_information_no_main("Group not found in data structure.")


    def __generate_security_traj_option(self):
        self.generateSecurityTrajOpt = self.ui.checkBox_avoidingVolume.isChecked()
        if self.generateSecurityTrajOpt:
            hide_object(self.objectListToHide, False)
        else:
            hide_object(self.objectListToHide, True)


    def __generate_approach_retract(self):
        self.generateAproRectractTrajOpt = self.ui.checkBox_approach_retract.isChecked()
        if self.generateAproRectractTrajOpt:
            disable_objects([self.ui.checkBox_avoidingVolume], False)
        else:
            disable_objects([self.ui.checkBox_avoidingVolume], True)
            disable_objects(self.objectListToHide, True)
            hide_object(self.objectListToHide, True)
            self.securityGeom = None
            self.ui.label_securityFaceEntry.setText("Entry:")



    def __get_security_geom(self):
        securityGeomList, securityGeomIDList = selection_method(self.mainApp, self.ui.label_securityFaceValidation, self.ui.label_securityFaceEntry, securityType)
        self.securityGeom = securityGeomList[0]


    def __get_increment(self):
        self.increment = get_value_in_line_edit(self.mainApp, self.ui.lineEdit_discretisationStep, self.ui.label_discretisationStepValidation)
    

    def __close_window(self):
        print("End of discretisation.")
        if salome.sg.hasDesktop():
            salome.sg.updateObjBrowser()
        self.mainApp.win.show()
        self.window.close()