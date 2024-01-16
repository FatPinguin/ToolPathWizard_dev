from PyQt5 import QtCore, QtWidgets

from ..func.environment import salome
import ToolPathWizard_dev.bin.func.environment as env
from ...assets.Interface_QT.Display_objects import Ui_Dialog_display_items
from ..func.json_gestion import display_objects_from_dataStruct


class display_objects_in_study: #TODO - Proposer d'afficher 1 point sur 10 - 100 et que les traj de retrait & approche + les vecteurs
    def __init__(self, mainApp, objectStr):
        self.mainApp = mainApp
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog_display_items()
        self.window.show()
        self.ui.setupUi(self.window)
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.ui.labelTitle_display_object.setText("<html><head/><body><p><span style=\" font-size:18pt; color:#3366cc;\">Affichage des %s</span></p></body></html>"%(objectStr))
        self.ui.pushButton_return.clicked.connect(self.__close_window)
        self.mainApp.win.show()
        #FCT.display_objects_from_dataStruct(objectStr, self.ui.progressBar, env.dataStruct)
        display_objects_from_dataStruct(objectStr, self.ui.progressBar, env.dataStruct)
        if salome.sg.hasDesktop():
            salome.sg.updateObjBrowser()
        self.window.close()


    def __close_window(self):
        print("Close display window.")
        print("______________________________________________________________________________\n")
        if salome.sg.hasDesktop():
            salome.sg.updateObjBrowser()
        self.mainApp.win.show()
        self.window.close()