from ..func.environment import salome
import ToolPathWizard_dev.bin.func.environment as env


import json
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject


from ...assets.Interface_QT.Home import Ui_Dialog_home
from ...assets.Interface_QT.Display_objects import Ui_Dialog_display_items

from .layAndCut_viz import tool_create_layersAndCutters
from .ope_viz import tool_create_operations
from .discr_viz import tool_discretise
from .exp_viz import tool_export
from .params_viz import tool_parameters
from .tree_viz import tool_tree
from .display_viz import display_objects_in_study
from .reverse_viz import tool_reverse
#from .graph_viz import fn

from ..func.common_variables import SLICERVERSION, cfrDlfVersion
from ..func.Classes import cls_data_structure
from ..func.json_gestion import create_dict_of_datastruct_for_json_dump, convert_dict_to_data_structure
from .user_com import message_information_no_main
from ..func.visualise import open_graph


class mainWindow(QObject):
    def __init__(self):
        #fn()
        super(mainWindow,self).__init__()
        self.win = QtWidgets.QMainWindow()
        self.uiMenu = Ui_Dialog_home()
        self.uiMenu.setupUi(self.win)
        #self.win.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.uiMenu.label_studyAdress.setWordWrap(True)
        self.uiMenu.label_dataAdress.setWordWrap(True)
        self.uiMenu.label_version.setText('Version: %s'%(SLICERVERSION))
        if not cfrDlfVersion:
            self.uiMenu.labelIsCFR.setText('')
        #global currentStudy, currentStudyName, geompy, dataStruct
        if env.currentStudy != salome.salome_study.myStudy:
            env.currentStudy = salome.salome_study.myStudy
            env.currentStudyName = salome.salome_study.myStudyName
            env.geompy = env.geomBuilder.New()
            if env.currentStudyName != env.dataStruct.studyAdress:
                message_information_no_main("Nouvelle étude détectée. \nLa structure de donnée est remise à zéro.")
                env.dataStruct = cls_data_structure(env.currentStudyName, env.machineParameters)
        self.uiMenu.label_studyAdress.setText(str(env.dataStruct.studyAdress+".hdf"))
        self.__initTools()
        self.__initSignals()


    def __initTools(self):#Importation des classes d'encapsulation de chacun des fenetres
        self.toolCreateLayers = tool_create_layersAndCutters(self)
        self.toolCreateOperations = tool_create_operations(self)
        self.toolDiscretise = tool_discretise(self)
        self.toolExportation = tool_export(self)
        self.toolParameters = tool_parameters(self)
        self.toolReverse = tool_reverse(self)
        #self.toolTree = tool_tree(self)


    def __initSignals(self):#Connexion entre les fenetres via les boutons
        self.uiMenu.pushButton_wipe_dataStruct.clicked.connect(self.__wipe_data_structure)
        self.uiMenu.pushButton_saveDataStruct.clicked.connect(self.__save_data_structure)
        self.uiMenu.pushButton_importDataStruct.clicked.connect(self.__import_data_structure)
        self.uiMenu.pushButton_toolsParam.clicked.connect(self.show_tools_parameters)
        self.uiMenu.pushButton_layersAndToolsGenerator.clicked.connect(self.__show_create_layers_and_cutters)
        self.uiMenu.pushButton_Operations.clicked.connect(self.__show_create_operations)
        self.uiMenu.pushButton_point_generator.clicked.connect(self.__show_discretise)
        self.uiMenu.pushButton_operationsTree.clicked.connect(self.__show_tool_tree)
        self.uiMenu.pushButton_Export.clicked.connect(self.__show_export)
        self.uiMenu.pushButton_display_layers.clicked.connect(self.__show_layers_in_study)
        self.uiMenu.pushButton_display_trajectories.clicked.connect(self.__show_trajectories_in_study)
        self.uiMenu.pushButton_display_points.clicked.connect(self.__show_points_in_study)
        self.uiMenu.pushButton_display_points.setDisabled(True)
        self.uiMenu.pushButton_viz.clicked.connect(self.__plot_points)
        self.uiMenu.pushButton_reverse.clicked.connect(self.__reverse_wires)
        #self.uiMenu.pushButton_viz.setDisabled(True)


    def __wipe_data_structure(self):
        print("\n______________________________________________________________________________")
        print("Reset data structure...")
        #global dataStruct, currentStudyName
        env.currentStudyName = salome.salome_study.myStudyName
        env.dataStruct = cls_data_structure(env.currentStudyName, env.machineParameters)
        self.uiMenu.label_dataAdress.setText("Reseted")


    def __save_data_structure(self):
        print("\n______________________________________________________________________________")
        print("Save HDF and data structure in jSon file...")
        fileName,typ = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File' ,'',"All files (*)")
        salome.salome_study.myStudyName = fileName
        salome.myStudy.SaveAs(str(fileName+".hdf"), False, False)
        file = open(str(fileName+".json"),'w')
        #json.dump(FCT.create_dict_of_datastruct_for_json_dump("SALUUUUT", env.dataStruct), file, indent=4)
        env.dataStruct.studyAdress = salome.salome_study.myStudyName
        #json.dump(FCT.create_dict_of_datastruct_for_json_dump(salome.salome_study.myStudyName, env.dataStruct), file, indent=4)
        json.dump(create_dict_of_datastruct_for_json_dump(salome.salome_study.myStudyName, env.dataStruct), file, indent=4)
        #json.dump(create_dict_of_datastruct_for_json_dump(salome.salome_study.myStudyName), file, indent=4)
        file.close()
        self.uiMenu.label_dataAdress.setText(str(fileName+".json"))
        self.uiMenu.label_studyAdress.setText(str(env.dataStruct.studyAdress+".hdf"))
        print(f"\tHDF saved")
        #if salome.salome_study.myStudyName!=dataStruct.studyAdress:
        #    message_information_no_main("Attention, l'étude actuelle ne correspond pas à la structure de donnée enregistée.\nActual study name : %s\nName saved : %s"%(salome.salome_study.myStudyName, dataStruct.studyAdress))   #TODO - Ajouter fenetre propostition ouverture study from datastuct
        #self.saveDataStruct.window.show() #Affiche la fenetre
        #self.win.close()    #ferme le menu principal
    

    def __import_data_structure(self):
        #global dataStruct, currentStudy, currentStudyName
        print("\n______________________________________________________________________________")
        print("Import data structure from jSon file...")
        fileName , typ = QtWidgets.QFileDialog.getOpenFileName(None,"Load File", "","Data structure slicer (*.json);;All files (*.*);;All files (*);;")
        #♣env.currentStudy = salome.myStudyManager.OpenStudy(str(fileName + ".hdf"))
        file = open(fileName,'r')
        dictDataStruct = json.load(file)
        file.close()
        #env.dataStruct = FCT.convert_dict_to_data_structure(dictDataStruct)
        env.dataStruct = convert_dict_to_data_structure(dictDataStruct)
        self.uiMenu.label_dataAdress.setText(fileName)
        #self.uiMenu.label_dataAdress.setText(str(fileName+".json"))
        if salome.salome_study.myStudyName!=env.dataStruct.studyAdress:
            message_information_no_main("Attention, l'étude actuelle ne correspond pas à la structure de donnée chargée.\nActual study name : %s\nName saved : %s"%(salome.salome_study.myStudyName, env.dataStruct.studyAdress))


    def show_tools_parameters(self):
        print("\n______________________________________________________________________________")
        print("Tools parameters...")
        self.toolParameters = tool_parameters(self)
        self.toolParameters.window.show() #Affiche la fenetre
        #self.win.close()    #ferme le menu principal


    def __show_create_layers_and_cutters(self):
        print("\n______________________________________________________________________________")
        print("Layer and cutter creation tool...")
        self.toolCreateLayers = tool_create_layersAndCutters(self)
        self.toolCreateLayers.window.show() #Affiche la fenetre
        self.win.close()    #ferme le menu principal
    

    def __show_create_operations(self):
        print("\n______________________________________________________________________________")
        print("Operation creation tool...")
        self.toolCreateOperations = tool_create_operations(self)
        self.toolCreateOperations.window.show() #Affiche la fenetre
        self.win.close()    #ferme le menu principal


    def __show_discretise(self):
        print("\n______________________________________________________________________________")
        print("Discretisation tool...")
        self.toolDiscretise = tool_discretise(self)
        self.toolDiscretise.window.show() #Affiche la fenetre
        self.win.close()    #ferme le menu principal


    def __show_tool_tree(self):
        print("\n______________________________________________________________________________")
        print("Operations tree...")
        self.toolTree = tool_tree(self)
        self.toolTree.window.show() #Affiche la fenetre
        self.win.close()    #ferme le menu principal


    def __show_export(self):
        print("\n______________________________________________________________________________")
        print("Discretisation and exportation...")
        self.toolExportation = tool_export(self)
        self.toolExportation.window.show() #Affiche la fenetre
        self.win.close()    #ferme le menu principal
    

    def __show_layers_in_study(self):
        self.__display_tool("layers")


    def __show_trajectories_in_study(self):
        self.__display_tool("trajectoires")


    def __show_points_in_study(self):
        self.__display_tool("points")
    

    def __display_tool(self, itemStr):
        print("\n______________________________________________________________________________")
        print("Displaying %s..."%(itemStr))
        #self.win.close()
        self.displayTool = display_objects_in_study(self, itemStr)
        #self.displayTool.window.show()


    def __plot_points(self):
        print("\n______________________________________________________________________________")
        print("Displaying graph of points")
        open_graph()
        self.win.show()


    def __reverse_wires(self):
        print("\n______________________________________________________________________________")
        print("Select wires to be reversed...")
        self.toolReverse = tool_reverse(self)
        self.toolReverse.window.show() #Affiche la fenetre
        self.win.close()    #ferme le menu principal
