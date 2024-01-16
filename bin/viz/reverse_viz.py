import ToolPathWizard_dev.bin.func.environment as env
#from .main_viz import mainWindow

from PyQt5 import QtCore, QtWidgets

from ...assets.Interface_QT.Reverse import Ui_Dialog_reverse


from .user_com import message_information_no_main
from .generic_viz import get_objects_from_study
from ..func.reverse import reverse_func, display_wires, verify_type, search

class tool_reverse:
    def __init__(self, mainApp):
        #self.mainApp:mainWindow = mainApp
        self.mainApp = mainApp
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog_reverse()
        self.ui.setupUi(self.window)
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.ui.pb_valider.clicked.connect(self.__main)
        self.ui.pb_return.clicked.connect(self.__close_window)
        self.ui.pb_add.clicked.connect(self.__add)
        self.ui.pb_remove.clicked.connect(self.__remove)
        self.selection = []
        self.selectionIds = []

    
    def __main(self):
        if self.selection != []:
            reverse_func(self.selection)
            display_wires(self.selectionIds)
            self.__close_window()
        else:
            message_information_no_main("Veuillez selectionner au minimum un wire.")


    def __close_window(self):
        print("End of reverse.")
        print("______________________________________________________________________________\n")
        if env.salome.sg.hasDesktop():
            env.salome.sg.updateObjBrowser()
        self.mainApp.win.show()
        self.window.close()


    def __add(self):
        selCount, objectList, objectIdList = get_objects_from_study(self.mainApp)
        for i in range(len(objectIdList)):
            if search(self.selectionIds, objectIdList[i]) == None:
                if verify_type(objectList[i]):
                    self.selection.append(objectList[i])
                    self.selectionIds.append(objectIdList[i])
        self.__set_text()
        return


    def __remove(self):
        selCount, objectList, objectIdList = get_objects_from_study(self.mainApp)
        for id in objectIdList:
            index = search(self.selectionIds, id)
            if index != None:
                self.selection.pop(index)
                self.selectionIds.pop(index)
        self.__set_text()
        return
    

    def __set_text(self):
        self.ui.textBrowser_selection_content.setText(str(self.selectionIds))
        return