from ..func.environment import salome
import ToolPathWizard_dev.bin.func.environment as env

from PyQt5 import QtCore, QtWidgets
import json

from ...assets.Interface_QT.Parameters import Ui_Dialog_parameters
from ..func.json_gestion import import_dict_tool_in_tool_struct, create_dict_of_toolstruct_for_json_dump


class tool_parameters:
    def __init__(self, mainApp):
        self.mainApp = mainApp
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog_parameters()
        self.ui.setupUi(self.window)
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.__display_params_from_data_struct()
        self.ui.pushButton_validation.clicked.connect(self.__main)
        self.ui.pushButton_return.clicked.connect(self.__close_window)
        self.ui.pushButton_import_param.clicked.connect(self.__import_tool_struct_from_json)
        self.ui.pushButton_save_param.clicked.connect(self.__save_tool_struct_in_json)
    

    def __main(self):
        self.get_parameters_from_study()
        self.__close_window()


    def __close_window(self):
        print("Close parameters setup.")
        print("______________________________________________________________________________\n")
        if salome.sg.hasDesktop():
            salome.sg.updateObjBrowser()
        #self.mainApp.win.show()
        self.window.close()
    

    def get_parameters_from_study(self):
        env.dataStruct.machineParam.generics.approachSpeed = float(self.ui.lineEdit_gen_approachSpeed.text())
        env.dataStruct.machineParam.generics.retractSpeed = float(self.ui.lineEdit_gen_retractSpeed.text())
        env.dataStruct.machineParam.generics.toolSpeed = float(self.ui.lineEdit_gen_toolSpeed.text())
        env.dataStruct.machineParam.generics.securityDistance = float(self.ui.lineEdit_distSecu.text())
        env.dataStruct.machineParam.generics.travelSpeed = float(self.ui.lineEdit_travelSpeed.text())

        env.dataStruct.machineParam.fdmPellet.screwSpeed = float(self.ui.lineEdit_FDM_pellet_screwSpeed.text())
        env.dataStruct.machineParam.fdmPellet.infillSpeed = float(self.ui.lineEdit_FDM_pellet_infillSpeed.text())
        env.dataStruct.machineParam.fdmPellet.perimeterSpeed = float(self.ui.lineEdit_FDM_pellet_perimeterSpeed.text())
        env.dataStruct.machineParam.fdmPellet.extruderTemp = float(self.ui.lineEdit_FDM_pellet_temperature.text())
        env.dataStruct.machineParam.fdmPellet.distanceToRetract = float(self.ui.lineEdit_FDM_pellet_retractionDistance.text())
        env.dataStruct.machineParam.fdmPellet.extrusionDiameter = float(self.ui.lineEdit_FDM_pellet_extrusionDiameter.text())
        
        env.dataStruct.machineParam.fdmFilament.infillSpeed = float(self.ui.lineEdit_FDM_filam_ifillSpeed.text())
        env.dataStruct.machineParam.fdmFilament.perimeterSpeed = float(self.ui.lineEdit_FDM_filam_perimeterSpeed.text())
        env.dataStruct.machineParam.fdmFilament.relativeFilamentSpeed = float(self.ui.lineEdit_FDM_filam_relativFilamentSpeed.text())
        env.dataStruct.machineParam.fdmFilament.filamentSpeed = float(self.ui.lineEdit_FDM_filam_filamentSpeed.text())
        env.dataStruct.machineParam.fdmFilament.extruderTemp = float(self.ui.lineEdit_FDM_filam_temperature.text())
        env.dataStruct.machineParam.fdmFilament.extrusionDiameter = float(self.ui.lineEdit_FDM_filam_extrusionDiameter.text())
        
        env.dataStruct.machineParam.milling.toolSpeed = float(self.ui.lineEdit_mill_moveSpeed.text())
        env.dataStruct.machineParam.milling.spindleSpeed = float(self.ui.lineEdit_mill_toolSpeedRot.text())
        env.dataStruct.machineParam.milling.toolDiameter = float(self.ui.lineEdit_mill_toolDiameter.text())
        env.dataStruct.machineParam.milling.toolCorrection = self.ui.checkBox_mill_compensateTool.isChecked()
        
        env.dataStruct.machineParam.airTape.toolSpeed = float(self.ui.lineEdit_airTape_speed.text())
        
        env.dataStruct.machineParam.laserTape.toolSpeed = float(self.ui.lineEdit_laserTape_toolSpeed.text())
        env.dataStruct.machineParam.laserTape.laserPower = float(self.ui.lineEdit_laserTape_laserPower.text())
        env.dataStruct.machineParam.laserTape.feedSpeed = float(self.ui.lineEdit_feedSpeed.text())
        env.dataStruct.machineParam.laserTape.minimumTrajectoryLength = float(self.ui.lineEdit_minTrajLen.text())
        env.dataStruct.machineParam.laserTape.offset = float(self.ui.lineEdit_offset.text())
        env.dataStruct.machineParam.laserTape.incr = float(self.ui.lineEdit_incr.text())
        env.dataStruct.machineParam.laserTape.layIncr = float(self.ui.lineEdit_layIncr.text())
        env.dataStruct.machineParam.laserTape.cutIncr = float(self.ui.lineEdit_cutIncr.text())

        #global machineParameters 
        env.machineParameters = env.dataStruct.machineParam


    def __display_params_from_data_struct(self):
        self.ui.lineEdit_gen_approachSpeed.setText(str(env.dataStruct.machineParam.generics.approachSpeed))
        self.ui.lineEdit_gen_retractSpeed.setText(str(env.dataStruct.machineParam.generics.retractSpeed))
        self.ui.lineEdit_gen_toolSpeed.setText(str(env.dataStruct.machineParam.generics.toolSpeed))
        self.ui.lineEdit_distSecu.setText(str(env.dataStruct.machineParam.generics.securityDistance))
        self.ui.lineEdit_travelSpeed.setText(str(env.dataStruct.machineParam.generics.travelSpeed))

        self.ui.lineEdit_FDM_pellet_screwSpeed.setText(str(env.dataStruct.machineParam.fdmPellet.screwSpeed))
        self.ui.lineEdit_FDM_pellet_infillSpeed.setText(str(env.dataStruct.machineParam.fdmPellet.infillSpeed))
        self.ui.lineEdit_FDM_pellet_perimeterSpeed.setText(str(env.dataStruct.machineParam.fdmPellet.perimeterSpeed))
        self.ui.lineEdit_FDM_pellet_temperature.setText(str(env.dataStruct.machineParam.fdmPellet.extruderTemp))
        self.ui.lineEdit_FDM_pellet_retractionDistance.setText(str(env.dataStruct.machineParam.fdmPellet.distanceToRetract))
        self.ui.lineEdit_FDM_pellet_extrusionDiameter.setText(str(env.dataStruct.machineParam.fdmPellet.extrusionDiameter))

        self.ui.lineEdit_FDM_filam_ifillSpeed.setText(str(env.dataStruct.machineParam.fdmFilament.infillSpeed))
        self.ui.lineEdit_FDM_filam_perimeterSpeed.setText(str(env.dataStruct.machineParam.fdmFilament.perimeterSpeed))
        self.ui.lineEdit_FDM_filam_relativFilamentSpeed.setText(str(env.dataStruct.machineParam.fdmFilament.relativeFilamentSpeed))
        self.ui.lineEdit_FDM_filam_filamentSpeed.setText(str(env.dataStruct.machineParam.fdmFilament.filamentSpeed))
        self.ui.lineEdit_FDM_filam_temperature.setText(str(env.dataStruct.machineParam.fdmFilament.extruderTemp))
        self.ui.lineEdit_FDM_filam_extrusionDiameter.setText(str(env.dataStruct.machineParam.fdmFilament.extrusionDiameter))
        
        self.ui.lineEdit_mill_moveSpeed.setText(str(env.dataStruct.machineParam.milling.toolSpeed))
        self.ui.lineEdit_mill_toolSpeedRot.setText(str(env.dataStruct.machineParam.milling.spindleSpeed))
        self.ui.lineEdit_mill_toolDiameter.setText(str(env.dataStruct.machineParam.milling.toolDiameter))
        self.ui.checkBox_mill_compensateTool.setChecked(env.dataStruct.machineParam.milling.toolCorrection)
        
        self.ui.lineEdit_airTape_speed.setText(str(env.dataStruct.machineParam.airTape.toolSpeed))
        
        self.ui.lineEdit_laserTape_toolSpeed.setText(str(env.dataStruct.machineParam.laserTape.toolSpeed))
        self.ui.lineEdit_laserTape_laserPower.setText(str(env.dataStruct.machineParam.laserTape.laserPower))
        self.ui.lineEdit_feedSpeed.setText(str(env.dataStruct.machineParam.laserTape.feedSpeed))
        self.ui.lineEdit_minTrajLen.setText(str(env.dataStruct.machineParam.laserTape.minimumTrajectoryLength))
        self.ui.lineEdit_offset.setText(str(env.dataStruct.machineParam.laserTape.offset))
        self.ui.lineEdit_incr.setText(str(env.dataStruct.machineParam.laserTape.incr))
        self.ui.lineEdit_layIncr.setText(str(env.dataStruct.machineParam.laserTape.layIncr))
        self.ui.lineEdit_cutIncr.setText(str(env.dataStruct.machineParam.laserTape.cutIncr))


    def __save_tool_struct_in_json(self):
        self.get_parameters_from_study()
        print("\n______________________________________________________________________________")
        print("Save data tool parameters in jSon file...")
        fileName,typ = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File' ,'',"Tool structure slicer (*.json);;All files (*.*);;All files (*);;")
        file = open(fileName,'w')
        #machParamDict = {'Machine parameters' : FCT.create_dict_of_toolstruct_for_json_dump(env.machineParameters)}
        print("suce")
        machParamDict = {'Machine parameters' : create_dict_of_toolstruct_for_json_dump(env.dataStruct.machineParam)}
        print(machParamDict)
        json.dump(machParamDict, file, indent=4)
        file.close()
    
    
    def __import_tool_struct_from_json(self):
        print("\n______________________________________________________________________________")
        print("Import tool structure from jSon file...")
        fileName , typ = QtWidgets.QFileDialog.getOpenFileName(None,"Load File", "","Tool structure slicer (*.json);;All files (*.*);;All files (*);;")
        file = open(fileName,'r')
        dictToolStruct = json.load(file)
        file.close()
        #FCT.import_dict_tool_in_tool_struct(env.dataStruct, dictToolStruct)
        import_dict_tool_in_tool_struct(env.dataStruct, dictToolStruct)
        self.__display_params_from_data_struct()