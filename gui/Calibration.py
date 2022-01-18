# -*- coding: utf-8 -*-

import sys
from PyQt5 import uic, QtWidgets, QtChart, QtCore, QtGui
from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
sys.path.append('gui')


class Ui_Calibration(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Ui_Calibration, self).__init__(parent)
        self.setupUi()
        #self.paraWindow = ParametersEditWindow()

        # define signal slots
        self.toolButton_testparameter.clicked.connect(self.showCalibrationEditWindow)
        self.lineEdit_1.textChanged.connect(self.aaa)
        #self.signal.connect(self.set_fre)

    def setupUi(self):
        dialog = uic.loadUi("uifiles/KalibierungWindow_neu.ui", self)

        dialog.show()


    def showCalibrationEditWindow(self):
        dialog = CalibrationEditWindow(self)
        dialog.exec_()

    def set_fre(self):
        self.parapass.lineEdit_1.setText(self.lineEdit_frequency.text())
        #self.parapass.lineEdit_1.setText(self.lineEdit_frequency.text())

    def aaa(self):
        print("1")


class CalibrationEditWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CalibrationEditWindow, self).__init__(parent)
        uic.loadUi("uifiles/KalibierungEinstellen.ui", self)

        # define Signal Slots
        self.treeWidget_parameters.doubleClicked.connect(self.findParaEdit)
        #self.toolButton_new.clicked.connect(self.findParaEdit)
        self.toolButton_new.clicked.connect(self.setnewPara)

    def findParaEdit(self):
        dialog = ParametersEditWindow(self)
        #self.lineEdit_frequency.setText(" ")
        dialog.exec_()

    def setnewPara(self):
        dialog = ParametersEditWindow(self)
        dialog.lineEdit_frequency.setText("")
        dialog.lineEdit_step.setText("")
        dialog.lineEdit_testlevel.setText("")
        dialog.lineEdit_Dwell.setText("")
        dialog.lineEdit_m1fre.setText("")
        dialog.lineEdit_m1dep.setText("")
        dialog.lineEdit_3.setText("")
        dialog.lineEdit_4.setText("")
        dialog.exec_()




class ParametersEditWindow(QtWidgets.QDialog):

    signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("uifiles/ParaEditWindow.ui", self)
        self.parapass = Ui_Calibration()

        self.edit_var_parameters.accepted.connect(self.passingInfor)

    def passingInfor(self):
        self.parapass.lineEdit_1.setText(self.lineEdit_frequency.text())
        print(self.parapass.lineEdit_1.text())

    #def emit_fre(self):
        #new_fre = self.lineEdit_frequency.text()
        #self.signal.emit(new_fre)
        #self.parapass.lineEdit_1.setText(self.lineEdit_frequency.text())
        #print(self.parapass.lineEdit_1.text())
        #print(self.lineEdit_frequency.text())
        #new_frequency = self.lineEdit_frequency.text()
        #self.signal.emit(new_frequency)


##

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Calibration()
    ui.setupUi()
    sys.exit(app.exec_())



