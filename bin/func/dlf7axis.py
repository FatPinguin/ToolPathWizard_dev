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


def dlf_7_axis_rotation(vectInPlane, normPlane, ptNorm:cls_vector):
    # Vérifier l'orthogonalité à la selection des vecteurs  : Ortho_test
    # Créer plan sur lequel projeter : Plane_1 = geompy.MakePlane2Vec(vectTang, vectNorm, Dim)
    # Projection : GEOM_Object = geompy.MakeProjection(Source, Target)
    pN = np.array([ptNorm.vx, ptNorm.vy, ptNorm.vz])
    vProj = plane_projection(normPlane, pN)
    #angle = angle_difference(normPlane, vProj)
    print(f"\nAngle d'origine:{pN}\tProjection: {vProj}\tvInPlane: {vectInPlane}\tnormPlane: {normPlane}")
    teta = angle_difference(vectInPlane, vProj)
    print(f"\tRes. Angle vP-vProj: {teta}")
    teta = orientation(vProj, normPlane, vectInPlane, teta)
    print(f"\tRes. Angle vP-vProj (new): {teta}")
    return teta


def plane_projection(n, u):
    # n = vecteur normal au plan (axe de rotation)
    # u = vecteur du point
    # v = vecteur projeté dans le plan : projection orthogonale du vecteur u sur le plan orthogonal à n
    v = np.cross(n, np.cross(u, n))
    return v


def angle_difference(w, v):
    # w = vecteur de référence dans le plan
    # v = vecteur "mobile" (projeté)

    #print(f"Angles 3D tan_norm:{np.rad2deg(np.arctan2(np.linalg.norm(np.cross(w, v)), np.dot(w, v)))}")
    print(f"Angles 3D tan2:{np.rad2deg(np.arctan2(np.cross(w, v), np.dot(w, v)))}")
    angle = np.rad2deg(np.arctan2(np.linalg.norm(np.cross(w, v)), np.dot(w, v)))
    #print(f"Angle COS: {np.rad2deg(np.arccos(np.dot(w,v) / (np.linalg.norm(w) * np.linalg.norm(v))))}deg")
    #if angle < np.single(0):
    #    return angle + np.single(360)
    #sin = np.linalg.norm(np.cross(w, v)) / (np.linalg.norm(w) * np.linalg.norm(v))
    #print("sin", sin)
    #cos = np.dot(w, v) / (np.linalg.norm(w) * np.linalg.norm(v))
    #print("cos", cos)
    #if cos < 0:
    #    angle = -angle
    return angle


def dlf_7_axis_point_modification(sortedFabricationSteps:list, orthoVector, rotVector):
    curve:cls_curve
    point:cls_point
    for [curveList, surfaceId, fabricationMode, operationID] in sortedFabricationSteps:
        for curve in curveList:
            for point in curve.pointList:
                point.pos7axis = dlf_7_axis_rotation(orthoVector, rotVector, point.normalVector)
    return sortedFabricationSteps


def orientation(v, n, w, teta):
    # n = vecteur normal au plan (axe de rotation)
    # v = vecteur projeté dans le plan
    # w = vecteur de référence dans le plan
    # k = vecteur orthogonal à v et n (dans ce sens)
    # teta = angle entre v et w
    # phi = angle entre k et w
    k = np.cross(v, n)
    phi = angle_difference(w, k)
    print(f"teta: {teta}\tphi: {phi}")
    if (0 <= teta <= 90) and (0 <= phi <= 90):  #if teta in range(0, 90) and phi in range(0, 90):
        return teta
    elif (90 <= teta <= 180) and (0 <= phi <= 90):  #elif teta in range(90, 180) and phi in range(0, 90):
        return teta
    elif (90 <= teta <= 180) and (90 <= phi <= 180):  #elif teta in range(90, 180) and phi in range(90, 180):
        return -teta +360
    elif (0 <= teta <= 90) and (90 <= phi <= 180):  #elif teta in range(0, 90) and phi in range(90, 180):
        return -teta +360