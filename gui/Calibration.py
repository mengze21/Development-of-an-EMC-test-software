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




class Ui_Calibration(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Ui_Calibration, self).__init__(parent)
        uic.loadUi("uifiles/KalibierungWindow_neu.ui", self)
        #self.setupUi()
        #self.Position = 1
        #self.Position = int(self.treeWidget_info.topLevelItem(0).text(1))
        self.Polarisation = ""
        #self.Polarisation = str(self.treeWidget_info.topLevelItem(1).text(1))
        # the parameters can later get from setting info
        self.FieldStrength = 30
        # get start frequency from setup info
        #if "M" in str(self.treeWidget_info.topLevelItem(2).text(1)):
            #self.StartFreq = int(self.treeWidget_info.topLevelItem(2).text(1).replace("M", "")) * 1E6
        #elif "G" in str(self.treeWidget_info.topLevelItem(2).text(1)):
            #self.StartFreq = int(self.treeWidget_info.topLevelItem(2).text(1).replace("G", "")) * 1E9
        # get frequency step from setup info
        #self.FreStep = int(self.treeWidget_info.topLevelItem(3).text(1).replace("%", "")) * 0.01
        # get max.frequency from setup info
        #if "M" in str(self.treeWidget_info.topLevelItem(4).text(1)):
            #self.MaxFreq = int(self.treeWidget_info.topLevelItem(4).text(1).replace("M", "")) * 1E6
        #elif "G" in str(self.treeWidget_info.topLevelItem(4).text(1)):
            #self.MaxFreq = int(self.treeWidget_info.topLevelItem(4).text(1).replace("G", "")) * 1E9
        #self.level
        # self.paraWindow = ParametersEditWindow()

        #print("Strat Frequenz ist %s" % self.StartFreq)
        #print("Max. Frequenz ist %s" % self.MaxFreq)

        # define signal slots
        self.toolButton_testparameter.clicked.connect(self.showCalibrationEditWindow)
        self.toolButton_start.clicked.connect(self.start_CaliThread)

    #def setupUi(self):
        #dialog = uic.loadUi("uifiles/KalibierungWindow_neu.ui", self)
        #dialog.exec_()
        #dialog.show()
        # get calibration setup from file
        #f = open("./data/KalibrierungEinstellungsDaten.txt", "r")
        #alllines = f.readlines()
        #paragroup = alllines[0].strip()
        #self.paralist = paragroup.split()
        #f.close()
        #self.treeWidget_info.topLevelItem(0).setText(1, "%s" % self.paralist[5])  # Position
        #self.treeWidget_info.topLevelItem(1).setText(1, "%s" % self.paralist[6])  # Polarisation
        #self.treeWidget_info.topLevelItem(2).setText(1, "%s" % self.paralist[0])
        #self.treeWidget_info.topLevelItem(3).setText(1, "%s" % self.paralist[1])
        #self.treeWidget_info.topLevelItem(4).setText(1, "%s" % self.paralist[2])
        #self.treeWidget_info.topLevelItem(5).setText(1, "%s" % self.paralist[3])
        #self.treeWidget_info.topLevelItem(6).setText(1, "%s" % self.paralist[4])

    def showCalibrationEditWindow(self):
        dialog = CalibrationEditWindow(self)
        dialog.exec_()
        # update parameters
        self.Position = int(dialog.comboBox_Pos.currentText())
        self.Polarisation = dialog.comboBox_Polar.currentText()
        self.treeWidget_info.topLevelItem(0).setText(1, "%s" % dialog.comboBox_Pos.currentText())
        self.treeWidget_info.topLevelItem(1).setText(1, "%s" % dialog.comboBox_Polar.currentText())
        self.treeWidget_info.topLevelItem(2).setText(1, "%s" % dialog.treeWidget_parameters.topLevelItem(0).text(0))
        self.treeWidget_info.topLevelItem(3).setText(1, "%s" % dialog.treeWidget_parameters.topLevelItem(0).text(1))
        self.treeWidget_info.topLevelItem(4).setText(1, "%s" % dialog.treeWidget_parameters.topLevelItem(0).text(2))
        self.treeWidget_info.topLevelItem(5).setText(1, "%s" % dialog.treeWidget_parameters.topLevelItem(0).text(3))
        self.treeWidget_info.topLevelItem(6).setText(1, "%s" % dialog.treeWidget_parameters.topLevelItem(0).text(4))
        # get start frequency from setup info
        if "M" in str(dialog.treeWidget_parameters.topLevelItem(0).text(0)):
            self.StartFreq = int(dialog.treeWidget_parameters.topLevelItem(0).text(0).replace("M", "")) * 1E6
        elif "G" in str(dialog.treeWidget_parameters.topLevelItem(0).text(0)):
            self.StartFreq = int(dialog.treeWidget_parameters.topLevelItem(0).text(0).replace("G", "")) * 1E9
        #print("Strat Frequenz ist %s" % self.StartFreq)
        # get frequency step from setup info
        self.FreStep = int(dialog.treeWidget_parameters.topLevelItem(0).text(1).replace("%", "")) * 0.01
        # get max.frequency from setup info
        if "M" in str(dialog.treeWidget_parameters.topLevelItem(0).text(2)):
            self.MaxFreq = int(dialog.treeWidget_parameters.topLevelItem(0).text(2).replace("M", "")) * 1E6
        elif "G" in str(dialog.treeWidget_parameters.topLevelItem(0).text(2)):
            self.MaxFreq = int(dialog.treeWidget_parameters.topLevelItem(0).text(2).replace("G", "")) * 1E9
        # get calibration level
        self.level = int(dialog.treeWidget_parameters.topLevelItem(0).text(3))

        print("Strat Frequenz ist %s" % self.MaxFreq)
        print("Strat Frequenz ist %s" % self.level)



    def start_CaliThread(self):
        # self.count = 0
        if self.treeWidget_info.topLevelItem(0).text(1) == "":
            QtWidgets.QMessageBox.information(self, "Hinweis", "Bitte die Parameter einstellen")
        else:
            print(self.comboBox_polarisation.currentText())
            # remained the user to set the polarisation
            if self.comboBox_polarisation.currentText() == "Polarisation: Horizontal":
                QtWidgets.QMessageBox.information(self, "Hinweis",
                                              "Die Sonde wird in Position %s eingestellt." % self.Position)
            else:
                QtWidgets.QMessageBox.information(self, "Hinweis", "Die Polarisation der Antenne is %s" % self.Polarisation)
            self.count = 0
            # start the test for all 5 points
            while self.Position < 6:
                # for self.count in range(6-self.Position):
             # remained user to put prob in right Position
                QtWidgets.QMessageBox.information(self, "Hinweis",
                                              "Bitte die Sonde in Position %s einstellen." % self.Position)
                self.cacl = External_FS_Calib(E_T=self.FieldStrength, f_min=self.StartFreq, f_step=self.FreStep,
                                          f_max=self.MaxFreq, level=self.level)
                self.cacl.start()
                print("1")
                self.count += 1
                self.Position += 1
                # self.count += 1
            if self.count == 5:
                QtWidgets.QMessageBox.information(self, "Hinweis",
                                              "Alle Prüfungen für 5 Positionen sind erledigt. \nBitte die Polarisation der Antenne ändern.")
            else:
                QtWidgets.QMessageBox.information(self, "Hinweis", "Bitte die Sonde in anderen Positonen einstellen.")

            # print(self.count)


class CalibrationEditWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CalibrationEditWindow, self).__init__(parent)
        uic.loadUi("uifiles/KalibierungEinstellen.ui", self)

        # define Signal Slots
        self.treeWidget_parameters.doubleClicked.connect(self.findParaEdit)
        # self.toolButton_new.clicked.connect(self.findParaEdit)
        self.toolButton_new.clicked.connect(self.setnewPara)
        self.buttonBox.accepted.connect(self.SveingData)

        # read parameters
        # f = open("./data/KalibrierungEinstellungsDaten.txt", "r")
        # alllines = f.readlines()
        # f.close()
        # paragroup1 = alllines[0].strip()
        # self.paralist = paragroup1.split()
        # print(self.paralist[0])
        # print(self.paralist[1])
        # self.treeWidget_parameters.topLevelItem(0).setText(0, "%s" % self.paralist[0])

    def findParaEdit(self):
        dialog = ParametersEditWindow(self)
        dialog.exec_()
        # self.treeWidget_parameters.topLevelItem(0).setText(0, "%s" % self.paralist[0])
        self.treeWidget_parameters.topLevelItem(0).setText(0, "%s" % dialog.start_freq)
        self.treeWidget_parameters.topLevelItem(0).setText(1, "%s" % dialog.freq_step)
        self.treeWidget_parameters.topLevelItem(0).setText(2, "%s" % dialog.Max_freq)
        self.treeWidget_parameters.topLevelItem(0).setText(3, "%s" % dialog.TestLevel)
        self.treeWidget_parameters.topLevelItem(0).setText(4, "%s" % dialog.Dwell)
        # self.lineEdit_frequency.setText(" ")

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

    def SveingData(self):
        self.Position = self.comboBox_Pos.currentText()
        self.Polarisation = self.comboBox_Polar.currentText()
        # add new Position to file
        # f = open("./data/KalibrierungEinstellungsDaten.txt", "r")
        # alllines = f.readlines()
        # paragroup1 = alllines[0].strip()
        # self.paralist = paragroup1.split()
        # f.close()
        # print(len(self.paralist))
        # print(len(paragroup1))
        # print(self.Position)
        # print(paragroup1[1])

        # paragroup1 = alllines[0].strip()
        with open("./data/KalibrierungEinstellungsDaten.txt", "a") as add_positon:
            add_positon.write("%s " % self.Position)
            add_positon.write("%s " % self.Polarisation)
        add_positon.close()


