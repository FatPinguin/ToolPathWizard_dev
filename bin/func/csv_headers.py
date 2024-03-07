from .common_variables import SLICERVERSION, fdmPerimeter, fdmInfill, milling, tapeLayingAirPulse, tapeLayingLaser, fdmPelletPerimeter, fdmPelletInfill, fdmFiberInfill, fdmFiberPerimeter, generic

### Fab/Op modes

standardHeader = ["Operation id", "Instruction", "Operation type", "Layer id", "Curve id", "Point id",
                      "X coord (mm)", "Y coord (mm)", "Z coord (mm)",
                      "Tangent vector X (mm)", "Tangent vector Y (mm)", "Tangent vector Z (mm)", 
                      "Normal vector X (mm)", "Normal vector Y (mm)", "Normal vector Z (mm)", 
                      "Tool rot Z (deg)", "Tool tilt Y (deg)", "7th axis pos (robots units)", "7th axis speed (robots units)",
                      "Distance on curve (mm)", "Total distance (mm) (only active passes)", "Speed (mm/s)", "Stop flag: continuous/stop here (0/1)"]

genericHeader = ["No tool selected"]

headerFdmPellet = ["Flow rate (mm3/s)", "Extruder temp (deg)", "Extrude: off/on (0/1)", "Direction: retract/push (0/1)", "Aux output 1 ", "Aux output 2 (*)"]

headerMilling = ["Spindle: off/on (0/1)", "Spindle speed (rev/min) or (0 to 1)", "Aux output 1 (*)", "Aux output 2 (*)", "Aux output 3 (*)", "Aux output 4 (*)"]

headerFdmFillament = ["Relative Filament Feed (mm) [incremental]", "Filament feed speed (mm/s)", "Part cooling: off/on (0/1)", "Extruder temp (deg)", "Aux output 1 (*)", "Aux output 2 (*)"]

headerTapeLayingLaser = ["Laser state: off/on (0/1)", "Laser power (laser controller units)", "Cut flag: idle/cut (0/1)", "Aux output 1 (*)", "Version %s"%(SLICERVERSION)]

headerTapeLayingAirPulse = ["Prep trigger off/on (0/1)", "Roller down off/on (0/1)", "Air flow off/on (0/1)", "Cut trigger off/on (0/1)", "Feed rate (mm/s)"]

headerFdmFiber = ["Relative Filament Feed (mm) [incremental]", "Filament feed speed (mm/s)", "Part cooling: off/on (0/1)", "Extruder temp (deg)", "Cut: off/on (0/1)", "Aux output 2 (*)"]


def fabrication_header(fabMode:int):
    if fabMode == generic:
        toolHeader = genericHeader
    elif fabMode == fdmPelletPerimeter or fabMode == fdmPelletInfill:
        toolHeader = headerFdmPellet
    elif fabMode == milling:
        toolHeader = headerMilling
    elif fabMode == fdmPerimeter or fabMode == fdmInfill:
        toolHeader = headerFdmFillament
    elif fabMode == tapeLayingLaser:
        toolHeader = headerTapeLayingLaser
    elif fabMode == tapeLayingAirPulse:
        toolHeader = headerTapeLayingAirPulse
    elif fdmFiberInfill or fabMode == fdmFiberPerimeter:
        toolHeader = headerFdmFiber
    return standardHeader + toolHeader
