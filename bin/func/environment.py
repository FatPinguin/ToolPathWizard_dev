################## Importation des librairies Salomé ##########################################################
import salome
#import salome_notebook
#notebook = salome_notebook.NoteBook()

################## GEOM component #############################################################################
import GEOM
from salome.geom import geomBuilder
from salome.geom import geomtools

salome.salome_init()
currentStudy = None
currentStudy = salome.salome_study.myStudy
currentStudyName = salome.salome_study.myStudyName
#geompy=geomtools.getGeompy()
#gp=geomtools.getGeompy()
geompy = geomBuilder.New()
gstools = geomtools.GeomStudyTools()
gg = salome.ImportComponentGUI("GEOM")
#geompy.addToStudyAuto(-1)
#GetStudyID()
#GetStudyEntry() 	
#salome.salome_study.myStudy
#salome.salome_study.myStudyName
studyEditor = salome.kernel.studyedit.getStudyEditor()

################## Global structure #############################################################################
from .Classes import cls_machine_parameters, default_machine_settings, cls_data_structure
machineParameters:cls_machine_parameters = default_machine_settings()
dataStruct = cls_data_structure(currentStudyName, machineParameters)