class ParametersEditWindow(QtWidgets.QDialog):
    # global position
    signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("uifiles/ParaEditWindow.ui", self)
        self.parapass = Ui_Calibration()

        # f = open("./data/KalibrierungEinstellungsDaten.txt", "r")
        # alllines = f.readlines()
        # f.close()
        # paragroup1 = alllines[0].strip()
        # self.paralist = paragroup1.split()
        # print(self.paralist[0])
        # print(self.paralist[1])
        # self.lineEdit_frequency.setText("%s" % self.paralist[0])

        # define signals
        self.edit_var_parameters.accepted.connect(self.SveingData)
        # self.edit_var_parameters.accepted.connect(self.passingInfor)

    def SveingData(self):
        self.start_freq = self.lineEdit_frequency.text()
        self.freq_step = self.lineEdit_step.text()
        self.Max_freq = self.lineEdit_MaxFreq.text()
        self.TestLevel = self.lineEdit_testlevel.text()
        self.Dwell = self.lineEdit_Dwell.text()
        self.Position = ""
        self.Polarisation = ""
        f = open("./data/KalibrierungEinstellungsDaten.txt", "w")
        f.writelines(["%s " % self.start_freq, "%s " % self.freq_step, "%s " % self.Max_freq, "%s " % self.TestLevel,
                      "%s " % self.Dwell, "%s" % self.Position, "%s" % self.Polarisation])
        # f.write("\n")
        f.close()
        print(self.start_freq)

    # def passingInfor(self):
    # position = self.conboBox_Pos.currentText()
    # print(position)
    # self.signal.emit(position)
    # self.parapass.lineEdit_1.setText(self.lineEdit_frequency.text())
    # print(self.parapass.lineEdit_1.text())

    # def emit_fre(self):
    # new_fre = self.lineEdit_frequency.text()
    # self.signal.emit(new_fre)
    # self.parapass.lineEdit_1.setText(self.lineEdit_frequency.text())
    # print(self.parapass.lineEdit_1.text())
    # print(self.lineEdit_frequency.text())
    # new_frequency = self.lineEdit_frequency.text()
    # self.signal.emit(new_frequency)


##

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Calibration()
    #ui.exec_()
    sys.exit(ui.exec_())
