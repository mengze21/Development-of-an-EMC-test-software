# -*- coding: utf-8 -*-

import sys
from PyQt5 import uic, QtWidgets

sys.path.append('gui')


class UiCalibration(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UiCalibration, self).__init__(parent)
        self.setupUi()

        # define signal slots
        self.toolButton_testparameter.clicked.connect(self.showCalibrationEditWindow)


    def setupUi(self):
        dialog = uic.loadUi("uifiles/KalibierungWindow_neu.ui", self)
        dialog.show()


    def showCalibrationEditWindow(self):
        dialog = CalibrationEditWindow(self)
        dialog.exec_()


class CalibrationEditWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CalibrationEditWindow, self).__init__(parent)
        uic.loadUi("uifiles/KalibierungEinstellen.ui", self)

        # define Signal Slots
        self.treeWidget_parameters.doubleClicked.connect(self.findParaEdit)
        self.toolButton_new.clicked.connect(self.findParaEdit)

    def findParaEdit(self):
        dialog = ParametersEditWindow(self)
        dialog.exec_()


class ParametersEditWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("uifiles/ParaEditWindow.ui", self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = UiCalibration()
    ui.setupUi()
    sys.exit(app.exec_())



