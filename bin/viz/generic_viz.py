from ..func.environment import salome, gstools
import ToolPathWizard_dev.bin.func.environment as env
from ..func.Classes import cls_surfaces_grp, cls_volume
from .user_com import message_information_no_main


def hide_object(objectList:list, flag):
    for object in objectList:
        if flag:
            object.hide()
        else:
            object.show()


def disable_objects(objectList:list, flag):
    for object in objectList:
        object.setDisabled(flag)
    return


def check_object_type(mainApp, geomObject, geomObjectID, typeList:list):
    """Checks if the object is one of the expected object types.
    Args:
        object (GEOm object): Object to be tested
        typeList (list): List of expected types

    Returns:
        bool: Is an expected type
        string: Object type
    """
    objectType = geomObject.GetShapeType()
    for type in typeList:
        if str(objectType) == type:
            #print("Object %s is a %s" %(geomObjectID, objectType))
            return True, objectType
    message_information_no_main("Object %s isn't compatible with types %s" %(geomObjectID, typeList))
    #message_error("Object %s isn't compatible with types %s" %(geomObjectID, typeList), mainApp)
    return False, objectType


def get_objects_from_study(mainApp):
    # get the selected objects
    objectList = []
    objectIdList = []
    selCount = salome.sg.SelectedCount() # the number of selected items
    if selCount:
        for i in range(selCount):
            ID = salome.sg.getSelected(i) #get the entry ID of i-th selected item
            objectList.append(salome.IDToObject(ID)) #output : Object
            objectIdList.append(ID)
        return selCount, objectList, objectIdList
    else:
        message_information_no_main('You must select an object')
        return 0, objectList, objectIdList


def selection_indicator(guiObject, flagObjectType):
    if flagObjectType:
        guiObject.setText("<span style = \'font-size:20px\'> &#128077;</span>")
    else:
        guiObject.setText("<span style = \'font-size:20px\'> &#129324;</span>")


def display_IDs_of_selected_objects(guiObject, objectIdList):
    text = "Entry: " + str(objectIdList)
    guiObject.setText(text)


def selection_method(mainApp, guiIndicator, guiEntryDisplay, authorisedTypesList):
    selCount, objectList, objectIdList = get_objects_from_study(mainApp)
    if selCount:
        flagObjectType = True
    else:
        flagObjectType = False
    for i in range(len(objectList)) :
        geomObject = objectList[i]
        geomObjectID = objectIdList[i]
        flag, objectType = check_object_type(mainApp, geomObject, geomObjectID, authorisedTypesList)
        if flag == False:
            flagObjectType = False
    selection_indicator(guiIndicator, flagObjectType)
    display_IDs_of_selected_objects(guiEntryDisplay, objectIdList)
    return objectList, objectIdList


def get_value_in_line_edit(mainApp, guiLineEdit, guiIndicator):
    try:
        value = float(guiLineEdit.text())
        selection_indicator(guiIndicator, True)
        return value
    except ValueError or value == 0.0:
        selection_indicator(guiIndicator, False)
        message_information_no_main("Value error.")
        return None


def search_group_in_volumes(groupId:str):
    volume:cls_volume
    group:cls_surfaces_grp
    for volume in env.dataStruct.volumeList:
        for group in volume.surfaceGroupList:
            if group.surfacesGrpId == groupId:
                return group
    return None


def destroy_temporary_object(object):
    try:
        idToDelete = object.GetEntry()
        env.gg.eraseGO(idToDelete,True)
        env.studyEditor.removeItem(object,True)
        object.Destroy()
    except:
        message_information_no_main("Deletion of object %s failed."%(object.GetEntry()))


def show_item_colorized(id:str, color:list=[143,28,247]):
    gstools.displayShapeByEntry(id, color)
    return