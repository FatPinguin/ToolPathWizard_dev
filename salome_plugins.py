import salome_pluginsmanager


def slicer_dev(context):
  import ToolPathWizard_dev.bin.viz.main_viz as GUI
  toolbar = GUI.mainWindow()
  toolbar.win.show()
from ToolPathWizard_dev.bin.func.common_variables import SLICERVERSION
salome_pluginsmanager.AddFunction(f'Tool Path Wizard v{SLICERVERSION}',f'Tool Path Wizard dev. v{SLICERVERSION}',slicer_dev)
