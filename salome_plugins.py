import salome_pluginsmanager


def slicer_dev(context):
  import ToolPathWizard_dev.bin.viz.main_viz as GUI
  toolbar = GUI.mainWindow()
  toolbar.win.show()
from ToolPathWizard_dev.bin.func.common_variables import SLICERVERSION
salome_pluginsmanager.AddFunction(f'Tool Path Wizard v{SLICERVERSION}',f'Tool Path Wizard dev. v{SLICERVERSION}',slicer_dev)

def myMakeHelix(context):
   import ToolPathWizard_dev.bin.makeHelix as makeHelix
   makeHelix.MakeHelixGUI()

def myMakeHeliSurf(context):
   import ToolPathWizard_dev.bin.makeHelix as makeHelix
   makeHelix.MakeHelicalSurfaceGUI()

salome_pluginsmanager.AddFunction('Make Helix','Make Helix',myMakeHelix)
salome_pluginsmanager.AddFunction('Make Helical Surface','Make Helical Surface',myMakeHeliSurf)
