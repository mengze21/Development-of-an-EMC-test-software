# -*- coding: utf-8 -*-
import os
import sys
import time
import csv
import numpy as np
import pandas as pd
import PyQt5

from PyQt5 import uic, QtWidgets, QtChart, QtCore, QtGui

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import *
from openpyxl.descriptors import Default

import CaliDataProcessing
#from thread_FS_Calib import External_FS_Calib
#from thread_FS_Meas import External_FS
from thread_FS_test import External_FS_test
from CaliDataProcessing import caliDataProcessing

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
        self.setWindowIcon(QIcon("./icon_materials/8.png"))

        #initial parameters
        self.FieldStrength = 0
        self.StartFreq = 0
        self.FreStep = 0
        self.MaxFreq = 0
        self.level = 0
        self.Dwell = 0
        self.vorPower = []
        self.measuredFreq = []
        self.measuredFieldStrength = []
        self.freqList = []
        self.vorPowList = []
        self.feilStrList = []
        #self.testresult = [[]]
        # self.setupUi()
        # deactivate pause and stop button
        self.toolButton_stop.setEnabled(False)
        self.toolButton_pause.setEnabled(False)


        # creation of the interactive diagram
        self.chart_1 = QtChart.QChart()
        self.chart_2 = QtChart.QChart()
        self.chart_3 = QtChart.QChart()
        # chart 1   Field Strength
        self.__axisFreq = QtChart.QLogValueAxis()
        self.__axisFreq.setLabelFormat("%d")  # format of the label
        self.__axisFreq.setTitleText("Frequenz / MHz \r\n ")
        self.__axisFreq.setRange(10, 10000)
        self.__axisFreq.setMinorTickCount(8)
        self.chart_1.addAxis(self.__axisFreq, QtCore.Qt.AlignBottom)
        self.__axisMag = QtChart.QValueAxis()
        self.__axisMag.setTitleText("Feldstärke / V/m  ")
        self.__axisMag.setRange(0, 30)
        self.__axisMag.setTickCount(6)
        self.__axisMag.setMinorTickCount(2)
        self.__axisMag.setLabelFormat("%.1f")
        self.chart_1.addAxis(self.__axisMag, QtCore.Qt.AlignLeft)
        # chart 2  forward power
        self.__axisFreq_2 = QtChart.QLogValueAxis()
        self.__axisFreq_2.setLabelFormat("%d")  # format of the label
        self.__axisFreq_2.setTitleText("Frequenz / MHz \r\n ")
        self.__axisFreq_2.setRange(10, 10000)
        self.__axisFreq_2.setMinorTickCount(8)
        # self.__axisFreq.tickAn([ticks])
        self.chart_2.addAxis(self.__axisFreq_2, QtCore.Qt.AlignBottom)
        self.__axisMag_2 = QtChart.QValueAxis()
        self.__axisMag_2.setTitleText("Vorwärtsleistung / dBm ")
        self.__axisMag_2.setRange(-40, 10)
        self.__axisMag_2.setTickCount(6)
        self.__axisMag_2.setMinorTickCount(2)
        self.__axisMag_2.setLabelFormat("%.1f")
        #self.__axisMag_2.setTickInterval(10)
        #self.__axisMag_2.setTickAnchor(5)
        #self.__axisMag_2.TickType(1)
        self.chart_2.addAxis(self.__axisMag_2, QtCore.Qt.AlignLeft)
        # chart 3   backward power
        self.__axisFreq_3 = QtChart.QLogValueAxis()
        self.__axisFreq_3.setLabelFormat("%d")  # format of the label
        self.__axisFreq_3.setTitleText("Frequenz / MHz \r\n ")
        self.__axisFreq_3.setRange(10, 10000)
        self.__axisFreq_3.setMinorTickCount(8)
        # self.__axisFreq.tickAn([ticks])
        self.chart_3.addAxis(self.__axisFreq_3, QtCore.Qt.AlignBottom)
        self.__axisMag_3 = QtChart.QValueAxis()
        self.__axisMag_3.setTitleText("Rückwärtsleistung / dBm ")
        self.__axisMag_3.setRange(-40, 10)
        self.__axisMag_3.setTickCount(6)
        self.__axisMag_3.setMinorTickCount(2)
        self.__axisMag_3.setLabelFormat("%.1f")
        self.chart_3.addAxis(self.__axisMag_3, QtCore.Qt.AlignLeft)

        # create graphics
        self.graphicsView = QmyChartView(self.frame_5)
        #self.graphicsView.setGeometry(QtCore.QRect(10, 0, 400, 400))
        #self.graphicsView.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addWidget(self.graphicsView)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView.setCursor(QtCore.Qt.ArrowCursor)
        self.graphicsView.mouseMove.connect(self.do_chartView_mouseMove)
        self.graphicsView.setChart(self.chart_1)
        self.graphicsView.setObjectName("graphicsView")

        self.graphicsView_2 = QmyChartView(self.frame_5)
        #self.graphicsView_2.setGeometry(QtCore.QRect(300, 0, 400, 400))
        self.horizontalLayout.addWidget(self.graphicsView_2)
        self.graphicsView_2.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView_2.setCursor(QtCore.Qt.ArrowCursor)
        self.graphicsView_2.mouseMove.connect(self.do_chartView_mouseMove)
        self.graphicsView_2.setChart(self.chart_2)
        #self.graphicsView_2.setChart(self.chart_3)
        self.graphicsView_2.setObjectName("graphicsView_2")

        # create curve for forward power
        # at position 1
        self.curveFPower1 = QtChart.QLineSeries()
        self.curveFPower1.setName("P1")
        self.chart_2.addSeries(self.curveFPower1)
        self.curveFPower1.attachAxis(self.__axisFreq_2)
        self.curveFPower1.attachAxis(self.__axisMag_2)
        self.chart_2.legend().markers(self.curveFPower1)[0].setVisible(True)
        self.chart_2.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
        pen.setWidth(1)
        self.curveFPower1.setPen(pen)
        self.curveFPower1.setPointsVisible(True)
        self.curveFPower1.hovered.connect(self.do_series_hovered)
        self.curveFPower1.clicked.connect(self.do_series_clicked)
        # at position 2
        self.curveFPower2 = QtChart.QLineSeries()
        self.curveFPower2.setName("P2")
        self.chart_2.addSeries(self.curveFPower2)
        self.curveFPower2.attachAxis(self.__axisFreq_2)
        self.curveFPower2.attachAxis(self.__axisMag_2)
        self.chart_2.legend().markers(self.curveFPower2)[0].setVisible(False)
        self.chart_2.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 255))
        pen.setWidth(1)
        self.curveFPower2.setPen(pen)
        self.curveFPower2.setPointsVisible(True)
        self.curveFPower2.hovered.connect(self.do_series_hovered)
        self.curveFPower2.clicked.connect(self.do_series_clicked)
        # at position 3
        self.curveFPower3 = QtChart.QLineSeries()
        self.curveFPower3.setName("P3")
        self.chart_2.addSeries(self.curveFPower3)
        self.curveFPower3.attachAxis(self.__axisFreq_2)
        self.curveFPower3.attachAxis(self.__axisMag_2)
        self.chart_2.legend().markers(self.curveFPower3)[0].setVisible(False)
        self.chart_2.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 255))
        pen.setWidth(1)
        self.curveFPower3.setPen(pen)
        self.curveFPower3.setPointsVisible(True)
        self.curveFPower3.hovered.connect(self.do_series_hovered)
        self.curveFPower3.clicked.connect(self.do_series_clicked)
        # at position 4
        self.curveFPower4 = QtChart.QLineSeries()
        self.curveFPower4.setName("P4")
        self.chart_2.addSeries(self.curveFPower4)
        self.curveFPower4.attachAxis(self.__axisFreq_2)
        self.curveFPower4.attachAxis(self.__axisMag_2)
        self.chart_2.legend().markers(self.curveFPower4)[0].setVisible(False)
        self.chart_2.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(0, 255, 255))
        pen.setWidth(1)
        self.curveFPower4.setPen(pen)
        self.curveFPower4.setPointsVisible(True)
        self.curveFPower4.hovered.connect(self.do_series_hovered)
        self.curveFPower4.clicked.connect(self.do_series_clicked)
        # at position 5
        self.curveFPower5 = QtChart.QLineSeries()
        self.curveFPower5.setName("P5")
        self.chart_2.addSeries(self.curveFPower5)
        self.curveFPower5.attachAxis(self.__axisFreq_2)
        self.curveFPower5.attachAxis(self.__axisMag_2)
        self.chart_2.legend().markers(self.curveFPower5)[0].setVisible(False)
        self.chart_2.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(255, 255, 0))
        pen.setWidth(1)
        self.curveFPower5.setPen(pen)
        self.curveFPower5.setPointsVisible(True)
        self.curveFPower5.hovered.connect(self.do_series_hovered)
        self.curveFPower5.clicked.connect(self.do_series_clicked)
        # real time curve
        self.curveFPower_real = QtChart.QLineSeries()
        self.curveFPower_real.setName("P1")
        self.chart_2.addSeries(self.curveFPower_real)
        self.curveFPower_real.attachAxis(self.__axisFreq_2)
        self.curveFPower_real.attachAxis(self.__axisMag_2)
        self.chart_2.legend().markers(self.curveFPower_real)[0].setVisible(False)
        self.chart_2.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))   # red
        pen.setWidth(1)
        self.curveFPower_real.setPen(pen)
        self.curveFPower_real.setPointsVisible(True)
        self.curveFPower_real.hovered.connect(self.do_series_hovered)
        self.curveFPower_real.clicked.connect(self.do_series_clicked)
        # real time curve 2
        self.curveFPower_real2 = QtChart.QLineSeries()
        self.curveFPower_real2.setName("P2")
        self.chart_2.addSeries(self.curveFPower_real2)
        self.curveFPower_real2.attachAxis(self.__axisFreq_2)
        self.curveFPower_real2.attachAxis(self.__axisMag_2)
        self.chart_2.legend().markers(self.curveFPower_real2)[0].setVisible(False)
        self.chart_2.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 255))   # blue
        pen.setWidth(1)
        self.curveFPower_real2.setPen(pen)
        self.curveFPower_real2.setPointsVisible(True)
        self.curveFPower_real2.hovered.connect(self.do_series_hovered)
        self.curveFPower_real2.clicked.connect(self.do_series_clicked)
        # real time curve 3
        self.curveFPower_real3 = QtChart.QLineSeries()
        self.curveFPower_real3.setName("P3")
        self.chart_2.addSeries(self.curveFPower_real3)
        self.curveFPower_real3.attachAxis(self.__axisFreq_2)
        self.curveFPower_real3.attachAxis(self.__axisMag_2)
        self.chart_2.legend().markers(self.curveFPower_real3)[0].setVisible(False)
        self.chart_2.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 255))     # fuchsia
        pen.setWidth(1)
        self.curveFPower_real3.setPen(pen)
        self.curveFPower_real3.setPointsVisible(True)
        self.curveFPower_real3.hovered.connect(self.do_series_hovered)
        self.curveFPower_real3.clicked.connect(self.do_series_clicked)
        # real time curve 4
        self.curveFPower_real4 = QtChart.QLineSeries()
        self.curveFPower_real4.setName("P5")
        self.chart_2.addSeries(self.curveFPower_real4)
        self.curveFPower_real4.attachAxis(self.__axisFreq_2)
        self.curveFPower_real4.attachAxis(self.__axisMag_2)
        self.chart_2.legend().markers(self.curveFPower_real4)[0].setVisible(False)
        self.chart_2.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(0, 128, 0))       # green
        pen.setWidth(1)
        self.curveFPower_real4.setPen(pen)
        self.curveFPower_real4.setPointsVisible(True)
        self.curveFPower_real4.hovered.connect(self.do_series_hovered)
        self.curveFPower_real4.clicked.connect(self.do_series_clicked)
        # real time curve 5
        self.curveFPower_real5 = QtChart.QLineSeries()
        self.curveFPower_real5.setName("P5")
        self.chart_2.addSeries(self.curveFPower_real5)
        self.curveFPower_real5.attachAxis(self.__axisFreq_2)
        self.curveFPower_real5.attachAxis(self.__axisMag_2)
        self.chart_2.legend().markers(self.curveFPower_real5)[0].setVisible(False)
        self.chart_2.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(128, 0, 128))     # purple
        pen.setWidth(1)
        self.curveFPower_real5.setPen(pen)
        self.curveFPower_real5.setPointsVisible(True)
        self.curveFPower_real5.hovered.connect(self.do_series_hovered)
        self.curveFPower_real5.clicked.connect(self.do_series_clicked)

        # create curve for field strength
        # at position 1
        self.curveFieldStr_1 = QtChart.QLineSeries()
        self.curveFieldStr_1.setName("P1")
        self.chart_1.addSeries(self.curveFieldStr_1)
        self.curveFieldStr_1.attachAxis(self.__axisFreq)
        self.curveFieldStr_1.attachAxis(self.__axisMag)
        self.chart_1.legend().markers(self.curveFieldStr_1)[0].setVisible(False)
        self.chart_1.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
        pen.setWidth(1)
        self.curveFieldStr_1.setPen(pen)
        self.curveFieldStr_1.setPointsVisible(True)
        self.curveFieldStr_1.hovered.connect(self.do_series_hovered)
        self.curveFieldStr_1.clicked.connect(self.do_series_clicked)
        # at position 2
        self.curveFieldStr_2 = QtChart.QLineSeries()
        self.curveFieldStr_2.setName("P2")
        self.chart_1.addSeries(self.curveFieldStr_2)
        self.curveFieldStr_2.attachAxis(self.__axisFreq)
        self.curveFieldStr_2.attachAxis(self.__axisMag)
        self.chart_1.legend().markers(self.curveFieldStr_2)[0].setVisible(False)
        self.chart_1.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 255))
        pen.setWidth(1)
        self.curveFieldStr_2.setPen(pen)
        self.curveFieldStr_2.setPointsVisible(True)
        self.curveFieldStr_2.hovered.connect(self.do_series_hovered)
        self.curveFieldStr_2.clicked.connect(self.do_series_clicked)
        # at position 3
        self.curveFieldStr_3 = QtChart.QLineSeries()
        self.curveFieldStr_3.setName("P3")
        self.chart_1.addSeries(self.curveFieldStr_3)
        self.curveFieldStr_3.attachAxis(self.__axisFreq)
        self.curveFieldStr_3.attachAxis(self.__axisMag)
        self.chart_1.legend().markers(self.curveFieldStr_3)[0].setVisible(False)
        self.chart_1.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 255))
        pen.setWidth(1)
        self.curveFieldStr_3.setPen(pen)
        self.curveFieldStr_3.setPointsVisible(True)
        self.curveFieldStr_3.hovered.connect(self.do_series_hovered)
        self.curveFieldStr_3.clicked.connect(self.do_series_clicked)
        # at position 4
        self.curveFieldStr_4 = QtChart.QLineSeries()
        self.curveFieldStr_4.setName("P4")
        self.chart_1.addSeries(self.curveFieldStr_4)
        self.curveFieldStr_4.attachAxis(self.__axisFreq)
        self.curveFieldStr_4.attachAxis(self.__axisMag)
        self.chart_1.legend().markers(self.curveFieldStr_4)[0].setVisible(False)
        self.chart_1.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(0, 255, 255))
        pen.setWidth(1)
        self.curveFieldStr_4.setPen(pen)
        self.curveFieldStr_4.setPointsVisible(True)
        self.curveFieldStr_4.hovered.connect(self.do_series_hovered)
        self.curveFieldStr_4.clicked.connect(self.do_series_clicked)
        # at position 5
        self.curveFieldStr_5 = QtChart.QLineSeries()
        self.curveFieldStr_5.setName("P5")
        self.chart_1.addSeries(self.curveFieldStr_5)
        self.curveFieldStr_5.attachAxis(self.__axisFreq)
        self.curveFieldStr_5.attachAxis(self.__axisMag)
        self.chart_1.legend().markers(self.curveFieldStr_5)[0].setVisible(False)
        self.chart_1.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(255, 255, 0))
        pen.setWidth(1)
        self.curveFieldStr_5.setPen(pen)
        self.curveFieldStr_5.setPointsVisible(True)
        self.curveFieldStr_5.hovered.connect(self.do_series_hovered)
        self.curveFieldStr_5.clicked.connect(self.do_series_clicked)
        # real time curve
        self.curveFieldStr_real = QtChart.QLineSeries()
        self.curveFieldStr_real.setName("P1")
        self.chart_1.addSeries(self.curveFieldStr_real)
        self.curveFieldStr_real.attachAxis(self.__axisFreq)
        self.curveFieldStr_real.attachAxis(self.__axisMag)
        self.chart_1.legend().markers(self.curveFieldStr_real)[0].setVisible(False)
        self.chart_1.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))       # red
        pen.setWidth(1)
        self.curveFieldStr_real.setPen(pen)
        self.curveFieldStr_real.setPointsVisible(True)
        self.curveFieldStr_real.hovered.connect(self.do_series_hovered)
        self.curveFieldStr_real.clicked.connect(self.do_series_clicked)
        # real time curve 2
        self.curveFieldStr_real2 = QtChart.QLineSeries()
        self.curveFieldStr_real2.setName("P2")
        self.chart_1.addSeries(self.curveFieldStr_real2)
        self.curveFieldStr_real2.attachAxis(self.__axisFreq)
        self.curveFieldStr_real2.attachAxis(self.__axisMag)
        self.chart_1.legend().markers(self.curveFieldStr_real2)[0].setVisible(False)
        self.chart_1.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 255))       # blue
        pen.setWidth(1)
        self.curveFieldStr_real2.setPen(pen)
        self.curveFieldStr_real2.setPointsVisible(True)
        self.curveFieldStr_real2.hovered.connect(self.do_series_hovered)
        self.curveFieldStr_real2.clicked.connect(self.do_series_clicked)
        # real time curve 3
        self.curveFieldStr_real3 = QtChart.QLineSeries()
        self.curveFieldStr_real3.setName("P3")
        self.chart_1.addSeries(self.curveFieldStr_real3)
        self.curveFieldStr_real3.attachAxis(self.__axisFreq)
        self.curveFieldStr_real3.attachAxis(self.__axisMag)
        self.chart_1.legend().markers(self.curveFieldStr_real3)[0].setVisible(False)
        self.chart_1.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 255))     # fuchsia
        pen.setWidth(1)
        self.curveFieldStr_real3.setPen(pen)
        self.curveFieldStr_real3.setPointsVisible(True)
        self.curveFieldStr_real3.hovered.connect(self.do_series_hovered)
        self.curveFieldStr_real3.clicked.connect(self.do_series_clicked)
        # real time curve 4
        self.curveFieldStr_real4 = QtChart.QLineSeries()
        self.curveFieldStr_real4.setName("P4")
        self.chart_1.addSeries(self.curveFieldStr_real4)
        self.curveFieldStr_real4.attachAxis(self.__axisFreq)
        self.curveFieldStr_real4.attachAxis(self.__axisMag)
        self.chart_1.legend().markers(self.curveFieldStr_real4)[0].setVisible(False)
        self.chart_1.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(0, 128, 0))       # green
        pen.setWidth(1)
        self.curveFieldStr_real4.setPen(pen)
        self.curveFieldStr_real4.setPointsVisible(True)
        self.curveFieldStr_real4.hovered.connect(self.do_series_hovered)
        self.curveFieldStr_real4.clicked.connect(self.do_series_clicked)
        # real time curve 5
        self.curveFieldStr_real5 = QtChart.QLineSeries()
        self.curveFieldStr_real5.setName("P5")
        self.chart_1.addSeries(self.curveFieldStr_real5)
        self.curveFieldStr_real5.attachAxis(self.__axisFreq)
        self.curveFieldStr_real5.attachAxis(self.__axisMag)
        self.chart_1.legend().markers(self.curveFieldStr_real5)[0].setVisible(False)
        self.chart_1.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(128, 0, 128))     # purple
        pen.setWidth(1)
        self.curveFieldStr_real5.setPen(pen)
        self.curveFieldStr_real5.setPointsVisible(True)
        self.curveFieldStr_real5.hovered.connect(self.do_series_hovered)
        self.curveFieldStr_real5.clicked.connect(self.do_series_clicked)

        # crate curve for chart3
        # crate curve for backward power
        # real time curve 1
        self.curveRwdPow_real = QtChart.QLineSeries()
        self.curveRwdPow_real.setName("P1")
        self.chart_3.addSeries(self.curveRwdPow_real)
        self.curveRwdPow_real.attachAxis(self.__axisFreq_3)
        self.curveRwdPow_real.attachAxis(self.__axisMag_3)
        self.chart_3.legend().markers(self.curveRwdPow_real)[0].setVisible(False)
        self.chart_3.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))       #red
        pen.setWidth(1)
        self.curveRwdPow_real.setPen(pen)
        self.curveRwdPow_real.setPointsVisible(True)
        self.curveRwdPow_real.hovered.connect(self.do_series_hovered)
        self.curveRwdPow_real.clicked.connect(self.do_series_clicked)
        # real time curve 2
        self.curveRwdPow_real2 = QtChart.QLineSeries()
        self.curveRwdPow_real2.setName("P2")
        self.chart_3.addSeries(self.curveRwdPow_real2)
        self.curveRwdPow_real2.attachAxis(self.__axisFreq_3)
        self.curveRwdPow_real2.attachAxis(self.__axisMag_3)
        self.chart_3.legend().markers(self.curveRwdPow_real2)[0].setVisible(False)
        self.chart_3.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 255))       # blue
        pen.setWidth(1)
        self.curveRwdPow_real2.setPen(pen)
        self.curveRwdPow_real2.setPointsVisible(True)
        self.curveRwdPow_real2.hovered.connect(self.do_series_hovered)
        self.curveRwdPow_real2.clicked.connect(self.do_series_clicked)
        # real time curve 3
        self.curveRwdPow_real3 = QtChart.QLineSeries()
        self.curveRwdPow_real3.setName("P2")
        self.chart_3.addSeries(self.curveRwdPow_real3)
        self.curveRwdPow_real3.attachAxis(self.__axisFreq_3)
        self.curveRwdPow_real3.attachAxis(self.__axisMag_3)
        self.chart_3.legend().markers(self.curveRwdPow_real3)[0].setVisible(False)
        self.chart_3.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 255))     # fuchsia
        pen.setWidth(1)
        self.curveRwdPow_real3.setPen(pen)
        self.curveRwdPow_real3.setPointsVisible(True)
        self.curveRwdPow_real3.hovered.connect(self.do_series_hovered)
        self.curveRwdPow_real3.clicked.connect(self.do_series_clicked)
        # real time curve 4
        self.curveRwdPow_real4 = QtChart.QLineSeries()
        self.curveRwdPow_real4.setName("P2")
        self.chart_3.addSeries(self.curveRwdPow_real4)
        self.curveRwdPow_real4.attachAxis(self.__axisFreq_3)
        self.curveRwdPow_real4.attachAxis(self.__axisMag_3)
        self.chart_3.legend().markers(self.curveRwdPow_real4)[0].setVisible(False)
        self.chart_3.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(0, 128, 0))       # green
        pen.setWidth(1)
        self.curveRwdPow_real4.setPen(pen)
        self.curveRwdPow_real4.setPointsVisible(True)
        self.curveRwdPow_real4.hovered.connect(self.do_series_hovered)
        self.curveRwdPow_real4.clicked.connect(self.do_series_clicked)
        # real time curve 5
        self.curveRwdPow_real5 = QtChart.QLineSeries()
        self.curveRwdPow_real5.setName("P2")
        self.chart_3.addSeries(self.curveRwdPow_real5)
        self.curveRwdPow_real5.attachAxis(self.__axisFreq_3)
        self.curveRwdPow_real5.attachAxis(self.__axisMag_3)
        self.chart_3.legend().markers(self.curveRwdPow_real5)[0].setVisible(False)
        self.chart_3.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(128, 0, 128))     # purple
        pen.setWidth(1)
        self.curveRwdPow_real5.setPen(pen)
        self.curveRwdPow_real5.setPointsVisible(True)
        self.curveRwdPow_real5.hovered.connect(self.do_series_hovered)
        self.curveRwdPow_real5.clicked.connect(self.do_series_clicked)

        # open and read measurement data
        # measurement data in position 1
        #self.measuredFreq = []  # init parameters
        #self.forwardPower = []  # init parameters
        #self.probData = []      # init parameters
        #with open("./output.csv", "r") as FSCaliData:
            #reader = csv.reader(FSCaliData)
           #rows = []
            #for row in reader:
               # rows.append(row)
            #print(rows)
       # for i in range(len(rows)):
            #self.measuredFreq.append(float(rows[i][0]))    # column 0 is frequency
            #self.forwardPower.append(float(rows[i][1]))    # column 1 is forward power
            #self.probData.append(float(rows[i][2]))        # column 2 is measurement data field strength from prob

        # adding data forward power to chart1
        #for a, b in zip(self.measuredFreq, self.forwardPower):
            #self.curveFPower1.append(a, b)
        # adding data field strength to chart1
        #for a, b in zip(self.measuredFreq, self.probData):
            #self.curveFieldStr_1.append(a, b)

        # define signal slots
        self.toolButton_testparameter.clicked.connect(self.showCalibrationEditWindow)
        self.toolButton_start.clicked.connect(self.start_test)  # signal connect to test function later rewrite!!
        self.toolButton_pause.clicked.connect(self.pause_test)  # signal connect to test function later rewrite!!
        self.toolButton_stop.clicked.connect(self.stop_test)    # signal connect to test function later rewrite!!
        self.pushButton_ShowHideCurve_1.clicked.connect(self.ShowHideCurveP1)
        self.pushButton_ShowHideCurve_2.clicked.connect(self.ShowHideCurveP2)
        self.pushButton_ShowHideCurve_3.clicked.connect(self.ShowHideCurveP3)
        self.pushButton_ShowHideCurve_4.clicked.connect(self.ShowHideCurveP4)
        self.pushButton_ShowHideCurve_5.clicked.connect(self.ShowHideCurveP5)
        self.toolButton_start.clicked.connect(self.clearGraphics)   # clear graphics when calibration start
        self.toolButton_tabulardaten.clicked.connect(self.showTabularTate)
        #self.toolButton_open.clicked.connect(self.loadNewData)
        self.toolButton_new.clicked.connect(self.clearGraphics)     # clear graphics
        self.toolButton_new.clicked.connect(self.clearParameter)    # clear parameters
        self.toolButton_save.clicked.connect(self.dataSave2)
        self.toolButton_result.clicked.connect(self.caliResult)
        #self.toolButton_open.clicked.connect(self.loadNewData2)
        self.comboBox_chart.currentIndexChanged.connect(self.changeChart)

        self.toolButton_open.clicked.connect(self.loadData)

        #self.toolButton_save.clicked.connect(self.dataSave)
        #self.toolButton_save.clicked.connect(self.savetest)

    # this function used for load all 5 positions data
    def loadNewData2(self):
        self.clearGraphics()
        self.measuredFreq = []  # init parameters
        self.forwardPower = []  # init parameters
        self.probData = []      # init parameters
        filepath = self.open_file()
        if not filepath == "":
            with open("%s" % filepath, "r") as FSCaliData:
                reader = csv.reader(FSCaliData)
                rows = []
                for row in reader:
                    rows.append(row)
            for i in range(len(rows)):
                self.measuredFreq.append(float(rows[i][0]))
                self.forwardPower.append(float(rows[i][1]))
                self.probData.append(float(rows[i][2]))
            for a, b in zip(self.measuredFreq, self.forwardPower):
                self.curveFPower1.append(a, b)
            for a, b in zip(self.measuredFreq, self.probData):
                self.curveFieldStr_1.append(a, b)
    #
    def caliResult(self):
        filepath = self.open_file()
        # get data

        if not filepath == "":
            pass
    # adding new data to graphics
    # once for 1 position
    def loadNewData(self):
        self.measuredFreq = []  # init parameters
        self.forwardPower = []  # init parameters
        self.probData = []
        filepath = self.open_file()
        if not filepath == "":
            with open("%s" % filepath, "r") as FSCaliData:
                reader = csv.reader(FSCaliData)
                rows = []
                for row in reader:
                    rows.append(row)
                print(rows)
            for i in range(len(rows)):
                self.measuredFreq.append(float(rows[i][0]))    # column 0 is frequency
                self.forwardPower.append(float(rows[i][1]))    # column 1 is forward power
                self.probData.append(float(rows[i][2]))        # column 2 is measurement data field strength from prob

            if not self.chart_2.legend().markers(self.curveFPower2)[0].isVisible():
                # adding data forward power to chart2
                for a, b in zip(self.measuredFreq, self.forwardPower):
                    self.curveFPower2.append(a, b)
                # adding data field strength to chart1
                for a, b in zip(self.measuredFreq, self.probData):
                    self.curveFieldStr_2.append(a, b)
                self.chart_1.legend().markers(self.curveFieldStr_2)[0].setVisible(True)
                self.chart_2.legend().markers(self.curveFPower2)[0].setVisible(True)
            elif not self.chart_2.legend().markers(self.curveFPower3)[0].isVisible():
                # adding data forward power to chart2
                for a, b in zip(self.measuredFreq, self.forwardPower):
                    self.curveFPower3.append(a, b)
                # adding data field strength to chart1
                for a, b in zip(self.measuredFreq, self.probData):
                    self.curveFieldStr_3.append(a, b)
                self.chart_1.legend().markers(self.curveFieldStr_3)[0].setVisible(True)
                self.chart_2.legend().markers(self.curveFPower3)[0].setVisible(True)
            elif not self.chart_2.legend().markers(self.curveFPower4)[0].isVisible():
                # adding data forward power to chart2
                for a, b in zip(self.measuredFreq, self.forwardPower):
                    self.curveFPower4.append(a, b)
                # adding data field strength to chart1
                for a, b in zip(self.measuredFreq, self.probData):
                    self.curveFieldStr_4.append(a, b)
                self.chart_1.legend().markers(self.curveFieldStr_4)[0].setVisible(True)
                self.chart_2.legend().markers(self.curveFPower4)[0].setVisible(True)
            elif not self.chart_2.legend().markers(self.curveFPower5)[0].isVisible():
                # adding data forward power to chart2
                for a, b in zip(self.measuredFreq, self.forwardPower):
                    self.curveFPower5.append(a, b)
                # adding data field strength to chart1
                for a, b in zip(self.measuredFreq, self.probData):
                    self.curveFieldStr_5.append(a, b)
                self.chart_1.legend().markers(self.curveFieldStr_5)[0].setVisible(True)
                self.chart_2.legend().markers(self.curveFPower5)[0].setVisible(True)

    # load the calibration data
    # Numpy and panda method
    def loadData(self):

        filepath = self.open_file()
        if not filepath == "":
            caliData = pd.read_csv('%s' % filepath, header=0).values
            spiltData = np.hsplit(caliData, 6)
            freqlist = np.array((spiltData[0]))
            fielStr = np.array((spiltData[1]))
            fwdPow = np.array((spiltData[2]))
            bwdPow = np.array((spiltData[3]))
            measuredLevel = np.array((spiltData[4]))
            validCheck = np.array((spiltData[5]))
            #newshap = validCheck.reshape(1, len(validCheck))
            newshap = np.concatenate(validCheck, axis=None)
            isValidIndex = np.where(newshap == 1)
            length = len(isValidIndex)
            #print("freqlist %s" %freqlist)
            #print("Index %s" % isValidIndex)
            for i in isValidIndex:
                #print("i is %s" %i)
                #print(freqlist[i])
                freqlistValid = []
               # fwdPowValid = []
                fielStrValid = []
                freqlistValid.append(freqlist[i])
                #fwdPowValid.append(fwdPow[i])
                fielStrValid.append(fielStr[i])
                freqlistValid = np.concatenate(freqlistValid, axis=None)
                fielStrValid = np.concatenate(fielStrValid, axis=None)
            #print(freqlistValid)
           # print(fielStrValid)
            #self.curveFieldStr_1.append(freqlistValid, fielStrValid)
                #for a, b in zip(freqlistValid, fwdPowValid):
                    #self.curveFPower1.append(a, b)
                for a, b in zip(freqlistValid, fielStrValid):
                    self.curveFieldStr_1.append(a, b)
            #print("freqlistvalid %s" % freqlistValid)
            #print("freqlist %s" % freqlist)
            #print("caliData %s" % caliData)
            #print("isValid %s" % validCheck)
            #print("isValid %s" % newshap)


    # choose a csv file and give the file path
    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Kalibrierungsdaten öffnen', '', 'csv files (*.csv)')
        self.path = filename[0]
        return self.path

    def clearGraphics(self):
        self.progressBar_status.setValue(0)
        self.curveFieldStr_real.clear()
        self.curveFieldStr_real2.clear()
        self.curveFieldStr_real3.clear()
        self.curveFieldStr_real4.clear()
        self.curveFieldStr_real5.clear()
        self.curveFPower_real.clear()
        self.curveFPower_real2.clear()
        self.curveFPower_real3.clear()
        self.curveFPower_real4.clear()
        self.curveFPower_real5.clear()
        self.curveRwdPow_real.clear()
        self.curveRwdPow_real2.clear()
        self.curveRwdPow_real3.clear()
        self.curveRwdPow_real4.clear()
        self.curveRwdPow_real5.clear()
        self.curveFieldStr_1.clear()
        self.curveFPower1.clear()
        self.curveFieldStr_2.clear()
        self.curveFPower2.clear()
        self.curveFieldStr_3.clear()
        self.curveFPower3.clear()
        self.curveFieldStr_4.clear()
        self.curveFPower4.clear()
        self.curveFieldStr_5.clear()
        self.curveFPower5.clear()
        self.chart_1.legend().markers(self.curveFieldStr_1)[0].setVisible(False)
        self.chart_1.legend().markers(self.curveFieldStr_2)[0].setVisible(False)
        self.chart_1.legend().markers(self.curveFieldStr_3)[0].setVisible(False)
        self.chart_1.legend().markers(self.curveFieldStr_4)[0].setVisible(False)
        self.chart_1.legend().markers(self.curveFieldStr_5)[0].setVisible(False)
        self.chart_2.legend().markers(self.curveFPower1)[0].setVisible(False)
        self.chart_2.legend().markers(self.curveFPower2)[0].setVisible(False)
        self.chart_2.legend().markers(self.curveFPower3)[0].setVisible(False)
        self.chart_2.legend().markers(self.curveFPower4)[0].setVisible(False)
        self.chart_2.legend().markers(self.curveFPower5)[0].setVisible(False)
        self.chart_3.legend().markers(self.curveRwdPow_real)[0].setVisible(False)
        self.chart_3.legend().markers(self.curveRwdPow_real2)[0].setVisible(False)
        self.chart_3.legend().markers(self.curveRwdPow_real3)[0].setVisible(False)
        self.chart_3.legend().markers(self.curveRwdPow_real4)[0].setVisible(False)
        self.chart_3.legend().markers(self.curveRwdPow_real5)[0].setVisible(False)

    def clearParameter(self):
        self.treeWidget_info.topLevelItem(0).setText(1, "")
        self.treeWidget_info.topLevelItem(1).setText(1, "")
        self.treeWidget_info.topLevelItem(2).setText(1, "")
        self.treeWidget_info.topLevelItem(3).setText(1, "")
        self.treeWidget_info.topLevelItem(4).setText(1, "")
        self.treeWidget_info.topLevelItem(5).setText(1, "")
        self.treeWidget_info.topLevelItem(6).setText(1, "")
        self.treeWidget_info.topLevelItem(7).setText(1, "")
        self.treeWidget_info.topLevelItem(8).setText(1, "")
        self.treeWidget_info.topLevelItem(9).setText(1, "")

    def ShowHideCurveP1(self):
        #if self.curveFPower1.isVisible():
            #self.curveFPower1.hide()
            #self.curveFieldStr_1.hide()
        #else:
            #self.curveFPower1.show()
            #self.curveFieldStr_1.show()
        if self.curveFPower_real.isVisible():
            self.curveFPower_real.hide()
            self.curveFieldStr_real.hide()
            self.curveRwdPow_real.hide()
        else:
            self.curveFPower_real.show()
            self.curveFieldStr_real.show()
            self.curveRwdPow_real.show()

    def ShowHideCurveP2(self):
        #if self.curveFPower2.isVisible():
            #self.curveFPower2.hide()
            #self.curveFieldStr_1.hide()
        #else:
            #self.curveFPower2.show()
            #self.curveFieldStr_2.show()
        if self.curveFPower_real2.isVisible():
            self.curveFPower_real2.hide()
            self.curveFieldStr_real2.hide()
            self.curveRwdPow_real2.hide()
        else:
            self.curveFPower_real2.show()
            self.curveFieldStr_real2.show()
            self.curveRwdPow_real2.show()

    def ShowHideCurveP3(self):
        #if self.curveFPower3.isVisible():
            #self.curveFPower3.hide()
            #self.curveFieldStr_3.hide()
        #else:
            #self.curveFPower3.show()
            #self.curveFieldStr_3.show()
        if self.curveFPower_real3.isVisible():
            self.curveFPower_real3.hide()
            self.curveFieldStr_real3.hide()
            self.curveRwdPow_real3.hide()
        else:
            self.curveFPower_real3.show()
            self.curveFieldStr_real3.show()
            self.curveRwdPow_real3.show()

    def ShowHideCurveP4(self):
        #if self.curveFPower4.isVisible():
            #self.curveFPower4.hide()
            #self.curveFieldStr_4.hide()
        #else:
            #self.curveFPower4.show()
            #self.curveFieldStr_4.show()
        if self.curveFPower_real4.isVisible():
            self.curveFPower_real4.hide()
            self.curveFieldStr_real4.hide()
            self.curveRwdPow_real4.hide()
        else:
            self.curveFPower_real4.show()
            self.curveFieldStr_real4.show()
            self.curveRwdPow_real4.show()

    def ShowHideCurveP5(self):
        #if self.curveFPower5.isVisible():
            #self.curveFPower5.hide()
            #self.curveFieldStr_5.hide()
        #else:
            #self.curveFPower5.show()
            #self.curveFieldStr_5.show()
        if self.curveFPower_real5.isVisible():
            self.curveFPower_real5.hide()
            self.curveFieldStr_real5.hide()
            self.curveRwdPow_real5.hide()
        else:
            self.curveFPower_real5.show()
            self.curveFieldStr_real5.show()
            self.curveRwdPow_real5.show()


    def changeChart(self):
        if self.comboBox_chart.currentText() == "Vorwärtsleistung":
            self.graphicsView_2.setChart(self.chart_2)
        elif self.comboBox_chart.currentText() == "Rückwärtsleistung":
            self.graphicsView_2.setChart(self.chart_3)

    def showCalibrationEditWindow(self):
        dialog = CalibrationEditWindow(self)
        dialog.exec_()
        # update parameters for calibration setup
        if not dialog.itemIndex == "":
            self.index = int(dialog.itemIndex)
            if dialog.comboBox_Pos.currentText() == "Alle 5":
                self.Position = 1         # "Alle 5" start with position 1
            else:
                self.Position = int(dialog.comboBox_Pos.currentText())
            self.Polarisation = dialog.comboBox_Polar.currentText()
            self.treeWidget_info.topLevelItem(0).setText(1, "%s" % dialog.comboBox_Pos.currentText())
            self.treeWidget_info.topLevelItem(1).setText(1, "%s" % dialog.comboBox_Polar.currentText())
            self.treeWidget_info.topLevelItem(2).setText(1, "%s" % dialog.treeWidget_parameters.topLevelItem(self.index).text(0))
            self.treeWidget_info.topLevelItem(3).setText(1, "%s" % dialog.treeWidget_parameters.topLevelItem(self.index).text(1))
            self.treeWidget_info.topLevelItem(4).setText(1, "%s" % dialog.treeWidget_parameters.topLevelItem(self.index).text(2))
            self.treeWidget_info.topLevelItem(5).setText(1, "%s" % dialog.treeWidget_parameters.topLevelItem(self.index).text(3))
            self.treeWidget_info.topLevelItem(6).setText(1, "%s" % dialog.treeWidget_parameters.topLevelItem(self.index).text(4))
            self.treeWidget_info.topLevelItem(7).setText(1, "%s" % dialog.lineEdit_StartDrive.text())
            self.treeWidget_info.topLevelItem(8).setText(1, "%s" % dialog.lineEdit_feldTol.text())
            self.treeWidget_info.topLevelItem(9).setText(1, "%s" % dialog.lineEdit_powMeterTol.text())
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

        # get startAPM
        self.startAPM = int(dialog.lineEdit_StartDrive.text())

        print("start fre %s" % self.StartFreq)
        print("max Frequenz %s" % self.MaxFreq)
        print('startAPM: %s' % self.startAPM)
        print("level  %s" % self.level)

    # test function delete later
    def start_test(self):
        self.freqList = []
        self.vorPowList = []
        self.feilStrList = []
        if self.treeWidget_info.topLevelItem(0).text(1) == "" or \
                self.treeWidget_info.topLevelItem(1).text(1) == "" or \
                self.treeWidget_info.topLevelItem(2).text(1) == "" or \
                self.treeWidget_info.topLevelItem(3).text(1) == "" or \
                self.treeWidget_info.topLevelItem(4).text(1) == "" or \
                self.treeWidget_info.topLevelItem(5).text(1) == "":
            QtWidgets.QMessageBox.information(self, "Hinweis", "Bitte alle Parameter einstellen")
        else:
            # activate the stop and pause button
            self.toolButton_stop.setEnabled(True)
            self.toolButton_pause.setEnabled(True)

            self.External_FS_test = External_FS_test(StartFreq=self.StartFreq,
                                                 FreqStep=self.FreStep, MaxFreq=self.MaxFreq, E_T=self.level,
                                                     startAPM=self.startAPM,
                                                     Position=self.Position, Polarisation=self.Polarisation)
            self.External_FS_test.start()
            self.label_TestRunningStatus.setText("Test läuft")
            self.label_status.setText("Status: %s (%s)" % (
            self.label_TestRunningStatus.text(), time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())))
            self.External_FS_test.countChanged.connect(self.onCountChanged)
            self.External_FS_test.completedflag.connect(self.testCompletedflag)
            # disable the start button when calibration is running
            self.toolButton_start.setEnabled(False)
        #self.External_FS_test.dataCache.connect(self.onDataCache)

    # test function delete later
    def pause_test(self):
        if not self.External_FS_test.isPaused:
            self.External_FS_test.pause()
            self.label_TestRunningStatus.setText("Test pausiert!")
            self.label_status.setText("Status: %s (%s)" % (
                self.label_TestRunningStatus.text(), time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())))
        else:
            self.External_FS_test.resum()
            self.label_TestRunningStatus.setText("Test läuft!")
            self.label_status.setText("Status: %s (%s)" % (
                self.label_TestRunningStatus.text(), time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())))

    # test function delete later
    def stop_test(self):
        if self.External_FS_test.isRunning():
            self.External_FS_test.stop()
            time.sleep(1)
            self.label_TestRunningStatus.setText("Test wird gestoppt!")
        self.label_status.setText("Status: %s (%s)" % (
            self.label_TestRunningStatus.text(), time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())))
        # enable the start button
        self.toolButton_start.setEnabled(True)
        self.toolButton_stop.setEnabled(False)
        self.toolButton_pause.setEnabled(False)

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

            self.calc = External_FS_test(E_T=self.FieldStrength, f_min=self.StartFreq, f_step=self.FreStep,
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

    def onDataCache(self, listFre, listPow, listFeld):
        self.testresult = [listFre,listPow,listFeld]
        #self.testresult = listPow
        #self.testresult  = listFeld
        print("saved data is %s" % self.testresult)

    # used to update the diagram
    def onCountChanged(self, measuredFreq, vorPower, bwdPow, FieldStrength, position):  # the parameters rewrite later
        frequency = measuredFreq
        magnitude1FwdPow = vorPower
        magnitude1RwdPow = bwdPow
        magnitude2 = FieldStrength
        Pos = position
        self.freqList.append(measuredFreq)
        self.vorPowList.append(vorPower)
        self.feilStrList.append(FieldStrength)
        # adding real time data to chart
        if Pos == 1:
            self.curveFPower_real.append(frequency, magnitude1FwdPow)
            self.curveFieldStr_real.append(frequency, magnitude2)
            self.curveRwdPow_real.append(frequency, magnitude1RwdPow)
            self.chart_2.legend().markers(self.curveFPower_real)[0].setVisible(True)
            self.chart_1.legend().markers(self.curveFieldStr_real)[0].setVisible(True)
            self.chart_3.legend().markers(self.curveRwdPow_real)[0].setVisible(True)

        elif Pos == 2:
            self.curveFPower_real2.append(frequency, magnitude1FwdPow)
            self.curveFieldStr_real2.append(frequency, magnitude2)
            self.curveRwdPow_real2.append(frequency, magnitude1RwdPow)
            self.chart_2.legend().markers(self.curveFPower_real2)[0].setVisible(True)
            self.chart_1.legend().markers(self.curveFieldStr_real2)[0].setVisible(True)
            self.chart_3.legend().markers(self.curveRwdPow_real2)[0].setVisible(True)
        elif Pos == 3:
            self.curveFPower_real3.append(frequency, magnitude1FwdPow)
            self.curveFieldStr_real3.append(frequency, magnitude2)
            self.curveRwdPow_real3.append(frequency, magnitude1RwdPow)
            self.chart_2.legend().markers(self.curveFPower_real3)[0].setVisible(True)
            self.chart_1.legend().markers(self.curveFieldStr_real3)[0].setVisible(True)
            self.chart_3.legend().markers(self.curveRwdPow_real3)[0].setVisible(True)
        elif Pos == 4:
            self.curveFPower_real4.append(frequency, magnitude1FwdPow)
            self.curveFieldStr_real4.append(frequency, magnitude2)
            self.curveRwdPow_real4.append(frequency, magnitude1RwdPow)
            self.chart_2.legend().markers(self.curveFPower_real4)[0].setVisible(True)
            self.chart_1.legend().markers(self.curveFieldStr_real4)[0].setVisible(True)
            self.chart_3.legend().markers(self.curveRwdPow_real4)[0].setVisible(True)
        elif Pos == 5:
            self.curveFPower_real5.append(frequency, magnitude1FwdPow)
            self.curveFieldStr_real5.append(frequency, magnitude2)
            self.curveRwdPow_real5.append(frequency, magnitude1RwdPow)
            self.chart_2.legend().markers(self.curveFPower_real5)[0].setVisible(True)
            self.chart_1.legend().markers(self.curveFieldStr_real5)[0].setVisible(True)
            self.chart_3.legend().markers(self.curveRwdPow_real5)[0].setVisible(True)

        value = ((frequency - self.StartFreq) / ((self.MaxFreq / (self.FreStep + 1.0)) - self.StartFreq)) * 100
        self.progressBar_status.setValue(value)

        #print("test data %s" % testdata)
        #print("start Fre %s" % self.StartFreq)
        #print("value ist %s" % value)
        #print("max freq %s" % self.MaxFreq)

    def testCompletedflag(self, completed, position):
        if completed:
            self.label_TestRunningStatus.setText("Kalibrierung für Position %s ist fertig!" % position)

            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Achtung!!')
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
            messageBox.setText('Kalibrierung für Position %s ist fertig!\n '
                               'Bitte die Sonde auf die nächste Position einstellen!' % position)
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
            buttonY.setText('Fortfahren')
            buttonN = messageBox.button(QtWidgets.QMessageBox.Cancel)
            buttonN.setText('Kalibrierung enden')
            if messageBox.exec_() == QtWidgets.QMessageBox.Ok:
                self.External_FS_test.runNextTest()
            else:
                self.External_FS_test.stop()
                self.toolButton_start.setEnabled(True)
        if completed and position == 5:
            self.toolButton_start.setEnabled(True)
            self.toolButton_stop.setEnabled(False)
            self.toolButton_pause.setEnabled(False)
            self.progressBar_status.setValue(0)
            # remain the user save data
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Daten speichern?')
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
            messageBox.setText('Die Kaliebrierung ist fertig!\n '
                               'Bitte die Daten speichern!')
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
            buttonY.setText('Speichern unter')
            buttonN = messageBox.button(QtWidgets.QMessageBox.Cancel)
            buttonN.setText('Nicht speichern')
            if messageBox.exec_() == QtWidgets.QMessageBox.Ok:
                print("aaa")
                filename = QFileDialog.getSaveFileName(self, "Save File", "./data", "csv file(*.csv)")
                if not filename[0] == "":
                    self.External_FS_test.saveData(filename[0])

        #completedflag = completed
        #currentTestPos = position
        #return completedflag, currentTestPos

    def showTabularTate(self):
        dialog = TabularDateWindow()
        if dialog.path != "":
            dialog.exec_()

    # use numpy and panda
    def dataSave2(self):
        filename = QFileDialog.getSaveFileName(self, "Save File", "./data", "csv file(*.csv)")
        if not filename[0] == "":
            result = caliDataProcessing()
            writeF = pd.DataFrame(result)
            writeF.to_csv('%s' % filename[0], index=False)
    # save the data for one test position
    #
    def dataSave(self):
        print("freq list %s" % self.freqList)
        filename = QFileDialog.getSaveFileName(self, "Save File", "./data", "csv file(*.csv)")
        header = ["Test-Position 1","","", "Test-Position 2","","","Test-Position 3","","", "Test-Position 4","","", "Test-Position 5","","",]
        if not filename[0] == "":
            print("name is %s " %filename[0])
            print(filename)
            if not os.path.exists(filename[0]):
                #if os.stat(filename[0]).st_size == 0:
                with open(filename[0], 'w') as FSCaliData:
                    datawriter = csv.writer(FSCaliData)
                    #datawriter.writerow(header)
                    #data = []
                    #data.append(self.freqList)
                    #data.append(self.vorPowList)
                    #data.append(self.feilStrList)
                    #datawriter.writerows(data)
                    data = zip(self.freqList, self.vorPowList, self.feilStrList)
                    #data = zip(self.freqList, self.vorPowList, self.feilStrList)
                    #self.alldata = self.alldata + data
                    #datawriter.writerow(["Frequenz", "Vorwärtsleistung", "Feldstärke"])
                    datawriter.writerows(data)
                    print(data)
            else:
                # get the old data
                with open(filename[0], 'r') as FSCaliData:
                    datareader = csv.reader(FSCaliData)
                    rows = []
                    for row in datareader:
                        rows.append(row)
                    columnumer = len(rows)
                    print("column numer %s" % columnumer)
                    print("rows number is %s" % len(rows))
                    print("fre number is %s" % len(self.freqList))
                    #rows[1].append("Frequenz"+"ddd"+"dddd")
                   #rows[1].append("Frequenz")
                    #rows[1].append("Frequenz")
                    for i in range(len(rows)):
                        rows[i].append(self.freqList[i])
                        rows[i].append(self.vorPowList[i])
                        rows[i].append(self.feilStrList[i])
                    print("new rwos is %s" % rows)
                # append the new test data to a new column and rewrite the file
                with open(filename[0], 'w') as FSCaliData:
                    datawriter = csv.writer(FSCaliData)
                    datawriter.writerows(rows)


                print("ok")
            #elif os.path.exists(filename[0]):
               #data = zip(self.freqList, self.vorPowList, self.feilStrList)
                #with open(filename[0], "a") as FSCaliData:
                    #datawriter = csv.writer(FSCaliData)
                    #datawriter.writerows(data)


                #for i in range(len(self.freqList)):
                    #datawriter.writerows(self.freqList)
                    #datawriter.writerows(self.vorPowList)
                    #datawriter.writerows(self.feilStrList)

    # when mouse is moving on a curve, the coordinates of the spot, where the mouse is pointing to, on the curve
    # will be showed in the Status bar
    def do_series_hovered(self, point, state):
        if state:
            horizontal_coor = "%.2f" % point.x()
            vertical_coor = "%.2f" % point.y()
            self.GeschwebtFrequenzLineEdit.setText(horizontal_coor)
            self.GeschwebtMagnitudeLineEdit.setText(vertical_coor)

    # when mouse clicks a spot on a curve, the coordinates of the spot will be showed in the Status bar
    def do_series_clicked(self, point):
        horizontal_coor = "%.2f" % point.x()
        vertical_coor = "%.2f" % point.y()
        self.GeklicktFrequenzLineEdit.setText(horizontal_coor)
        self.GeklicktMagnitudeLineEdit.setText(vertical_coor)

    # the current coordinates of the mouse will be showed continously in the status bar in real-time
    def do_chartView_mouseMove(self, point):
        pt = self.graphicsView.chart().mapToValue(point)
        pt2 = self.graphicsView_2.chart().mapToValue(point)
        self.MousPositionLabel.setText("Chart X=%.2f,Y=%.2f" % (pt.x(), pt.y()))
        self.MousPositionLabel.setText("Chart X=%.2f,Y=%.2f" % (pt2.x(), pt2.y()))


    def color(hex):
        r = int(hex[1:3], 16)
        g = int(hex[3:5], 16)
        b = int(hex[5:7], 16)
        return r, g, b


# this class define the window of calibration settings
class CalibrationEditWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CalibrationEditWindow, self).__init__(parent)
        uic.loadUi("uifiles/KalibierungEinstellen.ui", self)
        self.itemIndex = ""
        self.paragroup = []

        # show the saved parameter setup
        f = open("./data/KalibrierungEinstellungsDaten.txt", "r")
        alllines = f.readlines()
        f.close()
        for i in range(len(alllines)):
            self.paragroup.append(alllines[i].strip().split())
        #paragroup1 = alllines[0].strip()
        #paragroup2 = alllines[1].strip()
        #self.paralist2 = paragroup2.split()
        #self.paralist = paragroup1.split()
        print(len(alllines))
        print(self.paragroup)
        print("length %s" % self.paragroup)
        if not self.paragroup == []:
            for i in range(len(self.paragroup)):
                self.treeWidget_parameters.topLevelItem(i).setText(0, "%s" % self.paragroup[i][0])
                self.treeWidget_parameters.topLevelItem(i).setText(1, "%s" % self.paragroup[i][1])
                self.treeWidget_parameters.topLevelItem(i).setText(2, "%s" % self.paragroup[i][2])
                self.treeWidget_parameters.topLevelItem(i).setText(3, "%s" % self.paragroup[i][3])
                self.treeWidget_parameters.topLevelItem(i).setText(4, "%s" % self.paragroup[i][4])
        #if not self.paralist == []:
            #self.treeWidget_parameters.topLevelItem(0).setText(0, "%s" % self.paralist[0])
            #self.treeWidget_parameters.topLevelItem(0).setText(1, "%s" % self.paralist[1])
            #self.treeWidget_parameters.topLevelItem(0).setText(2, "%s" % self.paralist[2])
            #self.treeWidget_parameters.topLevelItem(0).setText(3, "%s" % self.paralist[3])
           # self.treeWidget_parameters.topLevelItem(0).setText(4, "%s" % self.paralist[4])
            #self.treeWidget_parameters.topLevelItem(1).setText(0, "%s" % self.paralist2[0])
            #self.treeWidget_parameters.topLevelItem(1).setText(1, "%s" % self.paralist2[1])
            #self.treeWidget_parameters.topLevelItem(1).setText(2, "%s" % self.paralist2[2])
            #self.treeWidget_parameters.topLevelItem(1).setText(3, "%s" % self.paralist2[3])
            #self.treeWidget_parameters.topLevelItem(1).setText(4, "%s" % self.paralist2[4])


        # define Signal Slots
        self.treeWidget_parameters.doubleClicked.connect(self.findParaEdit)
        # self.toolButton_new.clicked.connect(self.findParaEdit)
        self.toolButton_new.clicked.connect(self.setnewPara)
        self.buttonBox.accepted.connect(self.saveData)
        self.treeWidget_parameters.itemClicked.connect(self.currentItemIndex)

    # get the index of selected item
    def currentItemIndex(self):
        self.currentItem = self.treeWidget_parameters.selectedItems()
        self.itemIndex = self.treeWidget_parameters.indexFromItem(self.currentItem[0], 0).row() # Returns the row this model index refers to
        global indexNum     # save the index of chosen item in tree widget
        indexNum = self.itemIndex
        print(self.currentItem[0])
        print(self.currentItem[0].text(0))
        print(self.currentItem[0].text(1))
        print(self.itemIndex)
        return self.itemIndex

    def findParaEdit(self):
        dialog = ParametersEditWindow(self)
        #applybtn = dialog.edit_var_parameters.button(dialog.edit_var_parameters.Apply)
        #if dialog.edit_var_parameters.clicked.connect(self.accept):
        #if dialog.edit_var_parameters.clicked(applybtn):
            #print("clicked")
        dialog.exec_()

        # self.treeWidget_parameters.topLevelItem(0).setText(0, "%s" % self.paralist[0])
        # updating parameters from file
        #f = open("./data/KalibrierungEinstellungsDaten.txt", "r")
        #alllines = f.readlines()
        #paragroup1 = alllines[0].strip()
        #self.paralist = paragroup1.split()
        #f.close()
        #self.treeWidget_parameters.topLevelItem(0).setText(0, "%s" % self.paralist[0])
        #self.treeWidget_parameters.topLevelItem(0).setText(1, "%s" % self.paralist[1])
        #self.treeWidget_parameters.topLevelItem(0).setText(2, "%s" % self.paralist[2])
        #self.treeWidget_parameters.topLevelItem(0).setText(3, "%s" % self.paralist[3])
        #self.treeWidget_parameters.topLevelItem(0).setText(4, "%s" % self.paralist[4])
        if dialog.edit_var_parameters.accepted:
            self.treeWidget_parameters.topLevelItem(self.itemIndex).setText(0, "%s" % dialog.start_freq)
            self.treeWidget_parameters.topLevelItem(self.itemIndex).setText(1, "%s" % dialog.freq_step)
            self.treeWidget_parameters.topLevelItem(self.itemIndex).setText(2, "%s" % dialog.Max_freq)
            self.treeWidget_parameters.topLevelItem(self.itemIndex).setText(3, "%s" % dialog.TestLevel)
            self.treeWidget_parameters.topLevelItem(self.itemIndex).setText(4, "%s" % dialog.Dwell)
        elif dialog.edit_var_parameters.rejected:
            pass
            #dialog.quit()

    def setnewPara(self):
        dialog = ParametersEditWindow(self)
        dialog.lineEdit_frequency.setText("")
        dialog.lineEdit_step.setText("")
        dialog.lineEdit_MaxFreq.setText("")
        dialog.lineEdit_testlevel.setText("")
        dialog.lineEdit_Dwell.setText("")
        dialog.lineEdit_m1fre.setText("")
        dialog.lineEdit_m1dep.setText("")
        dialog.lineEdit_3.setText("")
        dialog.lineEdit_4.setText("")
        dialog.exec_()

    def saveData(self):
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

        #with open("./data/KalibrierungEinstellungsDaten.txt", "a") as add_position:
            #add_position.write("%s " % self.Position)
            #add_position.write("%s " % self.Polarisation)
            #add_position.write("\n")
        #add_position.close()


