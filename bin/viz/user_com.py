from PyQt5 import QtCore, QtWidgets


def update_progressBar(guiBar, percent:float):
       guiBar.setValue(percent)
       return


def update_progressBar_and_label(guiBar, uiLabel, actual:int, total:int, label:str):
       percent = round((actual)/total*100)
       guiBar.setValue(percent)
       uiLabel.setText(f"{label} {actual}/{total} ({percent}%)")
       return


#def message_error(message):
#    msg = QtWidgets.QMessageBox()
#    msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
#    msg.setIcon(QtWidgets.QMessageBox.Critical)
#    msg.setText("Error")
#    msg.setInformativeText(message)
#    msg.setWindowTitle("Error")
#    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
#    msg.clickedButton()== msg.setStandardButtons(QtWidgets.QMessageBox.Ok) 
#    msg.exec()
#    return


def message_error(message, mainApp=None):
    msg = QtWidgets.QMessageBox()
    msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText("Error")
    msg.setInformativeText(message)
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.clickedButton()== msg.setStandardButtons(QtWidgets.QMessageBox.Ok) 
    if mainApp:
        #mainWindow()
        mainApp.win.show()
    msg.exec()


def message_information_no_main(message, title="Error information", icon="crit"):
    msg = QtWidgets.QMessageBox()
    msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    if icon == "crit":
        msg.setIcon(QtWidgets.QMessageBox.Critical)
    elif icon == "info":
        msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(title)
    msg.setInformativeText(message)
    msg.setWindowTitle("Information")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.clickedButton()== msg.setStandardButtons(QtWidgets.QMessageBox.Ok) 
    msg.exec()