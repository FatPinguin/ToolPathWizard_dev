# ToolPathWizard_dev
 Generator of tool trajectories and tool control

# Installation
copy all the content into the folder : C:\Users\\%USERNAME%\\.config\salome\Plugins\ToolPathWizard_dev

(create the Plugins\ToolPathWizard_dev folder if needed)

# Modules
Need to install and update several modules :
- Run "C:\SALOME-9.10.0\run_salome_shell.bat"
- if needed $ python -m pip install --upgrade pip
- $ python -m pip install --upgrade matplotlib
- $ python -m pip uninstall pandas
- $ python -m pip install pandas

# Configure plugin file "salome_plugins.py"
Create or edit salome_plugins.py in : C:\Users\\%USERNAME%\\.config\salome\Plugins

An example is provide in this Git repo and should work if this is the only custom plugin that you want to load.
