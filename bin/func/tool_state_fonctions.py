from .environment import dataStruct
from .common_variables import MACHINING, APPROACH, RETRACT, TRAVEL, fdmPerimeter, fdmInfill, milling, tapeLayingAirPulse, tapeLayingLaser, fdmPelletPerimeter, fdmPelletInfill, fdmFiberInfill, fdmFiberPerimeter, generic

false = 0
true = 1
void = '0'

def tool_head_state(fabricationMode:int, moveType:int, increment:int, curveLength:float, distanceOnCurve:float, distOnApproach:float=None):#, startDistance:float, endDistance:float): #TODO - Gérer les opérations intermédiaires à des distances définies (exemple : start laser; cut strip; stop laser) (rétracter plastique)
    ### RBDK path streamer read 6 columns
    if fabricationMode == fdmPerimeter:
        return fdm_perimeter_tool_state(moveType, increment)
    elif fabricationMode == fdmInfill:
        return fdm_infill_tool_state(moveType, increment)
    elif fabricationMode == fdmPelletPerimeter:
        return fdm_pellet_perimeter_tool_state(moveType, distanceOnCurve, curveLength)
    elif fabricationMode == fdmPelletInfill:
        return fdm_pellet_infill_tool_state(moveType, distanceOnCurve, curveLength)
    elif fabricationMode == milling :
        return milling_tool_state(moveType)
    elif fabricationMode == tapeLayingLaser:
        return laser_tape_tool_state(moveType, increment, distanceOnCurve, curveLength)
    elif fabricationMode == tapeLayingAirPulse:
        return air_tape_tool_state(moveType, distanceOnCurve, curveLength, distOnApproach)
    else:
        return ["No tool selected"]
    

#TODO - Ajouter une gestion des STOP_TOOL à la fin d'une séquence d'opérations
def generic_tool_state():
    return [void, void, void, void, void, void]


def fdm_infill_tool_state(moveType:int, increment:float):
    #[relative filament fee (mm) -> incremental; filament feed speed (mm/s), part cooling (bool), extruder temp (°C)]    pass
    extruderTemp = dataStruct.machineParam.fdmFilament.extruderTemp
    if moveType == MACHINING : #ajouter ici les cas de rétractation du filament
        filamentSpeed = dataStruct.machineParam.fdmFilament.filamentSpeed
        cooling = true
        return [increment, filamentSpeed, cooling, extruderTemp, void, void]
    elif moveType == APPROACH :
        return [0,0,false,extruderTemp, void, void]
    elif moveType == RETRACT or moveType == TRAVEL :
        return [0,0,false,extruderTemp, void, void]


def fdm_perimeter_tool_state(moveType:int, increment:float):
    #[relative filament fee (mm) -> incremental; filament feed speed (mm/s), part cooling (bool), extruder temp (°C)]    pass
    extruderTemp = dataStruct.machineParam.fdmFilament.extruderTemp
    if moveType == MACHINING : #ajouter ici les cas de rétractation du filament
        filamentSpeed = dataStruct.machineParam.fdmFilament.filamentSpeed
        return [increment, filamentSpeed, true, extruderTemp, void, void]
    elif moveType == APPROACH :
        return [0,0,false,extruderTemp, void, void]
    elif moveType == RETRACT or moveType == TRAVEL :
        return [0,0,false,extruderTemp, void, void]


def fdm_pellet_infill_tool_state(moveType:int, distanceOnCurve:float, curveLength:float):
    #[extruder state (bool); extrusion direction(bool); extrudeur temp (°C); extrudeur speed (mm/s)]
    extrTemp = dataStruct.machineParam.fdmPellet.extruderTemp
    extrSpeed = dataStruct.machineParam.fdmPellet.screwSpeed
    if moveType == MACHINING : #ajouter ici les cas de rétractation du filament
        if distanceOnCurve >= (curveLength - dataStruct.machineParam.fdmPellet.distanceToRetract):  #Retract filament
            extrude = 1
            pull = 1
        else :
            extrude = 1
            pull = 0    #Push
    elif moveType == APPROACH :
        extrude = 1
        pull = 0
    elif moveType == RETRACT :
        extrude = 0
        pull = 1
    elif moveType == TRAVEL :
        extrude = 0
        pull = 0
    return [extrSpeed, extrTemp, extrude, pull, void, void] #0, 0


def fdm_pellet_perimeter_tool_state(moveType:int, distanceOnCurve:float, curveLength:float):
    extrTemp = dataStruct.machineParam.fdmPellet.extruderTemp
    extrSpeed = dataStruct.machineParam.fdmPellet.screwSpeed
    if moveType == MACHINING : #ajouter ici les cas de rétractation du filament
        if distanceOnCurve >= (curveLength - dataStruct.machineParam.fdmPellet.distanceToRetract):  #Retract filament
            extrude = 1
            pull = 1
        else :
            extrude = 1
            pull = 0    #Push
    elif moveType == APPROACH :
        extrude = 1
        pull = 0
    elif moveType == RETRACT :
        extrude = 0
        pull = 1
    elif moveType == TRAVEL :
        extrude = 0
        pull = 0
    return [extrSpeed, extrTemp, extrude, pull, void, void] #0, 0


