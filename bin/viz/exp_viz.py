from ..func.environment import salome
import ToolPathWizard_dev.bin.func.environment as env
from .generic_viz import hide_object, selection_method, get_value_in_line_edit, selection_indicator
from ..func.common_variables import volumesTypesList, surfacesTypesList, vectorTypesList, cfrDlfVersion
#from .main_viz import mainWindow
from ..func.dlf7axis import vectors_verification

from PyQt5 import QtCore, QtWidgets

from ...assets.Interface_QT.Export import Ui_Dialog_export


from .user_com import message_information_no_main
from ..func.export import export_tool


class tool_export:
    def __init__(self, mainApp):
        #self.mainApp:mainWindow = mainApp
        self.mainApp = mainApp
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog_export()
        self.ui.setupUi(self.window)
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.ui.pushButton_Validation.clicked.connect(self.__main)
        self.ui.pushButton_return.clicked.connect(self.__close_window)
        self.ui.progressBar.hide()
        self.ui.toolButton_seletctPath.clicked.connect(self.__chooseFile)
        self.fileName = None
        self.exportInfillBeforePerimeter = False
        self.ui.checkBox_infillBeforePerimeters.toggled.connect(self.__export_option)
        self.ui.lineEdit_fileName.editingFinished.connect(self.__get_fileName)
        self.ui.checkBox_infillBeforePerimeters.setDisabled(True)
        self.ui.checkBox_define_change_tool_point.setDisabled(True)
        self.ui.pushButton_load_change_tool_point.setDisabled(True)
        self.ui.label_pointValidation.setDisabled(True)
        self.ui.label_point_entry.setDisabled(True)
        #self.ui.tableWidget_operation.setDisabled(True)
        self.ui.label_pointValidation.hide()
        self.ui.label_point_entry.hide()
        self.orthoVector = None
        self.orthoVectorId = None
        self.rotVector = None
        self.rotVectorId = None
        self.orthoV = None
        self.rotV = None
        self.ui.pushButton_rotVect.clicked.connect(self.__select_vect_rot)
        self.ui.pushButton_orthoVect.clicked.connect(self.__select_vect_ortho)
        self.ui.checkBox_7axis_compilation.stateChanged.connect(self.__status_axis_7)
        self.ui.label_rotVectValidation.hide()
        self.ui.label_orthoVectValidation.hide()
    

    def __main(self):
        if self.fileName != None:
            self.ui.progressBar.show()
            export_tool(data=env.dataStruct, fileAdress=self.fileName, exportInfillBeforePerimeter=self.exportInfillBeforePerimeter, UiProgressBar=self.ui.progressBar, flag7axis=self.ui.checkBox_7axis_compilation, orthoVector=self.orthoV)
            #FCT.export_tool(data=env.dataStruct, fileAdress=self.fileName, exportInfillBeforePerimeter=self.exportInfillBeforePerimeter, UiProgressBar=self.ui.progressBar)
            self.__close_window()
        else:
            message_information_no_main("Veuillez selectionner un fichier.")


    def __close_window(self):
        print("End of export.")
        print("______________________________________________________________________________\n")
        if salome.sg.hasDesktop():
            salome.sg.updateObjBrowser()
        self.mainApp.win.show()
        self.window.close()


    def __get_fileName(self):
        self.fileName = self.ui.lineEdit_fileName.text()


    def __chooseFile(self):
        self.fileName, typ = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File' ,'',"Data export slicer (*.csv);;All files (*.*);;All files (*);;")
        self.ui.lineEdit_fileName.setText(self.fileName)


    def __export_option(self):
        self.exportInfillBeforePerimeter = self.ui.checkBox_infillBeforePerimeters.isChecked()

    
    def __select_vector(self, validation, entry):
        vector, vectorId, check = selection_method(self.mainApp, validation, entry, vectorTypesList)
        if check == False:
            return None, None
        #if len(vector) > 1:
        #    vector = vector[0]
        #    vectorId = vectorId[0]
        return vector[0], vectorId[0]
    
    
    def __select_vect_ortho(self):
        self.orthoVector, self.orthoVectorId = self.__select_vector(self.ui.label_orthoVectValidation, self.ui.label_orthoVectEntry)
        self.orthoV, self.rotV = self.__vectors_check()
    

    def __select_vect_rot(self):
        self.rotVector, self.rotVectorId = self.__select_vector(self.ui.label_rotVectValidation, self.ui.label_rotVectEntry)
        self.orthoV, self.rotV = self.__vectors_check()


    def __vectors_check(self):
        if self.rotVector != None and self.orthoVector != None:
            check, orthoV, rotV = vectors_verification(self.orthoVector, self.rotVector)
            if check :
                return orthoV, rotV
        return None, None
    

    def __status_axis_7(self):
        if self.ui.checkBox_7axis_compilation.isChecked():
            self.ui.label_rotVect.setEnabled(True)
            self.ui.pushButton_rotVect.setEnabled(True)
            self.ui.label_rotVectValidation.setEnabled(True)
            self.ui.label_rotVectEntry.setEnabled(True)
            self.ui.label_orthoVect.setEnabled(True)
            self.ui.pushButton_orthoVect.setEnabled(True)
            self.ui.label_orthoVectValidation.setEnabled(True)
            self.ui.label_orthoVectEntry.setEnabled(True)
        else :
            self.ui.label_rotVect.setEnabled(False)
            self.ui.pushButton_rotVect.setEnabled(False)
            self.ui.label_rotVectValidation.setEnabled(False)
            self.ui.label_rotVectEntry.setEnabled(False)
            self.ui.label_orthoVect.setEnabled(False)
            self.ui.pushButton_orthoVect.setEnabled(False)
            self.ui.label_orthoVectValidation.setEnabled(False)
            self.ui.label_orthoVectEntry.setEnabled(False)
            self.orthoVector = None
            self.orthoVectorId = None
            self.rotVector = None
            self.rotVectorId = None
            self.orthoV = None
            self.rotV = None
            selection_indicator(self.ui.label_rotVectValidation, False)
            selection_indicator(self.ui.label_orthoVectValidation, False)
            self.ui.label_rotVectValidation.hide()
            self.ui.label_orthoVectValidation.hide()
            self.ui.label_rotVectEntry.setText("Entry: ")
            self.ui.label_orthoVectEntry.setText("Entry: ")

        
