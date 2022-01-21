# -*- coding: utf-8 -*-

import sys
from PyQt5 import uic, QtWidgets, QtChart, QtCore, QtGui
from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from openpyxl.descriptors import Default

from thread_FS_Calib import External_FS_Calib
sys.path.append('gui')
#global position

class Ui_Calibration(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Ui_Calibration, self).__init__(parent)
        self.setupUi()
        self.Position = int(self.treeWidget_info.topLevelItem(0).text(1))
        self.Polarisation = str(self.treeWidget_info.topLevelItem(1).text(1))
        # the parameters can later get from setting info
        self.FieldStrength = 30
        self.StartFreq = int(self.treeWidget_info.topLevelItem(2).text(1).replace("M", "")) * 1000000
        self.FreStep = int(self.treeWidget_info.topLevelItem(3).text(1).replace("%", "")) * 0.01
        self.MaxFreq = 1000000000
        self.level = 30
        #self.paraWindow = ParametersEditWindow()

        print("Strat Frequenz ist %s" %self.StartFreq)
        print(self.FreStep)

        # define signal slots
        self.toolButton_testparameter.clicked.connect(self.showCalibrationEditWindow)
        self.toolButton_start.clicked.connect(self.start_CaliThread)
        #self.treeWidget_info.itemChanged.connect(self.deal_parameters)
        #self.signal.connect(self.set_fre)

        #self.a = str(self.treeWidget_info.topLevelItem(0).text(1))
        #self.b = str(self.treeWidget_info.topLevelItem(1).text(1))
        #print(self.a)
        #print(self.b)

    def setupUi(self):
        dialog = uic.loadUi("uifiles/KalibierungWindow_neu.ui", self)
        dialog.show()


    def showCalibrationEditWindow(self):
        dialog = CalibrationEditWindow(self)
        dialog.exec_()

    #def set_fre(self):
        #self.parapass.lineEdit_1.setText(self.lineEdit_frequency.text())
        #self.parapass.lineEdit_1.setText(self.lineEdit_frequency.text())

    #def deal_parameters(self):
        #self.treeWidget_info.topLevelItem(0).setText(1, "%s" %position)
        #print(self.treeWidget_info.topLevelItem(0).text(1))
        #print("*")


    def start_CaliThread(self):
        #self.count = 0
        print(self.comboBox_polarisation.currentText())
        # remained the user to set the polarisation
        if self.comboBox_polarisation.currentText() == "Polarisation: Horizontal":
            QtWidgets.QMessageBox.information(self, "Hinweis","Die Sonde wird in Position %s eingestellt." % self.Position)
        else:
            QtWidgets.QMessageBox.information(self, "Hinweis", "Die Polarisation der Antenne is %s" % self.Polarisation)
        self.count = 0
        while self.Position < 6:

        #for self.count in range(6-self.Position):
            # remained user to put prob in right Position
            QtWidgets.QMessageBox.information(self, "Hinweis", "Bitte die Sonde in Position %s einstellen." % self.Position)
            self.cacl = External_FS_Calib(E_T=self.FieldStrength, f_min=self.StartFreq, f_step=self.FreStep, f_max=self.MaxFreq, level=self.level)
            self.cacl.start()
            print("1")
            self.count += 1
            self.Position += 1
            #self.count += 1
        if self.count == 5:
            QtWidgets.QMessageBox.information(self, "Hinweis", "Alle Prüfungen für 5 Positionen sind erledigt. \nBitte die Polarisation der Antenne ändern.")
        else:
            QtWidgets.QMessageBox.information(self, "Hinweis", "Bitte die Sonde in anderen Positonen einstellen.")



            #print(self.count)





class CalibrationEditWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CalibrationEditWindow, self).__init__(parent)
        uic.loadUi("uifiles/KalibierungEinstellen.ui", self)

        # define Signal Slots
        self.treeWidget_parameters.doubleClicked.connect(self.findParaEdit)
        #self.toolButton_new.clicked.connect(self.findParaEdit)
        self.toolButton_new.clicked.connect(self.setnewPara)
        #self.buttonBox.accepted.connect(self.passingInfo)


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

    #def passingInfo(self):
        #position = self.comboBox_Pos.currentText()
        #self.signal.emit(position)
        #print(position)




class ParametersEditWindow(QtWidgets.QDialog):
    #global position
    signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("uifiles/ParaEditWindow.ui", self)
        self.parapass = Ui_Calibration()

        #self.edit_var_parameters.accepted.connect(self.passingInfor)

    #def passingInfor(self):
        #position = self.conboBox_Pos.currentText()
        #print(position)
        #self.signal.emit(position)
        #self.parapass.lineEdit_1.setText(self.lineEdit_frequency.text())
        #print(self.parapass.lineEdit_1.text())

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