def milling_tool_state(moveType:int):
    #[spindle state (bool); spindle speed (rev/min)]
    if moveType == MACHINING : #ajouter ici les actions en un point
        return [true, dataStruct.machineParam.milling.spindleSpeed, void, void, void, void]
    elif moveType == APPROACH :
        return [true, dataStruct.machineParam.milling.spindleSpeed, void, void, void, void]
    elif moveType == RETRACT or moveType == TRAVEL :
        return [false, 0, void, void, void, void]


#old
#def laser_tape_tool_state(moveType:int, increment:float, distanceOnCurve:float, curveLength:float, isFirstPoint):
#    #[Tape feed (mm); tape feed speed (mm/s); laser state (on/off); laser power (w); cut flag (bool)]
#    if moveType == MACHINING : #ajouter ici les actions en un point
#        if isFirstPoint:
#            increment = 0
#            tapeFeedSpeed = 0
#        else:
#            tapeFeedSpeed = dataStruct.machineParam.laserTape.feedSpeed
#        laserPower = dataStruct.machineParam.laserTape.laserPower
#        distTurnOnLaser = dataStruct.machineParam.laserTape.laserStartingDistance
#        distCutTape = curveLength - dataStruct.machineParam.laserTape.cuttingDistance
#        distTurnOffLaser = curveLength - dataStruct.machineParam.laserTape.laserStopingDistance
#        if distanceOnCurve <= (distTurnOnLaser - increment/2): #Dépose avant d'allumer le laser
#            return [increment, tapeFeedSpeed, false, 0, false]
#        elif distanceOnCurve > (distTurnOnLaser - increment/2) and distanceOnCurve <= (distTurnOffLaser - increment/2) : #Dépose et laser ON
#            if distanceOnCurve > (distCutTape - increment/2) and distanceOnCurve <= (distCutTape + increment/2) : #Coupe la bande (1 point)
#                return [increment, tapeFeedSpeed, true, laserPower, true]
#            return [increment, tapeFeedSpeed, true, laserPower, false]
#        elif distanceOnCurve > (distTurnOffLaser - increment/2) : #Extinction laser
#            return [increment, tapeFeedSpeed, false, 0, false]
#    elif moveType == APPROACH or moveType == RETRACT :
#        return [0, 0, false, 0, false]


def laser_tape_tool_state(moveType:int, increment:float, distanceOnCurve:float, curveLength:float):
    #[Tape feed (mm); tape feed speed (mm/s); laser state (on/off); laser power (w); cut flag (bool)]
    if moveType == MACHINING : #ajouter ici les actions en un point
        laserPower = dataStruct.machineParam.laserTape.laserPower
        distTurnOnLaser = dataStruct.machineParam.laserTape.laserStartingDistance
        distCutTape = curveLength - dataStruct.machineParam.laserTape.cuttingDistance
        distTurnOffLaser = curveLength - dataStruct.machineParam.laserTape.laserStopingDistance
        if distanceOnCurve <= (distTurnOnLaser - increment/2): #Dépose avant d'allumer le laser
            return [false, 0, false]
        elif distanceOnCurve > (distTurnOnLaser - increment/2) and distanceOnCurve <= (distTurnOffLaser - increment/2) : #Dépose et laser ON
            if distanceOnCurve > (distCutTape - increment/2) and distanceOnCurve <= (distCutTape + increment/2) : #Coupe la bande (1 point)
                return [true, laserPower, true]
            return [true, laserPower, false]
        elif distanceOnCurve > (distTurnOffLaser - increment/2) : #Extinction laser
            return [false, 0, false]
    elif moveType == APPROACH or moveType == RETRACT or moveType == TRAVEL :
        return [false, 0, false, void, void]
    

#def laser_tape_tool_state(moveType:int, increment:float, distanceOnCurve:float, curveLength:float, isFirstPoint):
#    #[Tape feed (mm); tape feed speed (mm/s); laser state (on/off); laser power (w); cut flag (bool)]
#    if moveType == MACHINING : #ajouter ici les actions en un point
#        if isFirstPoint:
#            increment = 0
#        laserPower = dataStruct.machineParam.laserTape.laserPower
#        distTurnOnLaser = dataStruct.machineParam.laserTape.laserStartingDistance
#        distCutTape = curveLength - dataStruct.machineParam.laserTape.cuttingDistance
#        distTurnOffLaser = curveLength - dataStruct.machineParam.laserTape.laserStopingDistance
#        if distanceOnCurve <= (distTurnOnLaser - increment/2): #Dépose avant d'allumer le laser
#            return [false, 0, false]
#        elif distanceOnCurve > (distTurnOnLaser - increment/2) and distanceOnCurve <= (distTurnOffLaser - increment/2) : #Dépose et laser ON
#            if distanceOnCurve > (distCutTape - increment/2) and distanceOnCurve <= (distCutTape + increment/2) : #Coupe la bande (1 point)
#                return [true, laserPower, true]
#            return [true, laserPower, false]
#        elif distanceOnCurve > (distTurnOffLaser - increment/2) : #Extinction laser
#            return [false, 0, false]
#    elif moveType == APPROACH or moveType == RETRACT or moveType == TRAVEL :
#        return [false, 0, false]
    

