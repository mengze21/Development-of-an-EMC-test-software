# -*- coding: utf-8 -*-

import sys
import time
import csv
import PyQt5
from PyQt5 import uic, QtWidgets, QtChart, QtCore, QtGui
from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from openpyxl.descriptors import Default
from thread_FS_Calib import External_FS_Calib
from thread_FS_test import External_FS_test

sys.path.append('gui')


# this class is used to customized a QChartView that can realize advanced functions.
# The advanced function is: When you press the left mouse on the diagramm in order to make a selection,
# a rectangular selection box will be displayed as the mouse is dragged.
class QmyChartView(QtChart.QChartView):
    mouseMove = QtCore.pyqtSignal(QtCore.QPoint)  # signal from mouse movement

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.__beginPoint = QtCore.QPoint()  # start point of the rectangular selection box
        self.__endPoint = QtCore.QPoint()  # end point of the rectangular selection box

    # define the method of mouse presse
    def mousePressEvent(self, event):  # mouse click
        if event.button() == QtCore.Qt.LeftButton:
            self.__beginPoint = event.pos()  # record the start point
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):  # mouse movement
        point = event.pos()
        self.mouseMove.emit(point)  # emit the mouse movement signal
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):  # Mouse left frame selection to zoom in, right click to restore
        if event.button() == QtCore.Qt.LeftButton:
            self.__endPoint = event.pos()
            rectF = QtCore.QRectF()
            rectF.setTopLeft(self.__beginPoint)
            rectF.setBottomRight(self.__endPoint)
            self.chart().zoomIn(rectF)  # zoom in the seletced rectangular area
        elif event.button() == QtCore.Qt.RightButton:
            self.chart().zoomReset()  # right click to restore the zoomed area
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):  # define the key press event
        key = event.key()
        if key == QtCore.Qt.Key_Plus:
            self.chart().zoom(1.2)
        elif key == QtCore.Qt.Key_Minus:
            self.chart().zoom(0.8)
        elif key == QtCore.Qt.Key_Left:
            self.chart().scroll(10, 0)
        elif key == QtCore.Qt.Key_Right:
            self.chart().scroll(-10, 0)
        elif key == QtCore.Qt.Key_Up:
            self.chart().scroll(0, -10)
        elif key == QtCore.Qt.Key_Down:
            self.chart().scroll(0, 10)
        elif key == QtCore.Qt.Key_PageUp:
            self.chart().scroll(0, -50)
        elif key == QtCore.Qt.Key_PageDown:
            self.chart().scroll(0, 50)
        elif key == QtCore.Qt.Key_Home:
            self.chart().zoomReset()
        super().keyPressEvent(event)