# this class define the window of parameters settings
class ParametersEditWindow(QtWidgets.QDialog):
    # signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("uifiles/ParaEditWindow.ui", self)

        # init paramters
        self.start_freq = self.lineEdit_frequency.text()
        self.freq_step = self.lineEdit_step.text()
        self.Max_freq = self.lineEdit_MaxFreq.text()
        self.TestLevel = self.lineEdit_testlevel.text()
        self.Dwell = self.lineEdit_Dwell.text()
        applybtn = self.edit_var_parameters.button(self.edit_var_parameters.Apply)

        # define signals
        self.edit_var_parameters.accepted.connect(self.saveData)

    def saveData(self):
        self.start_freq = self.lineEdit_frequency.text()
        self.freq_step = self.lineEdit_step.text()
        self.Max_freq = self.lineEdit_MaxFreq.text()
        self.TestLevel = self.lineEdit_testlevel.text()
        self.Dwell = self.lineEdit_Dwell.text()
        self.Position = " "
        self.Polarisation = " "
        self.paraSetup = []
        lineIndex = indexNum
        linetowrite = ["%s %s %s %s %s %s %s \n"
                       % (self.start_freq, self.freq_step, self.Max_freq, self.TestLevel, self.Dwell, self.Position, self.Polarisation)]
        f = open("./data/KalibrierungEinstellungsDaten.txt", "r")
        alllines = f.readlines()
        f.close()
        for i in range(len(alllines)):
            self.paraSetup.append(alllines[i])
        print(self.paraSetup)
        self.paraSetup[lineIndex] = linetowrite
        print("new file %s" % self.paraSetup)
        f = open("./data/KalibrierungEinstellungsDaten.txt", "w")
        for i in range(len(self.paraSetup)):
            for j in range(len(self.paraSetup[i])):
                f.write(self.paraSetup[i][j])
        f.close()
        #for i in range(len(self.parasetup)):
            #f.write(self.parasetup[i])
        #print("lineindex %s" % lineIndex)
        #f = open("./data/KalibrierungEinstellungsDaten.txt", "w")
        #f.writelines(["%s " % self.start_freq, "%s " % self.freq_step, "%s " % self.Max_freq, "%s " % self.TestLevel,
                      #"%s " % self.Dwell, "%s" % self.Position, "%s" % self.Polarisation])
        # f.write("\n")
        #f.close()


class TabularDateWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(TabularDateWindow, self).__init__(parent)
        uic.loadUi("uifiles/TabularDataWindow.ui", self)
        path = Ui_Calibration.open_file(self)   # path is tuple include filepath and filename
        if self.path != "":
            filename = path.split("/")[-1]
            #self.setWindowFilePath("%s" % path[0])
            self.setWindowTitle("%s" % filename)
            with open("%s" % path, "r") as FSCaliData:
            #with open("./output.csv", "r") as FSCaliData:
                reader = csv.reader(FSCaliData)
                rows = []
                for row in reader:
                    rows.append(row)
            rowPosition = self.tabularTable.rowCount()
            self.tabularTable.insertRow(rowPosition)
            rowCount = len(rows)
            self.tabularTable.setRowCount(rowCount)
            for i in range(len(rows)):
                self.tabularTable.setItem(i, 0, QTableWidgetItem(rows[i][0]))
                self.tabularTable.setItem(i, 1, QTableWidgetItem(rows[i][1]))
                self.tabularTable.setItem(i, 2, QTableWidgetItem(rows[i][2]))
                # self.measuredFreq.append(float(self.rows[i][0]))  # column 0 is frequency
                # self.forwardPower.append(float(self.rows[i][1]))  # column 1 is forward power
                # self.probData.append(float(self.rows[i][2]))  # column 2 is measurement data from prob


class RemainderDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("uifiles/remainderWindow.ui", self)
        self.label_reminder.setText("aaa")

        # define signals
        self.pushButton_continue.clicked.connect(self.startNextTest)
        #self.pushButton_cancle.clicked.connect()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Calibration()
    # ui.exec_()
    sys.exit(ui.exec_())
