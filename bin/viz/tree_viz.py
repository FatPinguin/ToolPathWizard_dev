from ..func.environment import salome
import ToolPathWizard_dev.bin.func.environment as env

from PyQt5 import QtCore, QtWidgets

from ...assets.Interface_QT.Operations_tree import Ui_Dialog_operationOrganisator
from ..func.tree import convert_data_structure_to_QT_tree_widget, find_modif_QT_tree_widget


class tool_tree:
    def __init__(self, mainApp):
        self.mainApp = mainApp
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog_operationOrganisator()
        self.ui.setupUi(self.window)
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #self.ui.pushButton_Validation.accepted.connect(self.__main)
        self.ui.pushButton_return.clicked.connect(self.__close_window)
        self.ui.pushButton_update_data.clicked.connect(self.__update_dataStruct)
        #FCT.convert_data_structure_to_QT_tree_widget(self.ui.treeWidget, env.dataStruct)
        convert_data_structure_to_QT_tree_widget(self.ui.treeWidget, env.dataStruct)
        #self.ui.pushButton_deleteOperation(self.__delete_item_dataStruct)
        #self.ui.pushButton_down_operation()
        #self.ui.pushButton_up_operation()


    def __close_window(self):
        print("Close tool tree.")
        print("______________________________________________________________________________\n")
        if salome.sg.hasDesktop():
            salome.sg.updateObjBrowser()
        self.mainApp.win.show()
        self.window.close()
    

    def __update_dataStruct(self):
        #FCT.find_modif_QT_tree_widget(self.ui.treeWidget, env.dataStruct)
        find_modif_QT_tree_widget(self.ui.treeWidget, env.dataStruct)
        opSort = []
        env.dataStruct.sortedOperations = opSort
