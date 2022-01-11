# -*- coding: utf-8 -*-

# This script defines widgets and methods of the "Test" Window.

import sys
sys.path.append('gui')
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtChart
import time
import numpy as np

# "PyQt5.QtPrintSupport" supports printer. Qprint is used to print the diagramm in Test Window.
# QprintDialog is used to open the printer window.
# QpagesteupDialog is used for printer settings.
from PyQt5.QtPrintSupport import QPrinter,QPrintDialog,QPrintPreviewDialog
import WordReportGenerator
import cv2 as cv
import qimage2ndarray
import os
from thread_LE import External


# this class is used to customized a QChartView that can realize advanced functions.
# The advanced function is: When you press the left mouse on the diagramm in order to make a selection,
# a rectangular selection box will be displayed as the mouse is dragged.
class QmyChartView(QtChart.QChartView):
   mouseMove = QtCore.pyqtSignal(QtCore.QPoint)   #signal from mouse movement
   def __init__(self, parent=None):
      super().__init__(parent)
      self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
      self.__beginPoint=QtCore.QPoint()    # start point of the rectangular selection box
      self.__endPoint=QtCore.QPoint()      # end point of the rectangular selection box

# define the method of mouse presse
   def mousePressEvent(self,event):       # mouse click
      if event.button()==QtCore.Qt.LeftButton:
         self.__beginPoint=event.pos()    # record the start point
      super().mousePressEvent(event)

   def mouseMoveEvent(self,event):    # mouse movement
      point=event.pos()
      self.mouseMove.emit(point)      # emit the mouse movement signal
      super().mouseMoveEvent(event)

   def mouseReleaseEvent(self,event): # Mouse left frame selection to zoom in, right click to restore
      if event.button()==QtCore.Qt.LeftButton:
         self.__endPoint=event.pos()
         rectF=QtCore.QRectF()
         rectF.setTopLeft(self.__beginPoint)
         rectF.setBottomRight(self.__endPoint)
         self.chart().zoomIn(rectF)    # zoom in the seletced rectangular area
      elif event.button()==QtCore.Qt.RightButton:
         self.chart().zoomReset()      # right click to restore the zoomed area
      super().mouseReleaseEvent(event)

   def keyPressEvent(self,event):      # define the key press event
      key=event.key()
      if key==QtCore.Qt.Key_Plus:
         self.chart().zoom(1.2)
      elif key==QtCore.Qt.Key_Minus:
         self.chart().zoom(0.8)
      elif key==QtCore.Qt.Key_Left:
         self.chart().scroll(10,0)
      elif key==QtCore.Qt.Key_Right:
         self.chart().scroll(-10,0)
      elif key==QtCore.Qt.Key_Up:
         self.chart().scroll(0,-10)
      elif key==QtCore.Qt.Key_Down:
         self.chart().scroll(0,10)
      elif key==QtCore.Qt.Key_PageUp:
         self.chart().scroll(0,-50)
      elif key==QtCore.Qt.Key_PageDown:
         self.chart().scroll(0,50)
      elif key==QtCore.Qt.Key_Home:
         self.chart().zoomReset()
      super().keyPressEvent(event)


