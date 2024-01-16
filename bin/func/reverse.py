from .environment import geompy, gg

def reverse_func(selection:list):
    for item in selection:
        geompy.ChangeOrientationShell(item)
    return


def display_wires(selectionIds:list):
    for id in selectionIds:
        gg.setVectorsMode(id, True)
    return


def verify_type(item)->bool:
    stype = str(item.GetShapeType())
    if stype == "WIRE" or stype == "EDGE":
        return True
    return False


def search(selectionIds:list, entry:str):
    try:
        return selectionIds.index(entry)
    except ValueError:
        return None
            