# this class define the calibration main window
class Ui_Calibration(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Ui_Calibration, self).__init__(parent)
        uic.loadUi("uifiles/KalibierungWindow_neu.ui", self)

        #initial parameters
        self.FieldStrength = 0
        self.StartFreq = 0
        self.FreStep = 0
        self.MaxFreq = 0
        self.level = 0
        self.Dwell = 0
        # self.setupUi()

        # init thread_FS_test
        self.lock = QtCore.QReadWriteLock()
        self.External_FS_test = External_FS_test(self.lock, self)

        # creation of the interactive diagram
        self.chart_1 = QtChart.QChart()
        self.chart_2 = QtChart.QChart()
        # chart 1
        self.__axisFreq = QtChart.QLogValueAxis()
        self.__axisFreq.setLabelFormat("%d")  # format of the label
        self.__axisFreq.setTitleText("Frequenz / MHz \r\n ")
        self.__axisFreq.setRange(10, 10000)
        self.__axisFreq.setMinorTickCount(8)
        self.chart_1.addAxis(self.__axisFreq, QtCore.Qt.AlignBottom)
        self.__axisMag = QtChart.QValueAxis()
        self.__axisMag.setTitleText("Feldstärke / V/m  ")
        self.__axisMag.setRange(0, 40)
        self.__axisMag.setTickCount(8)
        self.__axisMag.setLabelFormat("%d")
        self.chart_1.addAxis(self.__axisMag, QtCore.Qt.AlignLeft)
        # chart 2
        self.__axisFreq_2 = QtChart.QLogValueAxis()
        self.__axisFreq_2.setLabelFormat("%d")  # format of the label
        self.__axisFreq_2.setTitleText("Frequenz / MHz \r\n ")
        self.__axisFreq_2.setRange(10, 10000)
        self.__axisFreq_2.setMinorTickCount(8)
        # self.__axisFreq.tickAn([ticks])
        self.chart_2.addAxis(self.__axisFreq_2, QtCore.Qt.AlignBottom)
        self.__axisMag_2 = QtChart.QValueAxis()
        self.__axisMag_2.setTitleText("Vorwärtsleistung / dBm ")
        self.__axisMag_2.setRange(-10, 10)
        self.__axisMag_2.setTickCount(6)
        self.__axisMag_2.setLabelFormat("%d")
        self.chart_2.addAxis(self.__axisMag_2, QtCore.Qt.AlignLeft)

        # create graphics
        self.graphicsView = QmyChartView(self.frame_5)
        # self.graphicsView.setGeometry(QtCore.QRect(0, 0, 300, 400))
        # self.graphicsView.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addWidget(self.graphicsView)
        # self.verticalLayout.addWidget(self.frame)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView.setCursor(QtCore.Qt.ArrowCursor)
        self.graphicsView.mouseMove.connect(self.do_chartView_mouseMove)
        self.graphicsView.setChart(self.chart_1)
        self.graphicsView.setObjectName("graphicsView")

        self.graphicsView_2 = QmyChartView(self.frame_5)
        # self.graphicsView_2.setGeometry(QtCore.QRect(300, 0, 300, 400))
        self.horizontalLayout.addWidget(self.graphicsView_2)
        self.graphicsView_2.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView_2.setCursor(QtCore.Qt.ArrowCursor)
        self.graphicsView_2.mouseMove.connect(self.do_chartView_mouseMove)
        self.graphicsView_2.setChart(self.chart_2)
        self.graphicsView_2.setObjectName("graphicsView_2")

        # create curve for forward power at position 1
        self.curveFPower1 = QtChart.QLineSeries()
        self.curveFPower1.setName("Test Position 1")
        self.chart_2.addSeries(self.curveFPower1)
        self.curveFPower1.attachAxis(self.__axisFreq_2)
        self.curveFPower1.attachAxis(self.__axisMag_2)
        self.chart_2.legend().markers(self.curveFPower1)[0].setVisible(True)
        self.chart_2.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        pen.setWidth(1)
        self.curveFPower1.setPen(pen)
        self.curveFPower1.setPointsVisible(True)
        # self.curveProb.hovered.connect(self.do_series_hovered)
        # self.curveProb.clicked.connect(self.do_series_clicked)

        # create curve for field strength at position 1
        self.curveFieldStr_1 = QtChart.QLineSeries()
        self.curveFieldStr_1.setName("Test Position 1")
        self.chart_1.addSeries(self.curveFieldStr_1)
        self.curveFieldStr_1.attachAxis(self.__axisFreq)
        self.curveFieldStr_1.attachAxis(self.__axisMag)
        self.chart_1.legend().markers(self.curveFieldStr_1)[0].setVisible(True)
        self.chart_1.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        pen.setWidth(1)
        self.curveFieldStr_1.setPen(pen)
        self.curveFieldStr_1.setPointsVisible(True)

        # open and read measurement data
        self.measuredFreq = []  # init parameters
        self.forwardPower = []  # init parameters
        self.probData = []      # init parameters
        with open("./output.csv", "r") as FSCaliData:
            reader = csv.reader(FSCaliData)
            rows = []
            for row in reader:
                rows.append(row)
            print(rows)
        for i in range(len(rows)):
            self.measuredFreq.append(float(rows[i][0]))    # column 0 is frequency
            self.forwardPower.append(float(rows[i][1]))    # column 1 is forward power
            self.probData.append(float(rows[i][2]))        # column 2 is measurement data from prob
        #print(self.measuredFreq)
        #print(self.forwardPower)
        #print(self.probData)

        # adding data to chart1
        for a, b in zip(self.measuredFreq, self.forwardPower):
            self.curveFPower1.append(a, b)
        # adding data to chart1
        for a, b in zip(self.measuredFreq, self.probData):
            self.curveFieldStr_1.append(a, b)

        #while self.External_FS_test.completedflag == 1:
           #self.label_TestRunningStatus.setText("Test beendet!")

        # define signal slots
        self.toolButton_testparameter.clicked.connect(self.showCalibrationEditWindow)
        self.toolButton_start.clicked.connect(self.start_test)  # signal connect to test function later rewrite!!
        self.toolButton_pause.clicked.connect(self.pause_test)  # signal connect to test function later rewrite!!
        self.toolButton_stop.clicked.connect(self.stop_test)    # signal connect to test function later rewrite!!
        self.pushButton_colorChange_1.clicked.connect(self.changecolorP1)
        self.pushButton_colorChange_2.clicked.connect(self.changecolorP2)

    def changecolorP1(self):
        color = QtWidgets.QColorDialog.getColor()
        pen = QtGui.QPen(QtGui.QColor(color))
        self.curveFieldStr_1.setPen(pen)
        self.curveFPower1.setPen(pen)

    def changecolorP2(self):
        color = QtWidgets.QColorDialog.getColor()
        pen = QtGui.QPen(QtGui.QColor(color))
        #self.curveFieldStr_1.setPen(pen)
        #self.curveFPower1.setPen(pen)


    def do_chartView_mouseMove(self, point):
        pt = self.graphicsView_2.chart().mapToValue(point)
        self.MousPositionLabel.setText("Chart X=%.2f,Y=%.2f" % (pt.x(), pt.y()))

        self.Polarisation = ""
        self.FieldStrength = 30

    # def setupUi(self):
    # dialog = uic.loadUi("uifiles/KalibierungWindow_neu.ui", self)
    # dialog.exec_()
    # dialog.show()
    # get calibration setup from file
    # f = open("./data/KalibrierungEinstellungsDaten.txt", "r")
    # alllines = f.readlines()
    # paragroup = alllines[0].strip()
    # self.paralist = paragroup.split()
    # f.close()
    # self.treeWidget_info.topLevelItem(0).setText(1, "%s" % self.paralist[5])  # Position
    # self.treeWidget_info.topLevelItem(1).setText(1, "%s" % self.paralist[6])  # Polarisation
    # self.treeWidget_info.topLevelItem(2).setText(1, "%s" % self.paralist[0])
    # self.treeWidget_info.topLevelItem(3).setText(1, "%s" % self.paralist[1])
    # self.treeWidget_info.topLevelItem(4).setText(1, "%s" % self.paralist[2])
    # self.treeWidget_info.topLevelItem(5).setText(1, "%s" % self.paralist[3])
    # self.treeWidget_info.topLevelItem(6).setText(1, "%s" % self.paralist[4])

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
            self.StartFreq = float(dialog.treeWidget_parameters.topLevelItem(0).text(0).replace("M", ""))
        elif "G" in str(dialog.treeWidget_parameters.topLevelItem(0).text(0)):
            self.StartFreq = float(dialog.treeWidget_parameters.topLevelItem(0).text(0).replace("G", "")) * 1E3

        # get frequency step from setup info
        if "%" in str(dialog.treeWidget_parameters.topLevelItem(0).text(1)):
            self.FreStep = float(dialog.treeWidget_parameters.topLevelItem(0).text(1).replace("%", "")) * 0.01
        else:
            self.FreStep = dialog.treeWidget_parameters.topLevelItem(0).text(1)

        # get max.frequency from setup info
        if "M" in str(dialog.treeWidget_parameters.topLevelItem(0).text(2)):
            self.MaxFreq = float(dialog.treeWidget_parameters.topLevelItem(0).text(2).replace("M", ""))
        elif "G" in str(dialog.treeWidget_parameters.topLevelItem(0).text(2)):
            self.MaxFreq = float(dialog.treeWidget_parameters.topLevelItem(0).text(2).replace("G", "")) * 1E3

        # get calibration level
        self.level = int(dialog.treeWidget_parameters.topLevelItem(0).text(3))

        # get Dwell
        self.Dwell = int(dialog.treeWidget_parameters.topLevelItem(0).text(4))

        print("Strat Frequenz ist %s" % self.MaxFreq)
        print("Strat Frequenz ist %s" % self.level)


    # test function delete later
    def start_test(self):
        self.External_FS_test.start()
        self.label_TestRunningStatus.setText("Test läuft")
        self.label_status.setText("Status: %s (%s)" % (
        self.label_TestRunningStatus.text(), time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())))
        #while self.External_FS_test.completedflag:
            #self.label_TestRunningStatus.setText("Test beendet!")
    # test function delete later
    def pause_test(self):
        if not self.External_FS_test.ispaused:
            self.External_FS_test.pause()
            self.label_TestRunningStatus.setText("Test pausiert")
        else:
            self.External_FS_test.resum()
            self.label_TestRunningStatus.setText("Test läuft wieder")
    # test function delete later
    def stop_test(self):
        if self.External_FS_test.isRunning():
            self.External_FS_test.stop()
            time.sleep(1)
            self.label_TestRunningStatus.setText("Test wird gestoppt")
        self.label_status.setText("Status: %s (%s)" % (
            self.label_TestRunningStatus.text(), time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())))

    def start_CaliThread(self):
        # self.count = 0
        if self.treeWidget_info.topLevelItem(0).text(1) == "" or \
                self.treeWidget_info.topLevelItem(1).text(1) == "" or \
                self.treeWidget_info.topLevelItem(2).text(1) == "" or \
                self.treeWidget_info.topLevelItem(3).text(1) == "" or \
                self.treeWidget_info.topLevelItem(4).text(1) == "" or \
                self.treeWidget_info.topLevelItem(5).text(1) == "":
            QtWidgets.QMessageBox.information(self, "Hinweis", "Bitte alle Parameter einstellen")
        else:
            print(self.comboBox_polarisation.currentText())
            # remained the user to set the polarisation
            if self.comboBox_polarisation.currentText() == "Polarisation: Horizontal":
                QtWidgets.QMessageBox.information(self, "Hinweis",
                                                  "Die Sonde wird in Position %s eingestellt." % self.Position)
            else:
                QtWidgets.QMessageBox.information(self, "Hinweis",
                                                  "Die Polarisation der Antenne is %s" % self.Polarisation)
            # self.count = 0
            # start the test for all 5 points
            # while self.Position < 6:
            # for self.count in range(6-self.Position):
            # remained user to put prob in right Position
            # QtWidgets.QMessageBox.information(self, "Hinweis",
            # "Bitte die Sonde in Position %s einstellen." % self.Position)

            self.calc = External_FS_Calib(E_T=self.FieldStrength, f_min=self.StartFreq, f_step=self.FreStep,
                                          f_max=self.MaxFreq, level=self.level)
            self.calc.start()
            self.calc.signal = 1
            self.calc.countChanged.connect(self.onCountChanged)

            # self.count += 1
            # self.Position += 1
            # self.count += 1
            # if self.count == 5:
            # QtWidgets.QMessageBox.information(self, "Hinweis",
            # "Alle Prüfungen für 5 Positionen sind erledigt. \nBitte die Polarisation der Antenne ändern.")
            # else:
            # QtWidgets.QMessageBox.information(self, "Hinweis", "Bitte die Sonde in anderen Positonen einstellen.")

            # print(self.count)

    def cali_test_pause(self):
        pass


        #self.calc.signal += 1
        #print(self.calc.signal)
        #if (self.calc.signal & 1) == 0:
            #self.toolButton_pause.setAutoRaise(False)
            # time.sleep(1)
            #self.lineEdit_TestStatus.setText("Test unterbrochen! ")
        #elif (self.calc.signal & 1) == 1:

            #self.lineEdit_TestStatus.setText("Test läuft!")

            # self.calc = External_FS_Calib(E_T=self.FieldStrength, f_min=self.StartFreq, f_step=self.FreStep,
            # f_max=self.MaxFreq, level=self.level)
            # self.calc.start()
            # self.calc.signal = 1
            # self.calc.countChanged.connect(self.onCountChanged)

    def cali_test_stop(self):
        self.calc.quit()
        time.sleep(2)
        self.lineEdit_TestStatus.setText("Test ist stop!")

    # used to update the diagram
    def onCountChanged(self, value, num, spannung):  # the parameters rewrite later
        frequenz = value
        magnitude = num
        Sollspannung = spannung
        self.series_1.append(frequenz, magnitude)
        self.normline3.append(frequenz, Sollspannung)