#def air_tape_tool_state_old(moveType:int, increment:float, distanceOnCurve:float, curveLength:float):
#    #[Tape feed (mm); tape feed speed (mm/s); heating state (bool); heater power (bool); cut flag (bool); roller pressure (bool)]
#    if moveType == MACHINING : #ajouter ici les actions en un point
#        tapeFeedSpeed = dataStruct.machineParam.airTape.feedRate
#        distTurnOnAir = dataStruct.machineParam.airTape.airStartingDistance
#        distCutTape = curveLength - dataStruct.machineParam.airTape.cuttingDistance
#        distTurnOffAir = curveLength - dataStruct.machineParam.airTape.airStopingDistance
#        if distanceOnCurve <= (distTurnOnAir - increment/2): #Dépose avant d'allumer l'air
#            return [increment, tapeFeedSpeed, false, false, false, false]
#        elif distanceOnCurve > (distTurnOnAir - increment/2) and distanceOnCurve <= (distTurnOffAir - increment/2) : #Dépose et laser ON
#            if distanceOnCurve > (distCutTape - increment/2) and distanceOnCurve <= (distCutTape + increment/2) : #Coupe la bande (1 point)
#                return [increment, tapeFeedSpeed, true, true, true, true]
#            return [increment, tapeFeedSpeed, true, true, false, true]
#        elif distanceOnCurve > (distTurnOffAir - increment/2) : #Extinction de l'air
#            return [increment, tapeFeedSpeed, false, false, false, true]
#    elif moveType == APPROACH or moveType == RETRACT or moveType == TRAVEL :
#        return [0, 0, false, false, false, false]
    

def air_tape_tool_state(moveType:int, distanceOnCurve:float, curveLength:float, distOnApproach:float):
    """Composite automated tape layup tool conditions:
    - 1st approach point : Prep trigger = 1 --> next points = 0
    - If the distance to the end of the approach is less than RollDownDist lower the roller (1).
        - Raise it at the last point of the material deposit (0).
    - If the distance to the end of the approach is less than AirStartDist activate the airflow (1).
        - Stop it at the last point of the material deposit (0).

    Args:
        moveType (int): APPROACH, MACHINING, RETRACT, TRAVEL
        distanceOnCurve (float): _description_
        curveLength (float): _description_
        distOnApproach (float): _description_
        approachLength (float): _description_

    Returns:
        toolCommands (list): [Prep trigger off/on (0/1); Roller down off/on (0/1); Air flow off/on (0/1); Cut trigger off/on (0/1); Feed rate (mm/s)]
    """
    if moveType == MACHINING : #ajouter ici les actions en un point
        distCutTape = curveLength - dataStruct.machineParam.airTape.cuttingDistance
        feedRate = 0
        cutTrig = 0
        if distanceOnCurve <= distCutTape:
            feedRate = dataStruct.machineParam.airTape.feedRate
        if distanceOnCurve == distCutTape:
            cutTrig = 1
        return [0, 1, 1, cutTrig, feedRate, void]
    
    elif moveType == APPROACH :
        approachLength = dataStruct.machineParam.generics.securityDistance
        distLowerRoller = dataStruct.machineParam.airTape.rollerDownDistance
        distTurnOnAir = dataStruct.machineParam.airTape.airStartingDistance
        prepTrig = 0
        rollDown = 0
        airFlow = 0
        if distOnApproach <= 1E-3 :
            prepTrig = 1
        if distOnApproach >= (approachLength-distLowerRoller):
            rollDown = 1
        if distOnApproach >= (approachLength-distTurnOnAir):
            airFlow = 1
        return [prepTrig, rollDown, airFlow, 0, 0, void]  #Prep trigger = 1 ; Feed rate 0 mm/s
    
    elif moveType == RETRACT or moveType == TRAVEL :
        return [0, 0, 0, 0, 0, void]  #Feed rate 0 mm/s

    #    if distanceOnCurve <= (distTurnOnAir - increment/2): #Dépose avant d'allumer l'air
    #        return [0, 0, 0, 0, feedRate]
    #    elif distanceOnCurve > (distTurnOnAir - increment/2) and distanceOnCurve <= (distTurnOffAir - increment/2) : #Dépose et laser ON
    #        if distanceOnCurve > (distCutTape - increment/2) and distanceOnCurve <= (distCutTape + increment/2) : #Coupe la bande (1 point)
    #            return [0, 0, 0, 0, feedRate]
    #        return [0, 0, 0, 0, feedRate]
    #    elif distanceOnCurve > (distTurnOffAir - increment/2) : #Extinction de l'air
    #        return [0, 0, 0, 0, feedRate]
    #elif moveType == APPROACH or moveType == RETRACT or moveType == TRAVEL :
    #    return [0, 0, 0, 0, 0]  #Feed rate 0 mm/s
    
