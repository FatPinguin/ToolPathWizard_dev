from ..func.environment import salome
import ToolPathWizard_dev.bin.func.environment as env
#from .main_viz import mainWindow

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
    

    def __main(self):
        if self.fileName != None:
            self.ui.progressBar.show()
            export_tool(data=env.dataStruct, fileAdress=self.fileName, exportInfillBeforePerimeter=self.exportInfillBeforePerimeter, UiProgressBar=self.ui.progressBar)
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