# this class define the window of calibration settings
class CalibrationEditWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CalibrationEditWindow, self).__init__(parent)
        uic.loadUi("uifiles/KalibierungEinstellen.ui", self)

        # define Signal Slots
        self.treeWidget_parameters.doubleClicked.connect(self.findParaEdit)
        # self.toolButton_new.clicked.connect(self.findParaEdit)
        self.toolButton_new.clicked.connect(self.setnewPara)
        self.buttonBox.accepted.connect(self.SveingData)

    def findParaEdit(self):
        dialog = ParametersEditWindow(self)
        dialog.exec_()
        # self.treeWidget_parameters.topLevelItem(0).setText(0, "%s" % self.paralist[0])
        # updating parameters from file
        f = open("./data/KalibrierungEinstellungsDaten.txt", "r")
        alllines = f.readlines()
        paragroup1 = alllines[0].strip()
        self.paralist = paragroup1.split()
        f.close()
        #self.treeWidget_parameters.topLevelItem(0).setText(0, "%s" % self.paralist[0])
        #self.treeWidget_parameters.topLevelItem(0).setText(1, "%s" % self.paralist[1])
        #self.treeWidget_parameters.topLevelItem(0).setText(2, "%s" % self.paralist[2])
        #self.treeWidget_parameters.topLevelItem(0).setText(3, "%s" % self.paralist[3])
        #self.treeWidget_parameters.topLevelItem(0).setText(4, "%s" % self.paralist[4])
        self.treeWidget_parameters.topLevelItem(0).setText(0, "%s" % dialog.start_freq)
        self.treeWidget_parameters.topLevelItem(0).setText(1, "%s" % dialog.freq_step)
        self.treeWidget_parameters.topLevelItem(0).setText(2, "%s" % dialog.Max_freq)
        self.treeWidget_parameters.topLevelItem(0).setText(3, "%s" % dialog.TestLevel)
        self.treeWidget_parameters.topLevelItem(0).setText(4, "%s" % dialog.Dwell)

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

        with open("./data/KalibrierungEinstellungsDaten.txt", "a") as add_positon:
            add_positon.write("%s " % self.Position)
            add_positon.write("%s " % self.Polarisation)
        add_positon.close()


# this class define the window of parameters settings
class ParametersEditWindow(QtWidgets.QDialog):
    # signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("uifiles/ParaEditWindow.ui", self)

        # define signals
        self.edit_var_parameters.accepted.connect(self.SveingData)

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Calibration()
    # ui.exec_()
    sys.exit(ui.exec_())
