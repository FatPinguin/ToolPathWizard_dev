# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Max\.config\salome\Plugins\ToolPathWizard_dev\assets\Interface_QT\ui\Home.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_home(object):
    def setupUi(self, Dialog_home):
        Dialog_home.setObjectName("Dialog_home")
        Dialog_home.resize(400, 700)
        Dialog_home.setMinimumSize(QtCore.QSize(400, 700))
        Dialog_home.setMaximumSize(QtCore.QSize(400, 700))
        self.labelTitle_Menu = QtWidgets.QLabel(Dialog_home)
        self.labelTitle_Menu.setGeometry(QtCore.QRect(0, 0, 341, 60))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.labelTitle_Menu.setFont(font)
        self.labelTitle_Menu.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitle_Menu.setObjectName("labelTitle_Menu")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog_home)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 80, 359, 591))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_menu = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_menu.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_menu.setObjectName("verticalLayout_menu")
        self.horizontalLayout_dataStructButtons = QtWidgets.QHBoxLayout()
        self.horizontalLayout_dataStructButtons.setObjectName("horizontalLayout_dataStructButtons")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_dataStruct = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_dataStruct.setObjectName("label_dataStruct")
        self.verticalLayout_2.addWidget(self.label_dataStruct)
        self.label_dataAdress = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_dataAdress.setObjectName("label_dataAdress")
        self.verticalLayout_2.addWidget(self.label_dataAdress)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_dataStructButtons.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_wipe_dataStruct = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_wipe_dataStruct.setObjectName("pushButton_wipe_dataStruct")
        self.verticalLayout.addWidget(self.pushButton_wipe_dataStruct)
        self.pushButton_importDataStruct = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_importDataStruct.setObjectName("pushButton_importDataStruct")
        self.verticalLayout.addWidget(self.pushButton_importDataStruct)
        self.pushButton_saveDataStruct = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_saveDataStruct.setObjectName("pushButton_saveDataStruct")
        self.verticalLayout.addWidget(self.pushButton_saveDataStruct)
        self.horizontalLayout_dataStructButtons.addLayout(self.verticalLayout)
        self.verticalLayout_menu.addLayout(self.horizontalLayout_dataStructButtons)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_menu.addWidget(self.line)
        self.pushButton_toolsParam = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_toolsParam.setObjectName("pushButton_toolsParam")
        self.verticalLayout_menu.addWidget(self.pushButton_toolsParam)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_menu.addWidget(self.line_2)
        self.pushButton_layersAndToolsGenerator = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_layersAndToolsGenerator.setObjectName("pushButton_layersAndToolsGenerator")
        self.verticalLayout_menu.addWidget(self.pushButton_layersAndToolsGenerator)
        self.pushButton_Operations = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_Operations.setEnabled(True)
        self.pushButton_Operations.setObjectName("pushButton_Operations")
        self.verticalLayout_menu.addWidget(self.pushButton_Operations)
        self.pushButton_reverse = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_reverse.setObjectName("pushButton_reverse")
        self.verticalLayout_menu.addWidget(self.pushButton_reverse)
        self.pushButton_point_generator = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_point_generator.setEnabled(True)
        self.pushButton_point_generator.setObjectName("pushButton_point_generator")
        self.verticalLayout_menu.addWidget(self.pushButton_point_generator)
        self.pushButton_operationsTree = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_operationsTree.setEnabled(True)
        self.pushButton_operationsTree.setObjectName("pushButton_operationsTree")
        self.verticalLayout_menu.addWidget(self.pushButton_operationsTree)
        self.pushButton_Export = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_Export.setEnabled(True)
        self.pushButton_Export.setObjectName("pushButton_Export")
        self.verticalLayout_menu.addWidget(self.pushButton_Export)
        self.pushButton_viz = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_viz.setObjectName("pushButton_viz")
        self.verticalLayout_menu.addWidget(self.pushButton_viz)
        self.line_3 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_menu.addWidget(self.line_3)
        self.label_display = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_display.setObjectName("label_display")
        self.verticalLayout_menu.addWidget(self.label_display)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_display_layers = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_display_layers.setObjectName("pushButton_display_layers")
        self.horizontalLayout.addWidget(self.pushButton_display_layers)
        self.pushButton_display_trajectories = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_display_trajectories.setObjectName("pushButton_display_trajectories")
        self.horizontalLayout.addWidget(self.pushButton_display_trajectories)
        self.pushButton_display_points = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_display_points.setEnabled(False)
        self.pushButton_display_points.setObjectName("pushButton_display_points")
        self.horizontalLayout.addWidget(self.pushButton_display_points)
        self.verticalLayout_menu.addLayout(self.horizontalLayout)
        self.label_warning = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_warning.setObjectName("label_warning")
        self.verticalLayout_menu.addWidget(self.label_warning)
        self.line_4 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_menu.addWidget(self.line_4)
        self.label_studyName = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_studyName.setObjectName("label_studyName")
        self.verticalLayout_menu.addWidget(self.label_studyName)
        self.label_studyAdress = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_studyAdress.setObjectName("label_studyAdress")
        self.verticalLayout_menu.addWidget(self.label_studyAdress)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_menu.addItem(spacerItem1)
        self.label_version = QtWidgets.QLabel(Dialog_home)
        self.label_version.setGeometry(QtCore.QRect(120, 50, 161, 16))
        self.label_version.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_version.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_version.setObjectName("label_version")
        self.labelIsCFR = QtWidgets.QLabel(Dialog_home)
        self.labelIsCFR.setGeometry(QtCore.QRect(257, 65, 47, 13))
        self.labelIsCFR.setObjectName("labelIsCFR")

        self.retranslateUi(Dialog_home)
        self.pushButton_toolsParam.clicked.connect(self.pushButton_layersAndToolsGenerator.show)
        self.pushButton_toolsParam.clicked.connect(self.pushButton_Operations.show)
        self.pushButton_toolsParam.clicked.connect(self.pushButton_operationsTree.show)
        self.pushButton_toolsParam.clicked.connect(self.pushButton_Export.show)
        self.pushButton_toolsParam.clicked.connect(self.pushButton_point_generator.show)
        QtCore.QMetaObject.connectSlotsByName(Dialog_home)
        Dialog_home.setTabOrder(self.pushButton_wipe_dataStruct, self.pushButton_importDataStruct)
        Dialog_home.setTabOrder(self.pushButton_importDataStruct, self.pushButton_saveDataStruct)
        Dialog_home.setTabOrder(self.pushButton_saveDataStruct, self.pushButton_toolsParam)
        Dialog_home.setTabOrder(self.pushButton_toolsParam, self.pushButton_layersAndToolsGenerator)
        Dialog_home.setTabOrder(self.pushButton_layersAndToolsGenerator, self.pushButton_Operations)
        Dialog_home.setTabOrder(self.pushButton_Operations, self.pushButton_reverse)
        Dialog_home.setTabOrder(self.pushButton_reverse, self.pushButton_point_generator)
        Dialog_home.setTabOrder(self.pushButton_point_generator, self.pushButton_operationsTree)
        Dialog_home.setTabOrder(self.pushButton_operationsTree, self.pushButton_Export)
        Dialog_home.setTabOrder(self.pushButton_Export, self.pushButton_viz)
        Dialog_home.setTabOrder(self.pushButton_viz, self.pushButton_display_layers)
        Dialog_home.setTabOrder(self.pushButton_display_layers, self.pushButton_display_trajectories)
        Dialog_home.setTabOrder(self.pushButton_display_trajectories, self.pushButton_display_points)

    def retranslateUi(self, Dialog_home):
        _translate = QtCore.QCoreApplication.translate
        Dialog_home.setWindowTitle(_translate("Dialog_home", "Home"))
        self.labelTitle_Menu.setText(_translate("Dialog_home", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; color:#3366cc;\">Slicer 6 axes</span></p></body></html>"))
        self.label_dataStruct.setText(_translate("Dialog_home", "Structure de données :"))
        self.label_dataAdress.setText(_translate("Dialog_home", "...Not yet saved..."))
        self.pushButton_wipe_dataStruct.setText(_translate("Dialog_home", "Mise à zéro"))
        self.pushButton_importDataStruct.setText(_translate("Dialog_home", "Importer"))
        self.pushButton_saveDataStruct.setText(_translate("Dialog_home", "Sauvegarder"))
        self.pushButton_toolsParam.setText(_translate("Dialog_home", "Paramètres outils"))
        self.pushButton_layersAndToolsGenerator.setText(_translate("Dialog_home", "Couches et outils de coupe"))
        self.pushButton_Operations.setText(_translate("Dialog_home", "Opération"))
        self.pushButton_reverse.setText(_translate("Dialog_home", "Reverse wires"))
        self.pushButton_point_generator.setText(_translate("Dialog_home", "Générateur de points de passage"))
        self.pushButton_operationsTree.setText(_translate("Dialog_home", "Arbre des opérations"))
        self.pushButton_Export.setText(_translate("Dialog_home", "Export"))
        self.pushButton_viz.setText(_translate("Dialog_home", "View points form CSV"))
        self.label_display.setText(_translate("Dialog_home", "Afficher:"))
        self.pushButton_display_layers.setText(_translate("Dialog_home", "Layers"))
        self.pushButton_display_trajectories.setText(_translate("Dialog_home", "Trajectoires"))
        self.pushButton_display_points.setText(_translate("Dialog_home", "Points"))
        self.label_warning.setText(_translate("Dialog_home", "Attention au temps de chargement !"))
        self.label_studyName.setText(_translate("Dialog_home", "Study name:"))
        self.label_studyAdress.setText(_translate("Dialog_home", "..."))
        self.label_version.setText(_translate("Dialog_home", "Version: x.xx"))
        self.labelIsCFR.setText(_translate("Dialog_home", "CFR-DLF"))
