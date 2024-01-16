from ..func.environment import salome
import ToolPathWizard_dev.bin.func.environment as env


from PyQt5 import QtCore, QtWidgets


from ..func.visualise import open_graph


class Path_visualisation:
    def __init__(self, mainApp) -> None:
        #self.mainApp = mainApp
        #self.window = QtWidgets.QDialog()
        #self.ui = Ui_Dialog_()
        #self.ui.setupUi(self.window)
        #self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #self.ui.pushButton_Validation.clicked.connect(self.__main)
        pass

    def __main(self):
        open_graph()
        self.__close_window()


    def __close_window(self):
        print("End of export.")
        print("______________________________________________________________________________\n")
        if salome.sg.hasDesktop():
            salome.sg.updateObjBrowser()
        self.mainApp.win.show()
        self.window.close()