# This class defines the "Test" window, which is used to show up the visualized measurement results in real-time.
# It's Qt-Designer files are "TestWindow.ui" in folder "uifiles"
class Ui_TestWindow_LE(object):
    def setupUi(self, TestWindow):
        TestWindow.setObjectName("TestWindow")
        TestWindow.setWindowModality(QtCore.Qt.NonModal)
        TestWindow.resize(1613, 866)
        TestWindow.setMinimumSize(QtCore.QSize(1613, 866))
        TestWindow.setMaximumSize(QtCore.QSize(1613, 866))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        TestWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon_materials/7.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        TestWindow.setWindowIcon(icon)

        self.GraphicFrame = QtWidgets.QFrame(TestWindow)
        self.GraphicFrame.setGeometry(QtCore.QRect(20, 70, 1561, 541))
        self.GraphicFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.GraphicFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.GraphicFrame.setObjectName("GraphicFrame")

        # read the 1. Kabeldämpfungen
        self.fname1 = "./data/LMK11.TXT"
        aFile1 = open(self.fname1, 'r')
        allLine1 = aFile1.readlines()
        aFile1.close()
        rowCnt1 = len(allLine1)  # how many lines are in the .txt file
        vectF1 = [0] * rowCnt1
        vectMag1 = [0] * rowCnt1
        for i1 in range(len(allLine1)):
            lineText1 = allLine1[i1].strip()  # remove "\n" at each line end
            strList1 = lineText1.split()
            vectF1[i1] = float(strList1[0].replace(",", ".")) / 1000000.0
            vectMag1[i1] = float(strList1[1].replace(",", "."))
            if i1 == rowCnt1 - 1:
                break
        self.cablef1 = vectF1       # 1. Kabel Frequenz
        self.cablem1 = vectMag1     # 1. Kabel Dämpfungen

        # read the 2. Kabeldämpfungen
        self.fname2 = "./data/LMK12.TXT"
        aFile2 = open(self.fname2, 'r')
        allLine2 = aFile2.readlines()
        aFile2.close()
        rowCnt2 = len(allLine2)
        vectF2 = [0] * rowCnt2
        vectMag2 = [0] * rowCnt2
        for i2 in range(len(allLine2)):
            lineText2 = allLine2[i2].strip()
            strList2 = lineText2.split()
            vectF2[i2] = float(strList2[0].replace(",", ".")) / 1000000.0
            vectMag2[i2] = float(strList2[1].replace(",", "."))
            if i2 == rowCnt2 - 1:
                break
        self.cablef2 = vectF2          # 2. Kabel Frequenz
        self.cablem2 = vectMag2        # 2. Kabel Dämpfungen

        # read antenne factors
        self.fname = "./data/Antenne_Faktoren.txt"
        aFile = open(self.fname, 'r')
        allLine = aFile.readlines()
        aFile.close()
        rowCnt = len(allLine) - 2
        vectF = [0] * rowCnt
        vectMag = [0] * rowCnt
        for i in range(len(allLine)):
            lineText = allLine[i + 2].strip()
            strList = lineText.split()
            vectF[i] = float(strList[0][:-4]) / 1000000.0
            vectMag[i] = float(strList[1])
            if i == rowCnt - 1:
                break
        self.tianxianf=vectF         # Antenne Frequenz
        self.tianxianm=vectMag       # Antenne Faktoren

        # creation of the interactive diagramm in the "Test" window
        self.chart = QtChart.QChart()
        self.series_1 = QtChart.QLineSeries()
        self.series_1.setName("curve_1")
        self.series_2 = QtChart.QLineSeries()
        self.series_2.setName("curve_2")
        self.series_3 = QtChart.QLineSeries()
        self.series_3.setName("curve_3")
        self.series_4 = QtChart.QLineSeries()
        self.series_4.setName("curve_4")
        self.chart.addSeries(self.series_1)
        self.chart.addSeries(self.series_2)
        self.chart.addSeries(self.series_3)
        self.chart.addSeries(self.series_4)
        self.chart.legend().markers(self.series_1)[0].setVisible(False)
        self.chart.legend().markers(self.series_2)[0].setVisible(False)
        self.chart.legend().markers(self.series_3)[0].setVisible(False)
        self.chart.legend().markers(self.series_4)[0].setVisible(False)

        #QtChart.QCategoryAxis *axisX= new QCategoryAxis

        self.__axisFreq = QtChart.QLogValueAxis()
        self.__axisFreq.setLabelFormat("%d")  # format of the label
        self.__axisFreq.setTitleText("Frequenz / kHz ")
        self.__axisFreq.setRange(100, 30000)
        #self.__axisFreq.append
        x= [150,1000,10000,30000]
        strs=['150 kHz','1 MHz','10 MHz','30 MHz']
        ticks=[(i,j) for i,j in zip(x,strs)]
        self.__axisFreq.setMinorTickCount(8)
        #self.__axisFreq.tickAn([ticks])
        self.chart.addAxis(self.__axisFreq, QtCore.Qt.AlignBottom)


        self.__axisMag = QtChart.QValueAxis()
        self.__axisMag.setTitleText("Störspannung / dBμV ")
        self.__axisMag.setRange(20, 140)
        self.__axisMag.setTickCount(13)
        self.__axisMag.setLabelFormat("%d")
        self.chart.addAxis(self.__axisMag, QtCore.Qt.AlignLeft)

        self.series_1.attachAxis(self.__axisFreq)
        self.series_1.attachAxis(self.__axisMag)

        self.series_2.attachAxis(self.__axisFreq)
        self.series_2.attachAxis(self.__axisMag)

        self.series_3.attachAxis(self.__axisFreq)
        self.series_3.attachAxis(self.__axisMag)

        self.series_4.attachAxis(self.__axisFreq)
        self.series_4.attachAxis(self.__axisMag)

        # define signals
        self.series_1.hovered.connect(self.do_series_hovered)
        self.series_1.clicked.connect(self.do_series_clicked)

        # define signals
        self.series_2.hovered.connect(self.do_series_hovered)
        self.series_2.clicked.connect(self.do_series_clicked)

        # define signals
        self.series_3.hovered.connect(self.do_series_hovered)
        self.series_3.clicked.connect(self.do_series_clicked)

        # define signals
        self.series_4.hovered.connect(self.do_series_hovered)
        self.series_4.clicked.connect(self.do_series_clicked)

        self.graphicsView = QmyChartView(self.GraphicFrame)
        self.graphicsView.setGeometry(QtCore.QRect(10, 1, 1191, 531))
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView.setCursor(QtCore.Qt.ArrowCursor)
        self.graphicsView.mouseMove.connect(self.do_chartView_mouseMove)
        self.graphicsView.setChart(self.chart)
        self.graphicsView.setObjectName("graphicsView")

        self.label3 = QtWidgets.QLabel(self.graphicsView)
        self.label3.setGeometry(QtCore.QRect(81, 131, 421, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label3.setFont(font)
        self.label3.setStyleSheet("color: rgb(45, 130, 255);")
        self.label3.setObjectName("item3")
        self.label3.setText("Gruppe 1 (>20kVA). Klasse A. Quasi-Peak. 10m.")
        self.label3.hide()

        self.label1 = QtWidgets.QLabel(self.graphicsView)
        self.label1.setGeometry(QtCore.QRect(81, 81, 421, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label1.setFont(font)
        self.label1.setStyleSheet("color: rgb(45, 130, 255);")
        self.label1.setObjectName("item1")
        self.label1.setText("Gruppe 1 (>20kVA). Klasse A. Quasi-Peak. 3m.")
        self.label1.hide()

        self.label2 = QtWidgets.QLabel(self.graphicsView)
        self.label2.setGeometry(QtCore.QRect(551, 131, 421, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label2.setFont(font)
        self.label2.setStyleSheet("color: rgb(45, 130, 255);")
        self.label2.setObjectName("item2")
        self.label2.setText("Gruppe 1 (<=20kVA). Klasse A. Quasi-Peak. 3m.")
        self.label2.hide()

        self.label4 = QtWidgets.QLabel(self.graphicsView)
        self.label4.setGeometry(QtCore.QRect(81, 181, 431, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label4.setFont(font)
        self.label4.setStyleSheet("color: rgb(45, 130, 255);")
        self.label4.setObjectName("item4")
        self.label4.setText("Gruppe 1 (<=20kVA). Klasse A. Quasi-Peak. 10m.")
        self.label4.hide()

        self.label5 = QtWidgets.QLabel(self.graphicsView)
        self.label5.setGeometry(QtCore.QRect(551, 181, 431, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label5.setFont(font)
        self.label5.setStyleSheet("color: rgb(45, 130, 255);")
        self.label5.setObjectName("item5")
        self.label5.setText("Gruppe 1. Klasse B. Quasi-Peak. 3m.")
        self.label5.hide()

        self.label6 = QtWidgets.QLabel(self.graphicsView)
        self.label6.setGeometry(QtCore.QRect(81, 236, 431, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label6.setFont(font)
        self.label6.setStyleSheet("color: rgb(45, 130, 255);")
        self.label6.setObjectName("item6")
        self.label6.setText("Gruppe 1. Klasse B. Quasi-Peak. 10m.")
        self.label6.hide()

        self.StatusleisteGroupBox = QtWidgets.QGroupBox(self.GraphicFrame)
        self.StatusleisteGroupBox.setGeometry(QtCore.QRect(1230, 0, 331, 531))
        self.StatusleisteGroupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.StatusleisteGroupBox.setMaximumSize(QtCore.QSize(511, 11111))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.StatusleisteGroupBox.setFont(font)
        self.StatusleisteGroupBox.setObjectName("StatusleisteGroupBox")

        self.AktuellerZustandLineEdit = QtWidgets.QLineEdit(self.StatusleisteGroupBox)
        self.AktuellerZustandLineEdit.setGeometry(QtCore.QRect(20, 80, 231, 31))
        self.AktuellerZustandLineEdit.setMinimumSize(QtCore.QSize(231, 31))
        self.AktuellerZustandLineEdit.setMaximumSize(QtCore.QSize(231, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(245, 245, 245))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.AktuellerZustandLineEdit.setFont(font)
        self.AktuellerZustandLineEdit.setPalette(palette)
        self.AktuellerZustandLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.AktuellerZustandLineEdit.setText("")
        self.AktuellerZustandLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.AktuellerZustandLineEdit.setReadOnly(True)
        self.AktuellerZustandLineEdit.setText("Bereit zum Test.")
        self.AktuellerZustandLineEdit.setObjectName("AktuellerZustandLineEdit")

        self.AktuellerZustandLabel = QtWidgets.QLabel(self.StatusleisteGroupBox)
        self.AktuellerZustandLabel.setGeometry(QtCore.QRect(20, 40, 171, 31))
        self.AktuellerZustandLabel.setMinimumSize(QtCore.QSize(171, 31))
        self.AktuellerZustandLabel.setMaximumSize(QtCore.QSize(171, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.AktuellerZustandLabel.setFont(font)
        self.AktuellerZustandLabel.setObjectName("AktuellerZustandLabel")

        self.InformationenKoordinatenGroupBox = QtWidgets.QGroupBox(self.StatusleisteGroupBox)
        self.InformationenKoordinatenGroupBox.setGeometry(QtCore.QRect(10, 150, 311, 371))
        self.InformationenKoordinatenGroupBox.setMinimumSize(QtCore.QSize(0, 151))
        self.InformationenKoordinatenGroupBox.setMaximumSize(QtCore.QSize(631, 11111))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.InformationenKoordinatenGroupBox.setFont(font)
        self.InformationenKoordinatenGroupBox.setObjectName("InformationenKoordinatenGroupBox")

        self.GeschwebtMagnitudeLineEdit = QtWidgets.QLineEdit(self.InformationenKoordinatenGroupBox)
        self.GeschwebtMagnitudeLineEdit.setGeometry(QtCore.QRect(130, 140, 131, 31))
        self.GeschwebtMagnitudeLineEdit.setMinimumSize(QtCore.QSize(101, 31))
        self.GeschwebtMagnitudeLineEdit.setMaximumSize(QtCore.QSize(131, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.GeschwebtMagnitudeLineEdit.setFont(font)
        self.GeschwebtMagnitudeLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.GeschwebtMagnitudeLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.GeschwebtMagnitudeLineEdit.setPalette(palette)
        self.GeschwebtMagnitudeLineEdit.setReadOnly(True)
        self.GeschwebtMagnitudeLineEdit.setObjectName("GeschwebtMagnitudeLineEdit")

        self.GeschwebtFrequenzLineEdit = QtWidgets.QLineEdit(self.InformationenKoordinatenGroupBox)
        self.GeschwebtFrequenzLineEdit.setGeometry(QtCore.QRect(130, 90, 131, 31))
        self.GeschwebtFrequenzLineEdit.setMinimumSize(QtCore.QSize(101, 31))
        self.GeschwebtFrequenzLineEdit.setMaximumSize(QtCore.QSize(131, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.GeschwebtFrequenzLineEdit.setFont(font)
        self.GeschwebtFrequenzLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.GeschwebtFrequenzLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.GeschwebtFrequenzLineEdit.setReadOnly(True)
        self.GeschwebtFrequenzLineEdit.setPalette(palette)
        self.GeschwebtFrequenzLineEdit.setObjectName("GeschwebtFrequenzLineEdit")

        self.GeschwebtFrequenzLabel = QtWidgets.QLabel(self.InformationenKoordinatenGroupBox)
        self.GeschwebtFrequenzLabel.setGeometry(QtCore.QRect(20, 90, 91, 31))
        self.GeschwebtFrequenzLabel.setMinimumSize(QtCore.QSize(91, 31))
        self.GeschwebtFrequenzLabel.setMaximumSize(QtCore.QSize(91, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.GeschwebtFrequenzLabel.setFont(font)
        self.GeschwebtFrequenzLabel.setObjectName("GeschwebtFrequenzLabel")

        self.GeschwebtMagnitudeLabel = QtWidgets.QLabel(self.InformationenKoordinatenGroupBox)
        self.GeschwebtMagnitudeLabel.setGeometry(QtCore.QRect(20, 140, 101, 31))
        self.GeschwebtMagnitudeLabel.setMinimumSize(QtCore.QSize(101, 31))
        self.GeschwebtMagnitudeLabel.setMaximumSize(QtCore.QSize(101, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.GeschwebtMagnitudeLabel.setFont(font)
        self.GeschwebtMagnitudeLabel.setObjectName("GeschwebtMagnitudeLabel")

        self.GeschwebtLabel = QtWidgets.QLabel(self.InformationenKoordinatenGroupBox)
        self.GeschwebtLabel.setGeometry(QtCore.QRect(10, 40, 111, 31))
        self.GeschwebtLabel.setMinimumSize(QtCore.QSize(111, 31))
        self.GeschwebtLabel.setMaximumSize(QtCore.QSize(111, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.GeschwebtLabel.setFont(font)
        self.GeschwebtLabel.setObjectName("GeschwebtLabel")

        self.GeschwebtToolButton = QtWidgets.QToolButton(self.InformationenKoordinatenGroupBox)
        self.GeschwebtToolButton.setGeometry(QtCore.QRect(130, 40, 31, 31))
        self.GeschwebtToolButton.setMinimumSize(QtCore.QSize(31, 31))
        self.GeschwebtToolButton.setMaximumSize(QtCore.QSize(31, 31))
        self.GeschwebtToolButton.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("icon_materials/9.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.GeschwebtToolButton.setIcon(icon10)
        self.GeschwebtToolButton.setIconSize(QtCore.QSize(31, 31))
        self.GeschwebtToolButton.setStyleSheet("background-color: transparent")
        self.GeschwebtToolButton.setObjectName("GeschwebtToolButton")

        self.GeklicktToolButton = QtWidgets.QToolButton(self.InformationenKoordinatenGroupBox)
        self.GeklicktToolButton.setGeometry(QtCore.QRect(130, 200, 31, 31))
        self.GeklicktToolButton.setMinimumSize(QtCore.QSize(31, 31))
        self.GeklicktToolButton.setMaximumSize(QtCore.QSize(31, 31))
        self.GeklicktToolButton.setText("")
        self.GeklicktToolButton.setIcon(icon10)
        self.GeklicktToolButton.setIconSize(QtCore.QSize(31, 31))
        self.GeklicktToolButton.setStyleSheet("background-color: transparent")
        self.GeklicktToolButton.setObjectName("GeklicktToolButton")

        self.GeklicktMagnitudeLineEdit = QtWidgets.QLineEdit(self.InformationenKoordinatenGroupBox)
        self.GeklicktMagnitudeLineEdit.setGeometry(QtCore.QRect(130, 300, 131, 31))
        self.GeklicktMagnitudeLineEdit.setMinimumSize(QtCore.QSize(101, 31))
        self.GeklicktMagnitudeLineEdit.setMaximumSize(QtCore.QSize(131, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.GeklicktMagnitudeLineEdit.setFont(font)
        self.GeklicktMagnitudeLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.GeklicktMagnitudeLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.GeklicktMagnitudeLineEdit.setReadOnly(True)
        self.GeklicktMagnitudeLineEdit.setPalette(palette)
        self.GeklicktMagnitudeLineEdit.setObjectName("GeklicktMagnitudeLineEdit")

        self.GeklicktMagnitudeLabel = QtWidgets.QLabel(self.InformationenKoordinatenGroupBox)
        self.GeklicktMagnitudeLabel.setGeometry(QtCore.QRect(20, 300, 101, 31))
        self.GeklicktMagnitudeLabel.setMinimumSize(QtCore.QSize(101, 31))
        self.GeklicktMagnitudeLabel.setMaximumSize(QtCore.QSize(101, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.GeklicktMagnitudeLabel.setFont(font)
        self.GeklicktMagnitudeLabel.setObjectName("GeklicktMagnitudeLabel")

        self.GeklicktLabel = QtWidgets.QLabel(self.InformationenKoordinatenGroupBox)
        self.GeklicktLabel.setGeometry(QtCore.QRect(10, 200, 81, 31))
        self.GeklicktLabel.setMinimumSize(QtCore.QSize(81, 31))
        self.GeklicktLabel.setMaximumSize(QtCore.QSize(81, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.GeklicktLabel.setFont(font)
        self.GeklicktLabel.setObjectName("GeklicktLabel")

        self.GeklicktFrequenzLabel = QtWidgets.QLabel(self.InformationenKoordinatenGroupBox)
        self.GeklicktFrequenzLabel.setGeometry(QtCore.QRect(20, 250, 91, 31))
        self.GeklicktFrequenzLabel.setMinimumSize(QtCore.QSize(91, 31))
        self.GeklicktFrequenzLabel.setMaximumSize(QtCore.QSize(91, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.GeklicktFrequenzLabel.setFont(font)
        self.GeklicktFrequenzLabel.setObjectName("GeklicktFrequenzLabel")

        self.GeklicktFrequenzLineEdit = QtWidgets.QLineEdit(self.InformationenKoordinatenGroupBox)
        self.GeklicktFrequenzLineEdit.setGeometry(QtCore.QRect(130, 250, 131, 31))
        self.GeklicktFrequenzLineEdit.setMinimumSize(QtCore.QSize(101, 31))
        self.GeklicktFrequenzLineEdit.setMaximumSize(QtCore.QSize(131, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.GeklicktFrequenzLineEdit.setFont(font)
        self.GeklicktFrequenzLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.GeklicktFrequenzLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.GeklicktFrequenzLineEdit.setReadOnly(True)
        self.GeklicktFrequenzLineEdit.setPalette(palette)
        self.GeklicktFrequenzLineEdit.setObjectName("GeklicktFrequenzLineEdit")

        self.MousPositionLabel = QtWidgets.QLabel(self.InformationenKoordinatenGroupBox)
        self.MousPositionLabel.setGeometry(QtCore.QRect(20, 340, 281, 21))
        self.MousPositionLabel.setMinimumSize(QtCore.QSize(0, 21))
        self.MousPositionLabel.setMaximumSize(QtCore.QSize(611, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.MousPositionLabel.setFont(font)
        self.MousPositionLabel.setText("")
        self.MousPositionLabel.setObjectName("MousPositionLabel")

        self.ButtonFrame = QtWidgets.QFrame(TestWindow)
        self.ButtonFrame.setGeometry(QtCore.QRect(-1, 0, 1611, 51))
        self.ButtonFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ButtonFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ButtonFrame.setObjectName("ButtonFrame")

        self.OpenFilePushButton = QtWidgets.QToolButton(self.ButtonFrame)
        self.OpenFilePushButton.setGeometry(QtCore.QRect(20, 10, 31, 31))
        self.OpenFilePushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon_materials/13.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.OpenFilePushButton.setIcon(icon1)
        self.OpenFilePushButton.setIconSize(QtCore.QSize(31, 31))
        self.OpenFilePushButton.setAutoRaise(True)
        self.OpenFilePushButton.setObjectName("OpenFilePushButton")

        self.PrintPushButton = QtWidgets.QToolButton(self.ButtonFrame)
        self.PrintPushButton.setGeometry(QtCore.QRect(60, 10, 31, 31))
        self.PrintPushButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon_materials/19.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.PrintPushButton.setIcon(icon2)
        self.PrintPushButton.setIconSize(QtCore.QSize(31, 31))
        self.PrintPushButton.setAutoRaise(True)
        self.PrintPushButton.setObjectName("PrintPushButton")

        self.HandMovePushButton = QtWidgets.QToolButton(self.ButtonFrame)
        self.HandMovePushButton.setGeometry(QtCore.QRect(120, 10, 31, 31))
        self.HandMovePushButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icon_materials/28.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.HandMovePushButton.setIcon(icon3)
        self.HandMovePushButton.setIconSize(QtCore.QSize(31, 31))
        self.HandMovePushButton.setAutoRaise(True)
        self.HandMovePushButton.setObjectName("HandMovePushButton")

        self.pushButton_4 = QtWidgets.QToolButton(self.ButtonFrame)
        self.pushButton_4.setGeometry(QtCore.QRect(160, 10, 31, 31))
        self.pushButton_4.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icon_materials/29.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.pushButton_4.setIcon(icon4)
        self.pushButton_4.setIconSize(QtCore.QSize(31, 31))
        self.pushButton_4.setAutoRaise(True)
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QToolButton(self.ButtonFrame)
        self.pushButton_5.setGeometry(QtCore.QRect(200, 10, 31, 31))
        self.pushButton_5.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icon_materials/30.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.pushButton_5.setIcon(icon5)
        self.pushButton_5.setIconSize(QtCore.QSize(31, 31))
        self.pushButton_5.setAutoRaise(True)
        self.pushButton_5.setObjectName("pushButton_5")

        self.Line2 = QtWidgets.QFrame(self.ButtonFrame)
        self.Line2.setGeometry(QtCore.QRect(100, 5, 16, 41))
        self.Line2.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        self.Line2.setFrameShape(QtWidgets.QFrame.VLine)
        self.Line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Line2.setObjectName("Line2")

        self.Line1 = QtWidgets.QFrame(self.ButtonFrame)
        self.Line1.setGeometry(QtCore.QRect(5, 5, 3, 41))
        self.Line1.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        self.Line1.setLineWidth(1)
        self.Line1.setFrameShape(QtWidgets.QFrame.VLine)
        self.Line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Line1.setObjectName("Line1")

        self.line3 = QtWidgets.QFrame(self.ButtonFrame)
        self.line3.setGeometry(QtCore.QRect(240, 5, 3, 41))
        self.line3.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        self.line3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line3.setObjectName("line3")

        self.pushButton_6 = QtWidgets.QToolButton(self.ButtonFrame)
        self.pushButton_6.setGeometry(QtCore.QRect(250, 10, 31, 31))
        self.pushButton_6.setMinimumSize(QtCore.QSize(31, 31))
        self.pushButton_6.setMaximumSize(QtCore.QSize(31, 31))
        self.pushButton_6.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icon_materials/20.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.pushButton_6.setIcon(icon6)
        self.pushButton_6.setIconSize(QtCore.QSize(31, 31))
        self.pushButton_6.setAutoRaise(True)
        self.pushButton_6.setObjectName("pushButton_6")

        self.pushButton_7 = QtWidgets.QToolButton(self.ButtonFrame)
        self.pushButton_7.setGeometry(QtCore.QRect(290, 10, 31, 31))
        self.pushButton_7.setMinimumSize(QtCore.QSize(31, 31))
        self.pushButton_7.setMaximumSize(QtCore.QSize(31, 31))
        self.pushButton_7.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icon_materials/31.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.pushButton_7.setIcon(icon7)
        self.pushButton_7.setIconSize(QtCore.QSize(31, 31))
        self.pushButton_7.setAutoRaise(True)
        self.pushButton_7.setObjectName("pushButton_7")

        self.line4 = QtWidgets.QFrame(TestWindow)
        self.line4.setGeometry(QtCore.QRect(-3, 40, 1621, 20))
        self.line4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line4.setObjectName("line4")

        self.TestKontrollenGroupBox = QtWidgets.QGroupBox(TestWindow)
        self.TestKontrollenGroupBox.setGeometry(QtCore.QRect(1250, 619, 331, 221))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.TestKontrollenGroupBox.setFont(font)
        self.TestKontrollenGroupBox.setObjectName("TestKontrollenGroupBox")

        self.TestStratButton = QtWidgets.QToolButton(self.TestKontrollenGroupBox)
        self.TestStratButton.setGeometry(QtCore.QRect(30, 30, 71, 71))
        self.TestStratButton.setText("")
        self.TestStratButton.setIcon(icon)
        self.TestStratButton.setIconSize(QtCore.QSize(61, 61))
        self.TestStratButton.setAutoRaise(True)
        #self.TestStratButton.setStyleSheet("color:rgb({},{},{},255)".format(0, 0, 0))
        self.TestStratButton.setObjectName("TestStratButton")

        self.TestPausePushButton = QtWidgets.QToolButton(self.TestKontrollenGroupBox)
        self.TestPausePushButton.setGeometry(QtCore.QRect(130, 30, 71, 71))
        self.TestPausePushButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icon_materials/18.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.TestPausePushButton.setIcon(icon4)
        self.TestPausePushButton.setIconSize(QtCore.QSize(61, 61))
        self.TestPausePushButton.setAutoRaise(True)
        self.TestPausePushButton.setObjectName("TestPausePushButton")

        self.TestStopPushButton = QtWidgets.QToolButton(self.TestKontrollenGroupBox)
        self.TestStopPushButton.setGeometry(QtCore.QRect(230, 30, 71, 71))
        self.TestStopPushButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icon_materials/21.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.TestStopPushButton.setIcon(icon5)
        self.TestStopPushButton.setIconSize(QtCore.QSize(61, 61))
        self.TestStopPushButton.setAutoRaise(True)
        self.TestStopPushButton.setObjectName("TestStopPushButton")

        self.TestStartButtonLabel = QtWidgets.QLabel(self.TestKontrollenGroupBox)
        self.TestStartButtonLabel.setGeometry(QtCore.QRect(42, 100, 51, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.TestStartButtonLabel.setFont(font)
        #self.TestStratButton.setEnabled(False)
        self.TestStartButtonLabel.setObjectName("TestStartButtonLabel")

        self.TestPauseButtonLabel = QtWidgets.QLabel(self.TestKontrollenGroupBox)
        self.TestPauseButtonLabel.setGeometry(QtCore.QRect(140, 100, 55, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.TestPauseButtonLabel.setFont(font)
        self.TestPauseButtonLabel.setObjectName("TestPauseButtonLabel")

        self.TestStopButtonLabel = QtWidgets.QLabel(self.TestKontrollenGroupBox)
        self.TestStopButtonLabel.setGeometry(QtCore.QRect(244, 100, 44, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.TestStopButtonLabel.setFont(font)
        self.TestStopButtonLabel.setObjectName("TestStopButtonLabel")

        self.DatenExportierenToolButton = QtWidgets.QToolButton(self.TestKontrollenGroupBox)
        self.DatenExportierenToolButton.setGeometry(QtCore.QRect(30, 130, 271, 31))
        self.DatenExportierenToolButton.setMinimumSize(QtCore.QSize(271, 31))
        self.DatenExportierenToolButton.setMaximumSize(QtCore.QSize(271, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.DatenExportierenToolButton.setFont(font)
        self.DatenExportierenToolButton.setObjectName("DatenExportierenToolButton")
        self.DatenExportierenToolButton.setEnabled(False)

        self.StatusFrames = QtWidgets.QFrame(TestWindow)
        self.StatusFrames.setGeometry(QtCore.QRect(29, 610, 1191, 241))
        self.StatusFrames.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.StatusFrames.setFrameShadow(QtWidgets.QFrame.Raised)
        self.StatusFrames.setObjectName("StatusFrames")

        self.StatusProgressBar = QtWidgets.QProgressBar(self.StatusFrames)
        self.StatusProgressBar.setGeometry(QtCore.QRect(10, 40, 1181, 23))
        self.StatusProgressBar.setProperty("value", 0)
        self.StatusProgressBar.setObjectName("StatusProgressBar")

        self.TestStatusLabel = QtWidgets.QLabel(self.StatusFrames)
        self.TestStatusLabel.setGeometry(QtCore.QRect(10, 5, 361, 31))
        self.TestStatusLabel.setObjectName("TestStatusLabel")

        self.KurvenoperationGroupBox = QtWidgets.QGroupBox(self.StatusFrames)
        self.KurvenoperationGroupBox.setGeometry(QtCore.QRect(0, 70, 311, 161))
        self.KurvenoperationGroupBox.setObjectName("KurvenoperationGroupBox")

        self.KurvenauswahlGroupBox = QtWidgets.QGroupBox(self.KurvenoperationGroupBox)
        self.KurvenauswahlGroupBox.setGeometry(QtCore.QRect(10, 30, 291, 71))
        self.KurvenauswahlGroupBox.setObjectName("KurvenauswahlGroupBox")

        self.EchtzeitKurve = QtWidgets.QRadioButton(self.KurvenauswahlGroupBox)
        self.EchtzeitKurve.setGeometry(QtCore.QRect(10, 30, 151, 27))
        self.EchtzeitKurve.setChecked(True)
        self.EchtzeitKurve.setObjectName("EchtzeitKurve")

        self.NormKurve = QtWidgets.QRadioButton(self.KurvenauswahlGroupBox)
        self.NormKurve.setGeometry(QtCore.QRect(160, 30, 121, 27))
        self.NormKurve.setObjectName("NormKurve")

        self.KurvenLinientypLabel = QtWidgets.QLabel(self.KurvenoperationGroupBox)
        self.KurvenLinientypLabel.setGeometry(QtCore.QRect(20, 115, 91, 31))
        self.KurvenLinientypLabel.setObjectName("KurvenLinientypLabel")

        self.KurvenLinientyp = QtWidgets.QComboBox(self.KurvenoperationGroupBox)
        self.KurvenLinientyp.setGeometry(QtCore.QRect(170, 115, 131, 31))
        self.KurvenLinientyp.setObjectName("KurvenLinientyp")
        self.KurvenLinientyp.clear()
        self.KurvenLinientyp.addItem("Keine", 0)
        self.KurvenLinientyp.addItem("Uni", 1)
        self.KurvenLinientyp.addItem("Strich", 2)
        self.KurvenLinientyp.setCurrentIndex(1)
        self.KurvenLinientyp.setStyleSheet("background-color: white")

        self.KurveDiagramm = QtWidgets.QTableWidget(self.StatusFrames)
        self.KurveDiagramm.setGeometry(QtCore.QRect(330, 80, 851, 151))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.KurveDiagramm.setFont(font)
        self.KurveDiagramm.setShowGrid(True)
        self.KurveDiagramm.setObjectName("KurveDiagramm")
        self.KurveDiagramm.setColumnCount(6)
        self.KurveDiagramm.setRowCount(4)
        self.KurveDiagramm.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.KurveDiagramm.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.KurveDiagramm.verticalHeader().setVisible(False)
        self.curve1 = QtWidgets.QRadioButton()
        self.curve1.setObjectName("curve1")
        self.curve1.setText("  1. Kurve  ")
        self.curve2 = QtWidgets.QRadioButton()
        self.curve2.setObjectName("curve2")
        self.curve2.setText("  2. Kurve  ")
        self.curve3 = QtWidgets.QRadioButton()
        self.curve3.setObjectName("curve3")
        self.curve3.setText("  3. Kurve  ")
        self.curve4 = QtWidgets.QRadioButton()
        self.curve4.setObjectName("curve4")
        self.curve4.setText("  4. Kurve  ")
        self.KurveDiagramm.setCellWidget(0, 0, self.curve1)
        self.KurveDiagramm.setCellWidget(1, 0, self.curve2)
        self.KurveDiagramm.setCellWidget(2, 0, self.curve3)
        self.KurveDiagramm.setCellWidget(3, 0, self.curve4)
        fontde = QtGui.QFont()
        fontde.setFamily("Verdana")
        fontde.setPointSize(10)
        self.detektor1 = QtWidgets.QComboBox()
        self.detektor1.setFont(fontde)
        self.detektor1.addItems(['Max. Peak', 'Ave. Peak', 'Quasi Peak'])
        self.detektor1.setCurrentIndex(0)
        self.detektor1.setObjectName('detektor1')
        self.detektor1.setStyleSheet("background-color: white")
        self.detektor2 = QtWidgets.QComboBox()
        self.detektor2.setFont(fontde)
        self.detektor2.addItems(['Max. Peak', 'Ave. Peak', 'Quasi Peak'])
        self.detektor2.setCurrentIndex(1)
        self.detektor2.setObjectName('detektor2')
        self.detektor2.setStyleSheet("background-color: white")
        self.detektor3 = QtWidgets.QComboBox()
        self.detektor3.setFont(fontde)
        self.detektor3.addItems(['Max. Peak', 'Ave. Peak', 'Quasi Peak'])
        self.detektor3.setCurrentIndex(2)
        self.detektor3.setObjectName('detektor3')
        self.detektor3.setStyleSheet("background-color: white")
        self.detektor4 = QtWidgets.QComboBox()
        self.detektor4.setFont(fontde)
        self.detektor4.addItems(['Max. Peak', 'Ave. Peak', 'Quasi Peak'])
        self.detektor4.setObjectName('detektor4')
        self.detektor4.setStyleSheet("background-color: white")
        self.KurveDiagramm.setCellWidget(0, 1, self.detektor1)
        self.KurveDiagramm.setCellWidget(1, 1, self.detektor2)
        self.KurveDiagramm.setCellWidget(2, 1, self.detektor3)
        self.KurveDiagramm.setCellWidget(3, 1, self.detektor4)

        self.antten1 = QtWidgets.QLineEdit()
        self.antten1.setValidator(QtGui.QIntValidator())
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.antten1.setFont(font)
        self.antten1.setAcceptDrops(False)
        self.antten1.setMaxLength(2)
        self.antten1.setClearButtonEnabled(True)
        self.antten1.setToolTip("Bitte Integral hier eingeben.")
        self.antten1.setObjectName("antten1")
        self.antten1.setPlaceholderText("Standardwert: 10")
        self.antten1.setAlignment(QtCore.Qt.AlignCenter)
        self.KurveDiagramm.setCellWidget(0, 2, self.antten1)

        self.antten2 = QtWidgets.QLineEdit()
        self.antten2.setValidator(QtGui.QIntValidator())
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.antten2.setFont(font)
        self.antten2.setAcceptDrops(False)
        self.antten2.setMaxLength(2)
        self.antten2.setClearButtonEnabled(True)
        self.antten2.setToolTip("Bitte Integral hier eingeben.")
        self.antten2.setObjectName("antten2")
        self.antten2.setPlaceholderText("Standardwert: 10")
        self.antten2.setAlignment(QtCore.Qt.AlignCenter)
        self.KurveDiagramm.setCellWidget(1, 2, self.antten2)

        self.antten3 = QtWidgets.QLineEdit()
        self.antten3.setValidator(QtGui.QIntValidator())
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.antten3.setFont(font)
        self.antten3.setAcceptDrops(False)
        self.antten3.setMaxLength(2)
        self.antten3.setClearButtonEnabled(True)
        self.antten3.setToolTip("Bitte Integral hier eingeben.")
        self.antten3.setObjectName("antten1")
        self.antten3.setPlaceholderText("Standardwert: 10")
        self.antten3.setAlignment(QtCore.Qt.AlignCenter)
        self.KurveDiagramm.setCellWidget(2, 2, self.antten3)

        self.antten4 = QtWidgets.QLineEdit()
        self.antten4.setValidator(QtGui.QIntValidator())
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.antten4.setFont(font)
        self.antten4.setAcceptDrops(False)
        self.antten4.setMaxLength(2)
        self.antten4.setClearButtonEnabled(True)
        self.antten4.setToolTip("Bitte Integral hier eingeben.")
        self.antten4.setObjectName("antten4")
        self.antten4.setPlaceholderText("Standardwert: 10")
        self.antten4.setAlignment(QtCore.Qt.AlignCenter)
        self.KurveDiagramm.setCellWidget(3, 2, self.antten4)

        self.messtime1 = QtWidgets.QLineEdit()
        self.messtime1.setValidator(QtGui.QIntValidator())
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.messtime1.setFont(font)
        self.messtime1.setAcceptDrops(False)
        self.messtime1.setMaxLength(2)
        self.messtime1.setClearButtonEnabled(True)
        self.messtime1.setToolTip("Bitte Integral hier eingeben.")
        self.messtime1.setObjectName("messtime1")
        self.messtime1.setPlaceholderText("Standardwert: 50")
        self.messtime1.setAlignment(QtCore.Qt.AlignCenter)
        self.KurveDiagramm.setCellWidget(0, 3, self.messtime1)

        self.messtime2 = QtWidgets.QLineEdit()
        self.messtime2.setValidator(QtGui.QIntValidator())
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.messtime2.setFont(font)
        self.messtime2.setAcceptDrops(False)
        self.messtime2.setMaxLength(2)
        self.messtime2.setClearButtonEnabled(True)
        self.messtime2.setToolTip("Bitte Integral hier eingeben.")
        self.messtime2.setObjectName("messtime2")
        self.messtime2.setPlaceholderText("Standardwert: 50")
        self.messtime2.setAlignment(QtCore.Qt.AlignCenter)
        self.KurveDiagramm.setCellWidget(1, 3, self.messtime2)

        self.messtime3 = QtWidgets.QLineEdit()
        self.messtime3.setValidator(QtGui.QIntValidator())
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.messtime3.setFont(font)
        self.messtime3.setAcceptDrops(False)
        self.messtime3.setMaxLength(2)
        self.messtime3.setClearButtonEnabled(True)
        self.messtime3.setToolTip("Bitte Integral hier eingeben.")
        self.messtime3.setObjectName("messtime3")
        self.messtime3.setPlaceholderText("Standardwert: 50")
        self.messtime3.setAlignment(QtCore.Qt.AlignCenter)
        self.KurveDiagramm.setCellWidget(2, 3, self.messtime3)

        self.messtime4 = QtWidgets.QLineEdit()
        self.messtime4.setValidator(QtGui.QIntValidator())
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.messtime4.setFont(font)
        self.messtime4.setAcceptDrops(False)
        self.messtime4.setMaxLength(2)
        self.messtime4.setClearButtonEnabled(True)
        self.messtime4.setToolTip("Bitte Integral hier eingeben.")
        self.messtime4.setObjectName("messtime4")
        self.messtime4.setPlaceholderText("Standardwert: 50")
        self.messtime4.setAlignment(QtCore.Qt.AlignCenter)
        self.KurveDiagramm.setCellWidget(3, 3, self.messtime4)

        self.startfre1 = QtWidgets.QLineEdit()
        self.startfre1.setValidator(QtGui.QIntValidator())
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.startfre1.setFont(font)
        self.startfre1.setAcceptDrops(False)
        self.startfre1.setMaxLength(4)
        self.startfre1.setClearButtonEnabled(True)
        self.startfre1.setToolTip("Bitte Integral hier eingeben.")
        self.startfre1.setObjectName("startfre1")
        self.startfre1.setPlaceholderText("Standardwert: 150")
        self.startfre1.setAlignment(QtCore.Qt.AlignCenter)
        self.KurveDiagramm.setCellWidget(0, 4, self.startfre1)

        self.startfre2 = QtWidgets.QLineEdit()
        self.startfre2.setValidator(QtGui.QIntValidator())
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.startfre2.setFont(font)
        self.startfre2.setAcceptDrops(False)
        self.startfre2.setMaxLength(4)
        self.startfre2.setClearButtonEnabled(True)
        self.startfre2.setToolTip("Bitte Integral hier eingeben.")
        self.startfre2.setObjectName("startfre2")
        self.startfre2.setPlaceholderText("Standardwert: 150")
        self.startfre2.setAlignment(QtCore.Qt.AlignCenter)
        self.KurveDiagramm.setCellWidget(1, 4, self.startfre2)

        self.startfre3 = QtWidgets.QLineEdit()
        self.startfre3.setValidator(QtGui.QIntValidator())
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.startfre3.setFont(font)
        self.startfre3.setAcceptDrops(False)
        self.startfre3.setMaxLength(4)
        self.startfre3.setClearButtonEnabled(True)
        self.startfre3.setToolTip("Bitte Integral hier eingeben.")
        self.startfre3.setObjectName("startfre3")
        self.startfre3.setPlaceholderText("Standardwert: 150")
        self.startfre3.setAlignment(QtCore.Qt.AlignCenter)
        self.KurveDiagramm.setCellWidget(2, 4, self.startfre3)

        self.startfre4 = QtWidgets.QLineEdit()
        self.startfre4.setValidator(QtGui.QIntValidator())
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.startfre4.setFont(font)
        self.startfre4.setAcceptDrops(False)
        self.startfre4.setMaxLength(4)
        self.startfre4.setClearButtonEnabled(True)
        self.startfre4.setToolTip("Bitte Integral hier eingeben.")
        self.startfre4.setObjectName("startfre4")
        self.startfre4.setPlaceholderText("Standardwert: 150")
        self.startfre4.setAlignment(QtCore.Qt.AlignCenter)
        self.KurveDiagramm.setCellWidget(3, 4, self.startfre4)

        self.curvecolor1 = QtWidgets.QPushButton()
        self.curvecolor1.setAutoFillBackground(False)
        self.curvecolor1.setStyleSheet("background-color: rgb(255, 80, 80);")
        self.curvecolor1.setText("")
        self.curvecolor1.setFlat(False)
        self.curvecolor1.setObjectName("curvecolor1")
        self.KurveDiagramm.setCellWidget(0, 5, self.curvecolor1)

        self.curvecolor2 = QtWidgets.QPushButton()
        self.curvecolor2.setAutoFillBackground(False)
        self.curvecolor2.setStyleSheet("background-color: rgb(255, 192, 0);")
        self.curvecolor2.setText("")
        self.curvecolor2.setFlat(False)
        self.curvecolor2.setObjectName("curvecolor2")
        self.KurveDiagramm.setCellWidget(1, 5, self.curvecolor2)

        self.curvecolor3 = QtWidgets.QPushButton()
        self.curvecolor3.setAutoFillBackground(False)
        self.curvecolor3.setStyleSheet("background-color: rgb(0, 176, 80);")
        self.curvecolor3.setText("")
        self.curvecolor3.setFlat(False)
        self.curvecolor3.setObjectName("curvecolor3")
        self.KurveDiagramm.setCellWidget(2, 5, self.curvecolor3)

        self.curvecolor4 = QtWidgets.QPushButton()
        self.curvecolor4.setAutoFillBackground(False)
        self.curvecolor4.setStyleSheet("background-color: rgb(255, 0, 255);")
        self.curvecolor4.setText("")
        self.curvecolor4.setFlat(False)
        self.curvecolor4.setObjectName("curvecolor4")
        self.KurveDiagramm.setCellWidget(3, 5, self.curvecolor4)

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        item.setFont(font)
        self.KurveDiagramm.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        item.setFont(font)
        self.KurveDiagramm.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        item.setFont(font)
        self.KurveDiagramm.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        item.setFont(font)
        self.KurveDiagramm.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        item.setFont(font)
        self.KurveDiagramm.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        item.setFont(font)
        self.KurveDiagramm.setHorizontalHeaderItem(5, item)

        self.ReportGenerierenToolButton = QtWidgets.QToolButton(TestWindow)
        self.ReportGenerierenToolButton.setGeometry(QtCore.QRect(1280, 800, 271, 31))
        self.ReportGenerierenToolButton.setMinimumSize(QtCore.QSize(271, 31))
        self.ReportGenerierenToolButton.setMaximumSize(QtCore.QSize(271, 31))
        self.ReportGenerierenToolButton.setObjectName("ReportGenerierenToolButton")
        self.ReportGenerierenToolButton.setEnabled(False)

        self.retranslateUi(TestWindow)
        QtCore.QMetaObject.connectSlotsByName(TestWindow)
        # define signals
        self.curvecolor1.clicked.connect(self.KurvenLinenFarbe_clicked1)
        self.curvecolor2.clicked.connect(self.KurvenLinenFarbe_clicked2)
        self.curvecolor3.clicked.connect(self.KurvenLinenFarbe_clicked3)
        self.curvecolor4.clicked.connect(self.KurvenLinenFarbe_clicked4)
        self.OpenFilePushButton.clicked.connect(self.on_actOpen_triggered)
        self.PrintPushButton.clicked.connect(self.handle_print)
        self.HandMovePushButton.clicked.connect(self.on_actZoomIn_triggered)
        self.HandMovePushButton.clicked.connect(self.hide_line_labels)
        self.pushButton_4.clicked.connect(self.on_actZoomOut_triggered)
        self.pushButton_4.clicked.connect(self.hide_line_labels)
        self.pushButton_5.clicked.connect(self.on_actZoomReset_triggered)
        self.pushButton_5.clicked.connect(self.show_line_labels)
        self.TestStratButton.clicked.connect(self.start_thread)
        self.TestPausePushButton.clicked.connect(self.clicked_pause)
        self.TestStopPushButton.clicked.connect(self.clicked_stop)
        self.pushButton_7.clicked.connect(self._clearall)
        self.ReportGenerierenToolButton.clicked.connect(self.create_word_report)
        self.graphicsView.rubberBandChanged.connect(self.hide_line_labels)
        self.DatenExportierenToolButton.clicked.connect(self.daten_exportieren)

        # define the background color of the window
        pale = QtGui.QPalette()
        pale.setColor(QtGui.QPalette.Background, QtGui.QColor(248, 248, 248))
        TestWindow.setPalette(pale)

    def retranslateUi(self, TestWindow):
        _translate = QtCore.QCoreApplication.translate
        TestWindow.setWindowTitle(_translate("TestWindow", "Leitungsgebundene Emissionsmessung"))
        self.StatusleisteGroupBox.setTitle(_translate("TestWindow", "Statusleiste"))
        self.AktuellerZustandLabel.setText(_translate("TestWindow", "Aktueller Zustand:"))
        self.InformationenKoordinatenGroupBox.setTitle(_translate("TestWindow", "Informationen der Koordinaten"))
        self.GeschwebtFrequenzLabel.setText(_translate("TestWindow", "Frequenz:"))
        self.GeschwebtMagnitudeLabel.setText(_translate("TestWindow", "Magnitude:"))
        self.GeschwebtLabel.setText(_translate("TestWindow", "Geschwebt"))
        self.GeklicktMagnitudeLabel.setText(_translate("TestWindow", "Magnitude:"))
        self.GeklicktLabel.setText(_translate("TestWindow", "Geklickt"))
        self.GeklicktFrequenzLabel.setText(_translate("TestWindow", "Frequenz:"))
        self.pushButton_4.setText(_translate("TestWindow", "PushButton"))
        self.pushButton_5.setText(_translate("TestWindow", "PushButton"))
        self.TestKontrollenGroupBox.setTitle(_translate("TestWindow", "Testkontrollen"))
        self.TestStartButtonLabel.setText(_translate("TestWindow", "Start"))
        self.TestPauseButtonLabel.setText(_translate("TestWindow", "Pause"))
        self.TestStopButtonLabel.setText(_translate("TestWindow", "Stop"))
        self.DatenExportierenToolButton.setText(_translate("TestWindow", "Daten exportieren"))
        self.TestStatusLabel.setText(_translate("TestWindow", "Status: Leerlauf (01.01.2021 14:41:54)"))
        self.KurvenoperationGroupBox.setTitle(_translate("TestWindow", "Kurvenoperationen"))
        self.KurvenauswahlGroupBox.setTitle(_translate("TestWindow", "Kurvenauswahl"))
        self.EchtzeitKurve.setText(_translate("TestWindow", "Messkurve"))
        self.NormKurve.setText(_translate("TestWindow", "Grenzwerte"))
        self.KurvenLinientypLabel.setText(_translate("TestWindow", "Linientyp:"))
        item = self.KurveDiagramm.horizontalHeaderItem(0)
        item.setText(_translate("TestWindow", "Messkurve"))
        item = self.KurveDiagramm.horizontalHeaderItem(1)
        item.setText(_translate("TestWindow", "Detektor"))
        item = self.KurveDiagramm.horizontalHeaderItem(2)
        item.setText(_translate("TestWindow", "Attenuation / dB"))
        item = self.KurveDiagramm.horizontalHeaderItem(3)
        item.setText(_translate("TestWindow", "Messzeit / ms" ))
        item = self.KurveDiagramm.horizontalHeaderItem(4)
        item.setText(_translate("TestWindow", "Anfangsfrequenz / kHz"))
        item = self.KurveDiagramm.horizontalHeaderItem(5)
        item.setText(_translate("TestWindow", "Farbe"))
        self.ReportGenerierenToolButton.setText(_translate("TestWindow", "Report generieren"))
        self.GeklicktFrequenzLabel.setText(_translate("TestWindow", "Frequenz:"))
        self.GeklicktMagnitudeLabel.setText(_translate("TestWindow", "Magnitude:"))
        self.GeklicktLabel.setText(_translate("TestWindow", "Geklickt"))

    # clear all curve labels of marginal values (Grenzwerte)
    def _clearall(self):
        #self.chart.removeAllSeries()
        self.series_1.clear()
        self.series_2.clear()
        self.series_3.clear()
        self.series_4.clear()
        self.label1.hide()
        self.label2.hide()
        self.label3.hide()
        self.label4.hide()
        self.label5.hide()
        self.label6.hide()

    # when mouse is moving on a curve, the coordinates of the spot, where the mouse is pointing to, on the curve
    # will be showed in the Status bar
    def do_series_hovered(self, point, state):
        if state:
            horizontal_coor = "%.2f kHz" % point.x()
            vertical_coor = "%.2f dBμV/m" % point.y()
            self.GeschwebtFrequenzLineEdit.setText(horizontal_coor)
            self.GeschwebtMagnitudeLineEdit.setText(vertical_coor)

    # when mouse clicks a spot on a curve, the coordinates of the spot will be showed in the Status bar
    def do_series_clicked(self, point):
        horizontal_coor = "%.2f MHz" % point.x()
        vertical_coor = "%.2f dBμV/m" % point.y()
        self.GeklicktFrequenzLineEdit.setText(horizontal_coor)
        self.GeklicktMagnitudeLineEdit.setText(vertical_coor)

    # the current coordinates of the mouse will be showed continously in the status bar in real-time
    def do_chartView_mouseMove(self, point):
        pt = self.graphicsView.chart().mapToValue(point)
        self.MousPositionLabel.setText("Chart X=%.2f,Y=%.2f"%(pt.x(),pt.y()))

    # when the button "Pause" is clicked, the measuring process will take a break
    # at the same time, the status bar will show that the test process is in a pause
    def clicked_pause(self):
        self.calc.signal += 1                               # When pause is clicked, signal plus one
        #self.KurveDiagramm.setEnabled(False)
        if (self.calc.signal & 1) == 0:                     # signal is an even number, so stop the test and have a pause

            self.TestPausePushButton.setAutoRaise(False)
            self.DatenExportierenToolButton.setEnabled(True)
            self.ReportGenerierenToolButton.setEnabled(True)
            self.KurveDiagramm.setEnabled(False)
            # self.calc.quit()
            time.sleep(2)
            self.AktuellerZustandLineEdit.setText("Test unterbrochen! ")
        elif (self.calc.signal & 1) == 1:                   # signal is an odd number, so continue the test
            self.TestPausePushButton.setAutoRaise(True)
            self.AktuellerZustandLineEdit.setText("Test läuft!")
            self.KurveDiagramm.setEnabled(False)
            if self.curve1.isChecked() == True:
                if self.antten1.text() == "":
                    self.antten1.setText('10')
                if self.messtime1.text() == '':
                    self.messtime1.setText('50')
                '''if self.startfre1.text() == '':
                    self.startfre1.setText('150')'''
                antten = int(self.antten1.text())
                messtime = int(self.messtime1.text())
                # startfre = int(self.startfre1.text())
                self.color = self.curvecolor1.palette().button().color().name()
                r, g, b = color(self.color)
                pen = QtGui.QPen(QtGui.QColor(r, g, b))
                pen.setWidth(2)
                self.series_1.setPen(pen)
                if self.detektor1.currentText() == "Max. Peak":
                    mode = 'max'
                elif self.detektor1.currentText() == "Ave. Peak":
                    mode = 'average'
                elif self.detektor1.currentText() == "Quasi Peak":
                    mode = 'quasi'
            elif self.curve2.isChecked() == True:
                if self.antten2.text() == '':
                    self.antten2.setText('10')
                if self.messtime2.text() == '':
                    self.messtime2.setText('50')
                '''if self.startfre2.text() == '':
                    self.startfre2.setText('150')'''
                antten = int(self.antten2.text())
                messtime = int(self.messtime2.text())
                # startfre = int(self.startfre2.text())
                self.color = self.curvecolor2.palette().button().color().name()
                r, g, b = color(self.color)
                pen = QtGui.QPen(QtGui.QColor(r, g, b))
                pen.setWidth(2)
                self.series_2.setPen(pen)
                if self.detektor2.currentText() == "Max. Peak":
                    mode = 'max'
                elif self.detektor2.currentText() == "Ave. Peak":
                    mode = 'average'
                elif self.detektor2.currentText() == "Quasi Peak":
                    mode = 'quasi'
            elif self.curve3.isChecked() == True:
                if self.antten3.text() == '':
                    self.antten3.setText('10')
                if self.messtime3.text() == '':
                    self.messtime3.setText('50')
                if self.startfre3.text() == '':
                    self.startfre3.setText('150')
                antten = int(self.antten3.text())
                messtime = int(self.messtime3.text())
                # startfre = int(self.startfre3.text())
                self.color = self.curvecolor3.palette().button().color().name()
                r, g, b = color(self.color)
                pen = QtGui.QPen(QtGui.QColor(r, g, b))
                pen.setWidth(2)
                self.series_3.setPen(pen)
                if self.detektor3.currentText() == "Max. Peak":
                    mode = 'max'
                elif self.detektor3.currentText() == "Ave. Peak":
                    mode = 'average'
                elif self.detektor3.currentText() == "Quasi Peak":
                    mode = 'quasi'
            elif self.curve4.isChecked() == True:
                if self.antten4.text() == '':
                    self.antten4.setText('10')
                if self.messtime4.text() == '':
                    self.messtime4.setText('50')
                '''if self.startfre4.text() == '':
                    self.startfre4.setText('150')'''
                antten = int(self.antten4.text())
                messtime = int(self.messtime4.text())
                # startfre = int(self.startfre4.text())
                self.color = self.curvecolor4.palette().button().color().name()
                r, g, b = color(self.color)
                pen = QtGui.QPen(QtGui.QColor(r, g, b))
                pen.setWidth(2)
                self.series_4.setPen(pen)
                if self.detektor4.currentText() == "Max. Peak":
                    mode = 'max'
                elif self.detektor4.currentText() == "Ave. Peak":
                    mode = 'average'
                elif self.detektor4.currentText() == "Quasi Peak":
                    mode = 'quasi'
            self.TestStatusLabel.setText("Status: %s (%s)" % (
                self.AktuellerZustandLineEdit.text(), time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())))
            self.calc = External(mode=mode, attenuation=antten, messtime=messtime, startfre=self.calc.startfrequency)   # continue testing from the pause frequency
            self.calc.signal = 1
            self.calc.countChanged.connect(self.onCountChanged)
            self.calc.start()


    # when the button "Stop" is clicked, the test process stops immediately
    # at the same time, the status bar will show that the test process is over/done
    def clicked_stop(self):
        self.calc.signal += 1                 # When Stop is clicked, signal plus one. With the code in the thread_LE to determine the Signal, the test can be stopped.
        self.TestStratButton.setEnabled(True)
        self.KurveDiagramm.setEnabled(True)
        self.AktuellerZustandLineEdit.setText("Test Stop! ")

    # connected to the device driver
    # once the button "Start" is clicked, the test process will begin
    def start_thread(self):

        if self.curve1.isChecked() == False and \
                self.curve2.isChecked() == False and \
                self.curve3.isChecked() == False and \
                self.curve4.isChecked() == False:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Bitte Achtung')
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
            messageBox.setText(
                'Bitte GPIB0:20:INSTR ESPI Messempfänger verbinden !')
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
            buttonY.setText('Ok')
            messageBox.exec_()
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Kurvenauswahl')
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
            messageBox.setText(
                'Bitte wählen Sie zuerst eine Kurve aus!')
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
            buttonY.setText('Ok')
            messageBox.exec_()
        else:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Bitte Achtung')
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
            messageBox.setText(
                'Bitte Impulsbegrenzer verwenden !')
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
            buttonY.setText('Ok')
            messageBox.exec_()
            self.AktuellerZustandLineEdit.setText("Test läuft!")
            self.KurveDiagramm.setEnabled(False)
            self.TestStratButton.setEnabled(False)
            if self.curve1.isChecked() == True:
                if self.antten1.text() == "":
                    self.antten1.setText('10')
                    print(self.antten1.text)
                if self.messtime1.text() == '':
                    self.messtime1.setText('50')
                if self.startfre1.text() == '':
                    self.startfre1.setText('150')
                antten = int(self.antten1.text())
                messtime = int(self.messtime1.text())
                startfre = int(self.startfre1.text())
                self.color = self.curvecolor1.palette().button().color().name()
                r,g,b = color(self.color)
                pen = QtGui.QPen(QtGui.QColor(r,g,b))
                pen.setWidth(2)
                self.series_1.setPen(pen)
                if self.detektor1.currentText() == "Max. Peak":
                    mode = 'max'
                elif self.detektor1.currentText() == "Ave. Peak":
                    mode = 'average'
                elif self.detektor1.currentText() == "Quasi Peak":
                    mode = 'quasi'
            elif self.curve2.isChecked() == True:
                if self.antten2.text() == '':
                    self.antten2.setText('10')
                if self.messtime2.text() == '':
                    self.messtime2.setText('50')
                if self.startfre2.text() == '':
                    self.startfre2.setText('150')
                antten = int(self.antten2.text())
                messtime = int(self.messtime2.text())
                startfre = int(self.startfre2.text())
                self.color = self.curvecolor2.palette().button().color().name()
                r,g,b = color(self.color)
                pen = QtGui.QPen(QtGui.QColor(r,g,b))
                pen.setWidth(2)
                self.series_2.setPen(pen)
                if self.detektor2.currentText() == "Max. Peak":
                    mode = 'max'
                elif self.detektor2.currentText() == "Ave. Peak":
                    mode = 'average'
                elif self.detektor2.currentText() == "Quasi Peak":
                    mode = 'quasi'
            elif self.curve3.isChecked() == True:
                if self.antten3.text() == '':
                    self.antten3.setText('10')
                if self.messtime3.text() == '':
                    self.messtime3.setText('50')
                if self.startfre3.text() == '':
                    self.startfre3.setText('150')
                antten = int(self.antten3.text())
                messtime = int(self.messtime3.text())
                startfre = int(self.startfre3.text())
                self.color = self.curvecolor3.palette().button().color().name()
                r,g,b = color(self.color)
                pen = QtGui.QPen(QtGui.QColor(r,g,b))
                pen.setWidth(2)
                self.series_3.setPen(pen)
                if self.detektor3.currentText() == "Max. Peak":
                    mode = 'max'
                elif self.detektor3.currentText() == "Ave. Peak":
                    mode = 'average'
                elif self.detektor3.currentText() == "Quasi Peak":
                    mode = 'quasi'
            elif self.curve4.isChecked() == True:
                if self.antten4.text() == '':
                    self.antten4.setText('10')
                if self.messtime4.text() == '':
                    self.messtime4.setText('50')
                if self.startfre4.text() == '':
                    self.startfre4.setText('150')
                antten = int(self.antten4.text())
                messtime = int(self.messtime4.text())
                startfre = int(self.startfre4.text())
                self.color = self.curvecolor4.palette().button().color().name()
                r,g,b = color(self.color)
                pen = QtGui.QPen(QtGui.QColor(r,g,b))
                pen.setWidth(2)
                self.series_4.setPen(pen)
                if self.detektor4.currentText() == "Max. Peak":
                    mode = 'max'
                elif self.detektor4.currentText() == "Ave. Peak":
                    mode = 'average'
                elif self.detektor4.currentText() == "Quasi Peak":
                    mode = 'quasi'
            self.TestStatusLabel.setText("Status: %s (%s)" % (self.AktuellerZustandLineEdit.text(),time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())))
            self.calc = External(mode=mode, attenuation=antten, messtime=messtime, startfre=startfre)
            self.calc.signal=1
            self.calc.countChanged.connect(self.onCountChanged)
            self.calc.start()

    # Export measurement data.
    def daten_exportieren(self):
        if self.curve1.isChecked() == False and \
                self.curve2.isChecked() == False and \
                self.curve3.isChecked() == False and \
                self.curve4.isChecked() == False:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Kurvenauswahl')
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
            messageBox.setText(
                'Bitte wählen Sie zuerst eine Kurve aus!')
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
            buttonY.setText('Ok')
            messageBox.exec_()
        else:
            if self.curve1.isChecked() == True and self.series_1 is not None:
                fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, 'Messergebnisse speichern', 'd:\\',
                                                                    'Ergebnisse (*.txt)')
                f = open(fileName, "a")
                detektor = self.detektor1.currentText()
                f.write('Detektor: %s' % detektor)
                f.write('\t')
                attenuation = self.antten1.text()
                f.write('Attenuation: %s dB' % attenuation)
                f.write('\t')
                messtime = self.messtime1.text()
                f.write('Messzeit: %s ms' % messtime)
                f.write('\t')
                Startfre = self.startfre1.text()
                f.write('Startfrequenz: %s MHz' % Startfre)
                f.write('\n')
                f.write('Frequenz: MHz')
                f.write('\t')
                f.write('Feldstärke: dBuV/m')
                f.write('\n')
                for fre, mag in self.series_1:
                    f.write(fre)
                    f.write('\t')
                    f.write(mag)
                    f.write('\n')
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Hinweis')
                messageBox.setIcon(QtWidgets.QMessageBox.Information)
                messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/3.png'))
                messageBox.setText('Die Daten werden erfolgreich exportiert!')
                messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                buttonY.setText('Ok')
                messageBox.exec_()
            elif self.curve2.isChecked() == True and self.series_2 is not None:
                fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, 'Messergebnisse speichern', 'd:\\',
                                                                    'Ergebnisse (*.txt)')
                f = open(fileName, "a")
                detektor = self.detektor2.currentText()
                f.write('Detektor: %s' % detektor)
                f.write('\t')
                attenuation = self.antten2.text()
                f.write('Attenuation: %s dB' % attenuation)
                f.write('\t')
                messtime = self.messtime2.text()
                f.write('Messzeit: %s ms' % messtime)
                f.write('\t')
                Startfre = self.startfre2.text()
                f.write('Startfrequenz: %s MHz' % Startfre)
                f.write('\n')
                f.write('Frequenz: MHz')
                f.write('\t')
                f.write('Feldstärke: dBuV/m')
                f.write('\n')
                for fre, mag in self.series_2:
                    f.write(fre)
                    f.write('\t')
                    f.write(mag)
                    f.write('\n')
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Hinweis')
                messageBox.setIcon(QtWidgets.QMessageBox.Information)
                messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/3.png'))
                messageBox.setText('Die Daten werden erfolgreich exportiert!')
                messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                buttonY.setText('Ok')
                messageBox.exec_()

            elif self.curve3.isChecked() == True and self.series_3 is not None:
                fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, 'Messergebnisse speichern', 'd:\\',
                                                                    'Ergebnisse (*.txt)')
                f = open(fileName, "a")
                detektor = self.detektor3.currentText()
                f.write('Detektor: %s' % detektor)
                f.write('\t')
                attenuation = self.antten3.text()
                f.write('Attenuation: %s dB' % attenuation)
                f.write('\t')
                messtime = self.messtime3.text()
                f.write('Messzeit: %s ms' % messtime)
                f.write('\t')
                Startfre = self.startfre3.text()
                f.write('Startfrequenz: %s MHz' % Startfre)
                f.write('\n')
                f.write('Frequenz: MHz')
                f.write('\t')
                f.write('Feldstärke: dBuV/m')
                f.write('\n')
                for fre, mag in self.series_3:
                    f.write(fre)
                    f.write('\t')
                    f.write(mag)
                    f.write('\n')
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Hinweis')
                messageBox.setIcon(QtWidgets.QMessageBox.Information)
                messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/3.png'))
                messageBox.setText('Die Daten werden erfolgreich exportiert!')
                messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                buttonY.setText('Ok')
                messageBox.exec_()
            elif self.curve4.isChecked() == True and self.series_4 is not None:
                fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, 'Messergebnisse speichern', 'd:\\',
                                                                    'Ergebnisse (*.txt)')
                f = open(fileName, "a")
                detektor = self.detektor4.currentText()
                f.write('Detektor: %s' % detektor)
                f.write('\t')
                attenuation = self.antten4.text()
                f.write('Attenuation: %s dB' % attenuation)
                f.write('\t')
                messtime = self.messtime4.text()
                f.write('Messzeit: %s ms' % messtime)
                f.write('\t')
                Startfre = self.startfre4.text()
                f.write('Startfrequenz: %s MHz' % Startfre)
                f.write('\n')
                f.write('Frequenz: MHz')
                f.write('\t')
                f.write('Feldstärke: dBuV/m')
                f.write('\n')
                for fre, mag in self.series_4:
                    f.write(fre)
                    f.write('\t')
                    f.write(mag)
                    f.write('\n')
                messageBox = QtWidgets.QMessageBox()
                messageBox.setWindowTitle('Hinweis')
                messageBox.setIcon(QtWidgets.QMessageBox.Information)
                messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/3.png'))
                messageBox.setText('Die Daten werden erfolgreich exportiert!')
                messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
                buttonY.setText('Ok')
                messageBox.exec_()

    # by clicking the "Report generieren" button, a test report will be generated automatically
    def create_word_report(self):
        pix = self.graphicsView.grab()
        image = pix.toImage()
        image = qimage2ndarray.rgb_view(image, byteorder='little')
        savepath = 'D:/demo.png'
        cv.imwrite(savepath, image)
        WordReportGenerator.generate_word(savepath)
        #os.remove(savepath)
        messageBox = QtWidgets.QMessageBox()
        messageBox.setWindowTitle('Report')
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
        messageBox.setText('Der Word-Report wird erfolgreich generiert!')
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
        buttonY.setText('Ok')
        messageBox.exec_()

    # change the color of the 1. curve
    def KurvenLinenFarbe_clicked1(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            qss = "background-color: rgb(%d, %d, %d);" % (
                color.red(), color.green(), color.blue())
            self.curvecolor1.setStyleSheet(qss)

    # change the color of the 2. curve
    def KurvenLinenFarbe_clicked2(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            qss = "background-color: rgb(%d, %d, %d);" % (
                color.red(), color.green(), color.blue())
            self.curvecolor2.setStyleSheet(qss)

    # change the color of the 3. curve
    def KurvenLinenFarbe_clicked3(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            qss = "background-color: rgb(%d, %d, %d);" % (
                color.red(), color.green(), color.blue())
            self.curvecolor3.setStyleSheet(qss)

    # change the color of the 4. curve
    def KurvenLinenFarbe_clicked4(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            qss = "background-color: rgb(%d, %d, %d);" % (
                color.red(), color.green(), color.blue())
            self.curvecolor4.setStyleSheet(qss)

    # click the first button on the left upper corner to import old testing data into the test window.
    def on_actOpen_triggered(self):
        curPath=QtCore.QDir.currentPath()
        filename, flt = QtWidgets.QFileDialog.getOpenFileName(None, "Eine Datei öffnen", curPath, "Testdaten (*.txt)")
        if (filename==""):
            return

        aFile = open(filename, 'r')
        allLine = aFile.readlines()
        aFile.close()
        fileInfo = QtCore.QFileInfo(filename)
        QtCore.QDir.setCurrent(fileInfo.absolutePath())

        self.__loadData(allLine)

    # the imported old data is visualized by this method
    def __loadData(self, allLines):
        #self.chart.removeAllSeries()
        rowCnt = len(allLines)-1  # 文本行数
        vectF = [0] * rowCnt
        vectMag = [0] * rowCnt
        for i in range(rowCnt):
            lineText = allLines[i].strip()
            strList = lineText.split()
            vectF[i] = float(strList[0][:-3])
            vectMag[i] = float(strList[1].replace(",", "."))

        pen = QtGui.QPen(QtGui.QColor(255, 109, 109))
        pen.setWidth(1)
        seriesF = QtChart.QLineSeries()
        seriesF.setName("Alte Kurve")
        seriesF.setPen(pen)
        seriesF.setPointsVisible(False)
        seriesF.hovered.connect(self.do_series_hovered)
        seriesF.clicked.connect(self.do_series_clicked)

        count = len(vectF)
        for i in range(count):
            seriesF.append(vectF[i], vectMag[i])
        self.chart.addSeries(seriesF)
        self.chart.setAxisX(self.__axisFreq, seriesF)
        self.chart.setAxisY(self.__axisMag, seriesF)

    # related to the printer functions
    def handle_print(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, None)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.handle_paint_request(printer)

    # open the printer window
    def handle_preview(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handle_paint_request)
        dialog.exec_()

    # confirmation of the print requirement and print the diagramm
    def handle_paint_request(self, printer):
        painter = QtGui.QPainter(printer)
        painter.setViewport(self.graphicsView.rect())
        painter.setWindow(self.graphicsView.rect())
        self.graphicsView.render(painter)
        painter.end()

        # when the diagramm is printed successfully, an information messageBox will appear and
        # tell users that the diagramm is printed successfully.
        messageBox = QtWidgets.QMessageBox()
        messageBox.setWindowTitle('Drucker')
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
        messageBox.setText('Das Diagramm wird erfolgreich ausgedrukt!')
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
        buttonY.setText('Ok')
        messageBox.exec_()

    # zoom out the diagramm
    def on_actZoomIn_triggered(self):
        self.graphicsView.chart().zoom(1.2)

    # zoom in the diagramm
    def on_actZoomOut_triggered(self):
        self.graphicsView.chart().zoom(0.8)

    # reset the diagramm into original size
    def on_actZoomReset_triggered(self):
        self.graphicsView.chart().zoomReset()



    # used to update the loading bar
    def onCountChanged(self, value, num):
        frequenz = []
        magnitude = []
        for x in value:
            if len(x) >= 13:
                frequenz.append(float(x.replace('\r\n', '')) / 1000.0)
            else:
                if x != '\r\n\n':
                    magnitude.append(float(x))
        Antena = np.interp(frequenz, self.tianxianf, self.tianxianm)
        kabel11 = np.interp(frequenz, self.cablef1, self.cablem1)
        kabel12 = np.interp(frequenz, self.cablef2, self.cablem2)
        real_PK = magnitude + Antena - kabel11 - kabel12 +30
        if self.curve1.isChecked():
            for i in range(len(frequenz)):
                self.series_1.append(frequenz[i],real_PK[i])
        elif self.curve2.isChecked():
            for i in range(len(frequenz)):
                self.series_2.append(frequenz[i],real_PK[i])
        elif self.curve3.isChecked():
            for i in range(len(frequenz)):
                self.series_3.append(frequenz[i],real_PK[i])
        elif self.curve4.isChecked():
            for i in range(len(frequenz)):
                self.series_4.replace(frequenz[i], real_PK[i])
        value = (num-30)/2700*100
        self.StatusProgressBar.setValue(value)

    # draw curves for the marginal values (Grenzwerte) of the norms
    def drawnormlimit(self, norm):
        self.data = []
        for i in range(len(norm)):
            a = norm[i].text()
            self.data.append(a)


        if 'Gruppe 1 (>75kVA). Gruppe 2 (>75kVA).Klasse A. Quasi-Peak.' in self.data:
            x = [150, 500, 501, 5000,5001,30000]
            y = [130, 130, 125, 125,115,115]
            normline1 = QtChart.QLineSeries()
            normline1.setName("Norm Line 1.")
            self.chart.addSeries(normline1)
            normline1.attachAxis(self.__axisFreq)
            normline1.attachAxis(self.__axisMag)
            self.chart.legend().markers(normline1)[0].setVisible(False)
            pen = QtGui.QPen(QtGui.QColor(45, 130, 255))
            pen.setWidth(3)
            normline1.setPen(pen)
            normline1.setPointsVisible(False)
            normline1.hovered.connect(self.do_series_hovered)
            normline1.clicked.connect(self.do_series_clicked)
            for a, b in zip(x, y):
                normline1.append(a, b)

        if 'Gruppe 1 (>75kVA). Gruppe 2 (>75kVA).Klasse A. Average.' in self.data:
            x = [150, 500, 501, 5000, 5001, 30000]
            y = [120, 120, 115, 115, 105, 105]
            normline2 = QtChart.QLineSeries()
            normline2.setName("Norm Line 2.")
            self.chart.addSeries(normline2)
            normline2.attachAxis(self.__axisFreq)
            normline2.attachAxis(self.__axisMag)
            self.chart.legend().markers(normline2)[0].setVisible(False)
            pen = QtGui.QPen(QtGui.QColor(45, 130, 255))
            pen.setWidth(3)
            normline2.setPen(pen)
            normline2.setPointsVisible(False)
            normline2.hovered.connect(self.do_series_hovered)
            normline2.clicked.connect(self.do_series_clicked)
            for a, b in zip(x, y):
                normline2.append(a, b)

        if 'Gruppe 1 (>20kVA). Klasse A. Quasi-Peak. 3m.' in self.data:
            x = [30, 230, 231, 1000]
            y = [60, 60, 60, 60]
            normline1 = QtChart.QLineSeries()
            normline1.setName("Norm Line 1.")
            self.chart.addSeries(normline1)
            normline1.attachAxis(self.__axisFreq)
            normline1.attachAxis(self.__axisMag)
            self.chart.legend().markers(normline1)[0].setVisible(False)
            pen = QtGui.QPen(QtGui.QColor(45, 130, 255))
            pen.setWidth(3)
            normline1.setPen(pen)
            normline1.setPointsVisible(False)
            normline1.hovered.connect(self.do_series_hovered)
            normline1.clicked.connect(self.do_series_clicked)
            for a, b in zip(x, y):
                normline1.append(a, b)
            self.label1.show()

        if 'Gruppe 1 (<=20kVA). Klasse A. Quasi-Peak. 3m.' in self.data:
            x = [30, 230, 231, 1000]
            y = [50, 50, 57, 57]
            normline2 = QtChart.QLineSeries()
            normline2.setName("Norm Line 2.")
            self.chart.addSeries(normline2)
            normline2.attachAxis(self.__axisFreq)
            normline2.attachAxis(self.__axisMag)
            self.chart.legend().markers(normline2)[0].setVisible(False)
            pen = QtGui.QPen(QtGui.QColor(45, 130, 255))
            pen.setWidth(3)
            normline2.setPen(pen)
            normline2.setPointsVisible(False)
            normline2.hovered.connect(self.do_series_hovered)
            normline2.clicked.connect(self.do_series_clicked)
            for a, b in zip(x, y):
                normline2.append(a, b)
            self.label2.show()

        if "Gruppe 1 (>20kVA). Klasse A. Quasi-Peak. 10m." in self.data:
            x = [30, 230, 231, 1000]
            y = [50, 50, 50, 50]
            normline3 = QtChart.QLineSeries()
            normline3.setName("Norm Line 3.")
            self.chart.addSeries(normline3)
            normline3.attachAxis(self.__axisFreq)
            normline3.attachAxis(self.__axisMag)
            self.chart.legend().markers(normline3)[0].setVisible(False)
            pen = QtGui.QPen(QtGui.QColor(45, 130, 255))
            pen.setWidth(3)
            normline3.setPen(pen)
            normline3.setPointsVisible(False)
            normline3.hovered.connect(self.do_series_hovered)
            normline3.clicked.connect(self.do_series_clicked)
            for a, b in zip(x, y):
                normline3.append(a, b)
            self.label3.show()

        if "Gruppe 1 (<=20kVA). Klasse A. Quasi-Peak. 10m." in self.data:
            x = [30, 230, 231, 1000]
            y = [40, 40, 47, 47]
            normline4 = QtChart.QLineSeries()
            normline4.setName("Norm Line 4.")
            self.chart.addSeries(normline4)
            normline4.attachAxis(self.__axisFreq)
            normline4.attachAxis(self.__axisMag)
            self.chart.legend().markers(normline4)[0].setVisible(False)
            pen = QtGui.QPen(QtGui.QColor(45, 130, 255))
            pen.setWidth(3)
            normline4.setPen(pen)
            normline4.setPointsVisible(False)
            normline4.hovered.connect(self.do_series_hovered)
            normline4.clicked.connect(self.do_series_clicked)
            for a, b in zip(x, y):
                normline4.append(a, b)
            self.label4.show()

        if "Gruppe 1. Klasse B. Quasi-Peak. 3m." in self.data:
            x = [30, 230, 231, 1000]
            y = [40, 40, 47, 47]
            normline5 = QtChart.QLineSeries()
            normline5.setName("Norm Line 5.")
            self.chart.addSeries(normline5)
            normline5.attachAxis(self.__axisFreq)
            normline5.attachAxis(self.__axisMag)
            self.chart.legend().markers(normline5)[0].setVisible(False)
            pen = QtGui.QPen(QtGui.QColor(45, 130, 255))
            pen.setWidth(3)
            normline5.setPen(pen)
            normline5.setPointsVisible(False)
            normline5.hovered.connect(self.do_series_hovered)
            normline5.clicked.connect(self.do_series_clicked)
            for a, b in zip(x, y):
                normline5.append(a, b)
            self.label5.show()

        if "Gruppe 1. Klasse B. Quasi-Peak. 10m." in self.data:
            x = [30, 230, 231, 1000]
            y = [30, 30, 37, 37]
            normline6 = QtChart.QLineSeries()
            normline6.setName("Norm Line 6.")
            self.chart.addSeries(normline6)
            normline6.attachAxis(self.__axisFreq)
            normline6.attachAxis(self.__axisMag)
            self.chart.legend().markers(normline6)[0].setVisible(False)
            pen = QtGui.QPen(QtGui.QColor(45, 130, 255))
            pen.setWidth(3)
            normline6.setPen(pen)
            normline6.setPointsVisible(False)
            normline6.hovered.connect(self.do_series_hovered)
            normline6.clicked.connect(self.do_series_clicked)
            for a, b in zip(x, y):
                normline6.append(a, b)
            self.label6.show()

        if "Gruppe 2. Klasse A. Quasi-Peak. 3m." in self.data:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Mangel an Grenzwerten')
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
            messageBox.setText('Sorry, die Grenzwerte für \"Gruppe 2. Klasse A. Quasi-Peak. 3m.\" in dieser Norm ist noch nicht definiert.')
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
            buttonY.setText('Ok')
            messageBox.exec_()

        if "Gruppe 2. Klasse A. Quasi-Peak. 10m." in self.data:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Mangel an Grenzwerten')
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
            messageBox.setText(
                'Sorry, die Grenzwerte für \"Gruppe 2. Klasse A. Quasi-Peak. 10m.\" in dieser Norm ist noch nicht definiert.')
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
            buttonY.setText('Ok')
            messageBox.exec_()

        if "Gruppe 2. Klasse A. Quasi-Peak. 30m." in self.data:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Mangel an Grenzwerten')
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
            messageBox.setText(
                'Sorry, die Grenzwerte für \"Gruppe 2. Klasse A. Quasi-Peak. 30m.\" in dieser Norm ist noch nicht definiert.')
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
            buttonY.setText('Ok')
            messageBox.exec_()

        if "Gruppe 2. Klasse B. Quasi-Peak. 3m." in self.data:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Mangel an Grenzwerten')
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
            messageBox.setText(
                'Sorry, die Grenzwerte für \"Gruppe 2. Klasse B. Quasi-Peak. 3m.\" in dieser Norm ist noch nicht definiert.')
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
            buttonY.setText('Ok')
            messageBox.exec_()

        if "Gruppe 2. Klasse B. Average. 3m." in self.data:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Mangel an Grenzwerten')
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
            messageBox.setText(
                'Sorry, die Grenzwerte für \"Gruppe 2. Klasse B. Average. 3m.\" in dieser Norm ist noch nicht definiert.')
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
            buttonY.setText('Ok')
            messageBox.exec_()

        if "Gruppe 2. Klasse B. Quasi-Peak. 10m." in self.data:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Mangel an Grenzwerten')
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
            messageBox.setText(
                'Sorry, die Grenzwerte für \"Gruppe 2. Klasse B. Quasi-Peak. 10m.\" in dieser Norm ist noch nicht definiert.')
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
            buttonY.setText('Ok')
            messageBox.exec_()

        if "Gruppe 2. Klasse B. Average. 10m." in self.data:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle('Mangel an Grenzwerten')
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
            messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
            messageBox.setText(
                'Sorry, die Grenzwerte für \"Gruppe 2. Klasse B. Average. 10m.\" in dieser Norm ist noch nicht definiert.')
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
            buttonY.setText('Ok')
            messageBox.exec_()

    # hide all curve labels of the marginal values (Grenzwerte)
    def hide_line_labels(self):
        self.label1.hide()
        self.label2.hide()
        self.label3.hide()
        self.label4.hide()
        self.label5.hide()
        self.label6.hide()

    # show all curve labels of the marginal values (Grenzwerte)
    def show_line_labels(self):
        if 'Gruppe 1 (>20kVA). Klasse A. Quasi-Peak. 3m.' in self.data:
            self.label1.show()
        if 'Gruppe 1 (<=20kVA). Klasse A. Quasi-Peak. 3m.' in self.data:
            self.label2.show()
        if "Gruppe 1 (>20kVA). Klasse A. Quasi-Peak. 10m." in self.data:
            self.label3.show()
        if "Gruppe 1 (<=20kVA). Klasse A. Quasi-Peak. 10m." in self.data:
            self.label4.show()
        if "Gruppe 1. Klasse B. Quasi-Peak. 3m." in self.data:
            self.label5.show()
        if "Gruppe 1. Klasse B. Quasi-Peak. 10m." in self.data:
            self.label6.show()

from PyQt5 import QtChart

# decode the color and obtain the channel numbers
def color(hex):
    r = int(hex[1:3],16)
    g = int(hex[3:5],16)
    b = int(hex[5:7], 16)
    return r,g,b



if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TestWindow = QtWidgets.QWidget()
    ui = Ui_TestWindow_LE()
    ui.setupUi(TestWindow)
    TestWindow.show()
    sys.exit(app.exec_())

