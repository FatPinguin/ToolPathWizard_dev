from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5 import QtCore

from .Classes import cls_data_structure, cls_volume, cls_surfaces_grp, cls_surface, cls_operation
from .environment import dataStruct, salome
from ..viz.user_com import message_error
from .common_variables import succes, qtVolumeType, qtGroupType, qtOperationType, qtSurfaceType, qtOpeModeDict
from .navigate import find_volume_in_dataStruct


def convert_data_structure_to_QT_tree_widget(tree:QTreeWidget, data:cls_data_structure):
    tree.clear()
    tree.setColumnCount(4)
    tree.setHeaderLabels(["Objet", "Export", "Position", "ID"])
    tree.setColumnWidth(0, 350)
    tree.setColumnWidth(1, 70)
    tree.setColumnWidth(2, 90)
    #tree.setColumnWidth(3, 180)
    volume:cls_volume
    group:cls_surfaces_grp
    surface:cls_surface
    operation:cls_operation
    for volume in data.volumeList:
        volumeItem = QTreeWidgetItem(tree, ['%s'%(salome.IDToObject(volume.volumeId).GetName()), "", "", volume.volumeId])
        for group in volume.surfaceGroupList:
            surfaceGroupItem = QTreeWidgetItem(volumeItem, ['%s'%(salome.IDToObject(group.surfacesGrpId).GetName()), "", "", group.surfacesGrpId])
            for opName in data.generatedOperations:
                newMode = True
                for surface in group.surfaceList:
                    for operation in surface.operationList:
                        if operation.name == opName:
                            if newMode:
                                operationItem = QTreeWidgetItem(surfaceGroupItem, ['%s'%(salome.IDToObject(operation.ID).GetName()), "", str(operation.order), ""])
                                operationItem.setCheckState(1, False)
                                operationItem.setFlags(operationItem.flags() | QtCore.Qt.ItemIsEditable)
                                newMode = False
                            surfaceItem = QTreeWidgetItem(operationItem, ['%s'%(salome.IDToObject(surface.surfaceId).GetName()), "", "", surface.surfaceId])


def find_modif_QT_tree_widget(tree:QTreeWidget, data:cls_data_structure):
    exportDict = {}
    posList = []
    for opeGen in data.generatedOperations:
        operationItems = tree.findItems(opeGen, QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive)    #    operationItem = tree.findItems(qtOpeModeDict[operation.fabricationMode], QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive)[0]
        for item in operationItems:
            check = int(item.checkState(1))
            position = item.text(2).strip()
            print(f"{type(position)} #{position}#")
            if check != 0 and position != '...':  
                try:
                    position = float(position)
                except ValueError:
                    message_error(f"{opeGen} position #{position}# is a {type(position)}")
                    return False
                print('\tExport:', opeGen, 'pos:', '#', position, '#')
                exportDict[position] = opeGen
                posList.append(position)
                count = item.childCount()
                for i in range(count):
                    child = item.child(i).text(3)
                    print("\t\tDependent surface", child)
    print('dict:', exportDict)
    print('posList:', posList)
    posList = sorted(posList, key = lambda x:float(x))
    print('sorted posList:', posList)
    data.sortedOperations = []
    for pos in posList:
        data.sortedOperations.append(exportDict[pos])
    volume:cls_volume
    group:cls_surfaces_grp
    surface:cls_surface
    operation:cls_operation
    for volume in data.volumeList:
        for group in volume.surfaceGroupList:
            for surface in group.surfaceList:
                for operation in surface.operationList:
                    try :
                        data.sortedOperations.index(operation.name) #Si l'opération est trouvée: check export et maj position
                        operation.tbe = 1
                        operation.order = list(exportDict.keys())[list(exportDict.values()).index(operation.name)]
                    except ValueError: #Sinon, 
                        operation.tbe = 0
                        operation.order = '...'


def delete_in_data_structure_from_selection_in_tree(tree, selectedItems:list):
    print("Deletion of items selected and childs:")
    print(selectedItems)    #TODO - delete from study
    volume:cls_volume
    group:cls_surfaces_grp
    surface:cls_surface
    operation:cls_operation
    for itemId, itemType in selectedItems:
        if itemType == qtVolumeType:
            itemInDataStruct = find_volume_in_dataStruct(itemId)
            if itemInDataStruct:
                dataStruct.volumeList.remove(itemInDataStruct)
        elif itemType == qtGroupType:
            for volume in dataStruct.volumeList:
                for group in volume.surfaceGroupList:
                    if group.originalSurfaceId == itemId:
                        volume.surfaceGroupList.remove(group)
        elif itemType == qtSurfaceType:
            for volume in dataStruct.volumeList:
                for group in volume.surfaceGroupList:
                    for surface in group.surfaceList:    
                        if surface.surfaceId == itemId:
                            group.surfaceList.remove(surface)
        elif itemType == qtOperationType:
            for volume in dataStruct.volumeList:
                for group in volume.surfaceGroupList:
                    for surface in group.surfaceList:
                        for operation in surface.operationList:   
                            dataStruct.generatedOperations.remove(operation.name)#TODO - Vérifier que si déjà supprimé = pas de bug
                            if operation.fabricationMode == qtOpeModeDict[itemType]:
                                surface.operationList.remove(operation)
    print("Items deleted")
    return succes