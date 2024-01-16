from .Classes import cls_volume, cls_surfaces_grp, cls_surface, cls_operation, cls_curve, cls_point
from .environment import dataStruct


def find_volume_in_dataStruct(volumeID:str):
    volume:cls_volume
    for volume in dataStruct.volumeList:
        if volume.volumeId == volumeID :
            return volume
    return None


def find_similar_surface_group(groupType:int, referenceSurfaceId:str, volume:cls_volume):
    surfaceGroup:cls_surfaces_grp
    for surfaceGroup in volume.surfaceGroupList:
        if surfaceGroup.typeGenerated == groupType and surfaceGroup.originalSurfaceId == referenceSurfaceId :
            return surfaceGroup
    return None


def find_surface_in_surface_group(surfaceId:str, surfaceGroup:cls_surfaces_grp):
    surface:cls_surface
    for surface in surfaceGroup.surfaceList:
        if surface.surfaceId == surfaceId:
            return surface
    return None


def find_similar_operations_in_surface_group(fabricationMode:int, surfaceGroup:cls_surfaces_grp):
    surface:cls_surface
    operation:cls_operation
    operationMatchList = []
    for surface in surfaceGroup.surfaceList:
        for operation in surface.operationList:
            if operation.fabricationMode == fabricationMode:
                operationMatchList.append(operation)
    return operationMatchList


def find_item_from_id(id:str):
    volume:cls_volume
    surfaceGroup:cls_surfaces_grp
    surface:cls_surface
    operation:cls_operation
    curve:cls_curve
    point:cls_point
    for volume in dataStruct.volumeList:
        if volume.volumeId == id:
            return volume
        for surfaceGroup in volume.surfaceGroupList:
            if surfaceGroup.surfacesGrpId == id:
                return surfaceGroup
            for surface in surfaceGroup.surfaceList:
                if surface.surfaceId == id:
                    return surface
                for operation in surface.operationList:
                    if operation.ID == id:
                        return operation
                    for curve in operation.curveList:
                        if curve.curveId == id:
                            return curve
                        for point in curve.pointList:
                            if point.pointId == id:
                                return point