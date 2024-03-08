import numpy as np

from .Classes import cls_curve, cls_vector, cls_point
from .environment import geompy
from .errors import Orthogonality_error


def vectors_verification(geomV1, geomV2):
    v1 = geompy.VectorCoordinates(geomV1)
    v2 = geompy.VectorCoordinates(geomV2)
    v1 = np.array(v1)
    v2 = np.array(v2)
    try :
        check = ortho_check(v1, v2)
    except:
        return False, v1, v2
    return check, v1, v2


def ortho_check(u, v):
    if np.dot(u, v) == 0:    #u.v = 0 -> Vecteurs orthogonaux
        return True
    raise Orthogonality_error


def dlf_7_axis_rotation(orthoVector, ptNorm:cls_vector):
    # Vérifier l'orthogonalité à la selection des vecteurs  : Ortho_test
    # Créer plan sur lequel projeter : Plane_1 = geompy.MakePlane2Vec(vectTang, vectNorm, Dim)
    # Projection : GEOM_Object = geompy.MakeProjection(Source, Target)
    pN = np.array([ptNorm.vx, ptNorm.vy, ptNorm.vz])
    v = plane_projection(orthoVector, pN)
    angle = angle_difference(orthoVector, v)
    return angle


def plane_projection(n, u):
    v = np.cross(n, np.cross(u, n))
    return v


def angle_difference(n, v):
    angle = np.rad2deg(np.arctan2(np.cross(n, v), np.dot(n, v)))[0]
    if angle < np.single(0):
        return angle + np.single(360)
    return angle


def dlf_7_axis_point_modification(sortedFabricationSteps:list, orthoVector):
    curve:cls_curve
    point:cls_point
    for [curveList, surfaceId, fabricationMode, operationID] in sortedFabricationSteps:
        for curve in curveList:
            for point in curve.pointList:
                point.pos7axis = dlf_7_axis_rotation(orthoVector, point.normalVector)
    return sortedFabricationSteps