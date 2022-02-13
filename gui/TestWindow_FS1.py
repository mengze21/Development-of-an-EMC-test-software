import csv
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtChart
from PyQt5.QtCore import Qt
import time
import numpy as np
import math
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
import WordReportGenerator
import cv2 as cv
import qimage2ndarray
import os
from thread_FS import External_FS
from thread_FS_test import External_FS_test

sys.path.append('gui')

# "PyQt5.QtPrintSupport" supports printer. Qprint is used to print the diagram in Test Window.
# QprintDialog is used to open the printer window.
# QpagesteupDialog is used for printer settings.


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

    # define the method of mouse press
    def mousePressEvent(self, event):  # mouse click
        if event.button() == QtCore.Qt.LeftButton:
            self.__beginPoint = event.pos()  # record the start point
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):  # mouse click
        if event.button() == QtCore.Qt.leftButton:
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
            self.chart().zoomIn(rectF)  # zoom in the selected rectangular area
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

# This class defines the "Test" window, which is used to show up the visualized measurement results in real-time.
# It's Qt-Designer files are "TestWindow.ui" in folder "uifiles"


class Ui_TestWindow_FS(object):
    def setupUi(self, TestWindow):
        TestWindow.setObjectName("TestWindow")
        TestWindow.resize(1115, 850)
        TestWindow.setMinimumSize(QtCore.QSize(1100, 850))
        self.gridLayout = QtWidgets.QGridLayout(TestWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.ButtonFrame = QtWidgets.QFrame(TestWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonFrame.sizePolicy().hasHeightForWidth())
        self.ButtonFrame.setSizePolicy(sizePolicy)
        self.ButtonFrame.setMinimumSize(QtCore.QSize(0, 50))
        self.ButtonFrame.setSizeIncrement(QtCore.QSize(0, 0))
        self.ButtonFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ButtonFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ButtonFrame.setObjectName("ButtonFrame")
        self.OpenFilePushButton = QtWidgets.QPushButton(self.ButtonFrame)
        self.OpenFilePushButton.setGeometry(QtCore.QRect(20, 10, 31, 31))
        self.OpenFilePushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon_materials/13.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.OpenFilePushButton.setIcon(icon)
        self.OpenFilePushButton.setIconSize(QtCore.QSize(31, 31))
        self.OpenFilePushButton.setObjectName("OpenFilePushButton")
        self.PrintPushButton = QtWidgets.QPushButton(self.ButtonFrame)
        self.PrintPushButton.setGeometry(QtCore.QRect(60, 10, 31, 31))
        self.PrintPushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon_materials/19.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.PrintPushButton.setIcon(icon1)
        self.PrintPushButton.setIconSize(QtCore.QSize(31, 31))
        self.PrintPushButton.setObjectName("PrintPushButton")
        self.HandMovePushButton = QtWidgets.QPushButton(self.ButtonFrame)
        self.HandMovePushButton.setGeometry(QtCore.QRect(120, 10, 31, 31))
        self.HandMovePushButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon_materials/28.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.HandMovePushButton.setIcon(icon2)
        self.HandMovePushButton.setIconSize(QtCore.QSize(31, 31))
        self.HandMovePushButton.setObjectName("HandMovePushButton")
        self.pushButton_4 = QtWidgets.QPushButton(self.ButtonFrame)
        self.pushButton_4.setGeometry(QtCore.QRect(160, 10, 31, 31))
        self.pushButton_4.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icon_materials/29.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setIconSize(QtCore.QSize(31, 31))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.ButtonFrame)
        self.pushButton_5.setGeometry(QtCore.QRect(200, 10, 31, 31))
        self.pushButton_5.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icon_materials/30.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_5.setIcon(icon4)
        self.pushButton_5.setIconSize(QtCore.QSize(31, 31))
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
        self.pushButton_6 = QtWidgets.QPushButton(self.ButtonFrame)
        self.pushButton_6.setGeometry(QtCore.QRect(250, 10, 31, 31))
        self.pushButton_6.setMinimumSize(QtCore.QSize(31, 31))
        self.pushButton_6.setMaximumSize(QtCore.QSize(31, 31))
        self.pushButton_6.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icon_materials/20.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_6.setIcon(icon5)
        self.pushButton_6.setIconSize(QtCore.QSize(31, 31))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.ButtonFrame)
        self.pushButton_7.setGeometry(QtCore.QRect(290, 10, 31, 31))
        self.pushButton_7.setMinimumSize(QtCore.QSize(31, 31))
        self.pushButton_7.setMaximumSize(QtCore.QSize(31, 31))
        self.pushButton_7.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icon_materials/31.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_7.setIcon(icon6)
        self.pushButton_7.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.ButtonFrame, 2, 0, 1, 3)
        self.GraphicFrame = QtWidgets.QFrame(TestWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GraphicFrame.sizePolicy().hasHeightForWidth())
        self.GraphicFrame.setSizePolicy(sizePolicy)
        self.GraphicFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.GraphicFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.GraphicFrame.setObjectName("GraphicFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.GraphicFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # creation of the interactive diagram in the "Test" window
        self.chart_1 = QtChart.QChart()
        self.chart_2 = QtChart.QChart()

        self.graphicsView = QmyChartView(self.GraphicFrame)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView.setCursor(QtCore.Qt.ArrowCursor)
        self.graphicsView.mouseMove.connect(self.do_chartView_mouseMove)
        self.graphicsView.setChart(self.chart_1)

        self.graphicsView_2 = QmyChartView(self.GraphicFrame)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.horizontalLayout.addWidget(self.graphicsView_2)
        self.graphicsView_2.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView_2.setCursor(QtCore.Qt.ArrowCursor)
        self.graphicsView_2.mouseMove.connect(self.do_chartView_mouseMove)
        self.graphicsView_2.setChart(self.chart_2)

        # creation of axis to chart_1
        self.__axisFreq = QtChart.QLogValueAxis()
        self.__axisFreq.setLabelFormat("%d")  # format of the label
        self.__axisFreq.setTitleText("Frequenz / MHz \r\n ")
        self.__axisFreq.setRange(10, 10000)
        self.__axisFreq.setMinorTickCount(8)
        # self.__axisFreq.tickAn([ticks])
        self.chart_1.addAxis(self.__axisFreq, QtCore.Qt.AlignBottom)
        self.__axisMag = QtChart.QValueAxis()
        self.__axisMag.setTitleText("Feldstärke / V/m  ")
        self.__axisMag.setRange(0, 50)
        self.__axisMag.setTickCount(8)
        self.__axisMag.setLabelFormat("%d")
        self.chart_1.addAxis(self.__axisMag, QtCore.Qt.AlignLeft)
        # creation of axis to chart_2
        self.__axisFreq_2 = QtChart.QLogValueAxis()
        self.__axisFreq_2.setLabelFormat("%d")  # format of the label
        self.__axisFreq_2.setTitleText("Frequenz / MHz \r\n ")
        self.__axisFreq_2.setRange(10, 10000)
        self.__axisFreq_2.setMinorTickCount(8)
        # self.__axisFreq.tickAn([ticks])
        self.chart_2.addAxis(self.__axisFreq_2, QtCore.Qt.AlignBottom)
        self.__axisMag_2 = QtChart.QValueAxis()
        self.__axisMag_2.setTitleText("Vorwärtsleistung / dBm ")
        self.__axisMag_2.setRange(-30, 10)
        self.__axisMag_2.setTickCount(8)
        self.__axisMag_2.setLabelFormat("%d")
        self.chart_2.addAxis(self.__axisMag_2, QtCore.Qt.AlignLeft)

        # create curve for forward power
        self.curveFPower = QtChart.QLineSeries()
        self.curveFPower.setName("P1")
        self.chart_2.addSeries(self.curveFPower)
        self.curveFPower.attachAxis(self.__axisFreq_2)
        self.curveFPower.attachAxis(self.__axisMag_2)
        self.chart_2.legend().markers(self.curveFPower)[0].setVisible(True)
        self.chart_2.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        pen.setWidth(1)
        self.curveFPower.setPen(pen)
        self.curveFPower.setPointsVisible(True)
        self.curveFPower.hovered.connect(self.do_series_hovered)
        self.curveFPower.clicked.connect(self.do_series_clicked)
        # create curve for real time test
        self.curveFPower_realTime = QtChart.QLineSeries()
        self.curveFPower_realTime.setName("Vorwärtleistung")
        self.chart_2.addSeries(self.curveFPower_realTime)
        self.curveFPower_realTime.attachAxis(self.__axisFreq_2)
        self.curveFPower_realTime.attachAxis(self.__axisMag_2)
        self.chart_2.legend().markers(self.curveFPower_realTime)[0].setVisible(False)
        self.chart_2.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 255))
        pen.setWidth(1)
        self.curveFPower_realTime.setPen(pen)
        self.curveFPower_realTime.setPointsVisible(True)
        self.curveFPower_realTime.hovered.connect(self.do_series_hovered)
        self.curveFPower_realTime.clicked.connect(self.do_series_clicked)

        # create curve for field strength
        self.curveFieldStr = QtChart.QLineSeries()
        self.curveFieldStr.setName("P1")
        self.chart_1.addSeries(self.curveFieldStr)
        self.curveFieldStr.attachAxis(self.__axisFreq)
        self.curveFieldStr.attachAxis(self.__axisMag)
        self.chart_1.legend().markers(self.curveFieldStr)[0].setVisible(True)
        self.chart_1.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        pen.setWidth(1)
        self.curveFieldStr.setPen(pen)
        self.curveFieldStr.setPointsVisible(True)
        self.curveFieldStr.hovered.connect(self.do_series_hovered)
        self.curveFieldStr.clicked.connect(self.do_series_clicked)
        # creat curve for real time test
        self.curveFieldStr_realTime = QtChart.QLineSeries()
        self.curveFieldStr_realTime.setName("P1")
        self.chart_1.addSeries(self.curveFieldStr_realTime)
        self.curveFieldStr_realTime.attachAxis(self.__axisFreq)
        self.curveFieldStr_realTime.attachAxis(self.__axisMag)
        self.chart_1.legend().markers(self.curveFieldStr_realTime)[0].setVisible(False)
        self.chart_1.legend().setAlignment(Qt.AlignTop)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 255))
        pen.setWidth(1)
        self.curveFieldStr_realTime.setPen(pen)
        self.curveFieldStr_realTime.setPointsVisible(True)
        self.curveFieldStr_realTime.hovered.connect(self.do_series_hovered)
        self.curveFieldStr_realTime.clicked.connect(self.do_series_clicked)


        self.StatusleisteGroupBox = QtWidgets.QGroupBox(self.GraphicFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StatusleisteGroupBox.sizePolicy().hasHeightForWidth())
        self.StatusleisteGroupBox.setSizePolicy(sizePolicy)
        self.StatusleisteGroupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.StatusleisteGroupBox.setMaximumSize(QtCore.QSize(511, 11111))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.StatusleisteGroupBox.setFont(font)
        self.StatusleisteGroupBox.setObjectName("StatusleisteGroupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.StatusleisteGroupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.AktuellerZustandLabel = QtWidgets.QLabel(self.StatusleisteGroupBox)
        self.AktuellerZustandLabel.setMinimumSize(QtCore.QSize(171, 31))
        self.AktuellerZustandLabel.setMaximumSize(QtCore.QSize(171, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.AktuellerZustandLabel.setFont(font)
        self.AktuellerZustandLabel.setObjectName("AktuellerZustandLabel")
        self.gridLayout_2.addWidget(self.AktuellerZustandLabel, 0, 0, 1, 1)
        self.AktuellerZustandLineEdit = QtWidgets.QLineEdit(self.StatusleisteGroupBox)
        self.AktuellerZustandLineEdit.setMinimumSize(QtCore.QSize(231, 31))
        self.AktuellerZustandLineEdit.setMaximumSize(QtCore.QSize(231, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(156, 156, 156))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(156, 156, 156))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.AktuellerZustandLineEdit.setPalette(palette)
        self.AktuellerZustandLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.AktuellerZustandLineEdit.setText("")
        self.AktuellerZustandLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.AktuellerZustandLineEdit.setReadOnly(True)
        self.AktuellerZustandLineEdit.setObjectName("AktuellerZustandLineEdit")
        self.gridLayout_2.addWidget(self.AktuellerZustandLineEdit, 1, 0, 1, 1)
        self.InformationenKoordinatenGroupBox = QtWidgets.QGroupBox(self.StatusleisteGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.InformationenKoordinatenGroupBox.sizePolicy().hasHeightForWidth())
        self.InformationenKoordinatenGroupBox.setSizePolicy(sizePolicy)
        self.InformationenKoordinatenGroupBox.setMinimumSize(QtCore.QSize(0, 151))
        self.InformationenKoordinatenGroupBox.setMaximumSize(QtCore.QSize(631, 11111))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.InformationenKoordinatenGroupBox.setFont(font)
        self.InformationenKoordinatenGroupBox.setObjectName("InformationenKoordinatenGroupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.InformationenKoordinatenGroupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.GeschwebtLabel = QtWidgets.QLabel(self.InformationenKoordinatenGroupBox)
        self.GeschwebtLabel.setMinimumSize(QtCore.QSize(111, 31))
        self.GeschwebtLabel.setMaximumSize(QtCore.QSize(111, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.GeschwebtLabel.setFont(font)
        self.GeschwebtLabel.setObjectName("GeschwebtLabel")
        self.gridLayout_3.addWidget(self.GeschwebtLabel, 0, 0, 1, 1)
        self.GeklicktMagnitudeLabel = QtWidgets.QLabel(self.InformationenKoordinatenGroupBox)
        self.GeklicktMagnitudeLabel.setMinimumSize(QtCore.QSize(101, 31))
        self.GeklicktMagnitudeLabel.setMaximumSize(QtCore.QSize(101, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.GeklicktMagnitudeLabel.setFont(font)
        self.GeklicktMagnitudeLabel.setObjectName("GeklicktMagnitudeLabel")
        self.gridLayout_3.addWidget(self.GeklicktMagnitudeLabel, 5, 0, 1, 1)
        self.GeklicktLabel = QtWidgets.QLabel(self.InformationenKoordinatenGroupBox)
        self.GeklicktLabel.setMinimumSize(QtCore.QSize(81, 31))
        self.GeklicktLabel.setMaximumSize(QtCore.QSize(81, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.GeklicktLabel.setFont(font)
        self.GeklicktLabel.setObjectName("GeklicktLabel")
        self.gridLayout_3.addWidget(self.GeklicktLabel, 3, 0, 1, 1)
        self.GeschwebtMagnitudeLineEdit = QtWidgets.QLineEdit(self.InformationenKoordinatenGroupBox)
        self.GeschwebtMagnitudeLineEdit.setMinimumSize(QtCore.QSize(101, 31))
        self.GeschwebtMagnitudeLineEdit.setMaximumSize(QtCore.QSize(131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.GeschwebtMagnitudeLineEdit.setFont(font)
        self.GeschwebtMagnitudeLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.GeschwebtMagnitudeLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.GeschwebtMagnitudeLineEdit.setReadOnly(True)
        self.GeschwebtMagnitudeLineEdit.setObjectName("GeschwebtMagnitudeLineEdit")
        self.gridLayout_3.addWidget(self.GeschwebtMagnitudeLineEdit, 2, 1, 1, 1)
        self.GeschwebtMagnitudeLabel = QtWidgets.QLabel(self.InformationenKoordinatenGroupBox)
        self.GeschwebtMagnitudeLabel.setMinimumSize(QtCore.QSize(101, 31))
        self.GeschwebtMagnitudeLabel.setMaximumSize(QtCore.QSize(101, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.GeschwebtMagnitudeLabel.setFont(font)
        self.GeschwebtMagnitudeLabel.setObjectName("GeschwebtMagnitudeLabel")
        self.gridLayout_3.addWidget(self.GeschwebtMagnitudeLabel, 2, 0, 1, 1)
        self.GeschwebtToolButton = QtWidgets.QToolButton(self.InformationenKoordinatenGroupBox)
        self.GeschwebtToolButton.setMinimumSize(QtCore.QSize(31, 31))
        self.GeschwebtToolButton.setMaximumSize(QtCore.QSize(31, 31))
        self.GeschwebtToolButton.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icon_materials/9.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.GeschwebtToolButton.setIcon(icon7)
        self.GeschwebtToolButton.setIconSize(QtCore.QSize(30, 30))
        self.GeschwebtToolButton.setObjectName("GeschwebtToolButton")
        self.gridLayout_3.addWidget(self.GeschwebtToolButton, 0, 1, 1, 1)
        self.GeschwebtFrequenzLineEdit = QtWidgets.QLineEdit(self.InformationenKoordinatenGroupBox)
        self.GeschwebtFrequenzLineEdit.setMinimumSize(QtCore.QSize(101, 31))
        self.GeschwebtFrequenzLineEdit.setMaximumSize(QtCore.QSize(131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.GeschwebtFrequenzLineEdit.setFont(font)
        self.GeschwebtFrequenzLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.GeschwebtFrequenzLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.GeschwebtFrequenzLineEdit.setReadOnly(True)
        self.GeschwebtFrequenzLineEdit.setObjectName("GeschwebtFrequenzLineEdit")
        self.gridLayout_3.addWidget(self.GeschwebtFrequenzLineEdit, 1, 1, 1, 1)
        self.MousPositionLabel = QtWidgets.QLabel(self.InformationenKoordinatenGroupBox)
        self.MousPositionLabel.setMinimumSize(QtCore.QSize(0, 21))
        self.MousPositionLabel.setMaximumSize(QtCore.QSize(611, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.MousPositionLabel.setFont(font)
        self.MousPositionLabel.setText("")
        self.MousPositionLabel.setObjectName("MousPositionLabel")
        self.gridLayout_3.addWidget(self.MousPositionLabel, 6, 0, 1, 2)
        self.GeklicktFrequenzLineEdit = QtWidgets.QLineEdit(self.InformationenKoordinatenGroupBox)
        self.GeklicktFrequenzLineEdit.setMinimumSize(QtCore.QSize(101, 31))
        self.GeklicktFrequenzLineEdit.setMaximumSize(QtCore.QSize(131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.GeklicktFrequenzLineEdit.setFont(font)
        self.GeklicktFrequenzLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.GeklicktFrequenzLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.GeklicktFrequenzLineEdit.setReadOnly(True)
        self.GeklicktFrequenzLineEdit.setObjectName("GeklicktFrequenzLineEdit")
        self.gridLayout_3.addWidget(self.GeklicktFrequenzLineEdit, 4, 1, 1, 1)
        self.GeklicktFrequenzLabel = QtWidgets.QLabel(self.InformationenKoordinatenGroupBox)
        self.GeklicktFrequenzLabel.setMinimumSize(QtCore.QSize(91, 31))
        self.GeklicktFrequenzLabel.setMaximumSize(QtCore.QSize(91, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.GeklicktFrequenzLabel.setFont(font)
        self.GeklicktFrequenzLabel.setObjectName("GeklicktFrequenzLabel")
        self.gridLayout_3.addWidget(self.GeklicktFrequenzLabel, 4, 0, 1, 1)
        self.GeschwebtFrequenzLabel = QtWidgets.QLabel(self.InformationenKoordinatenGroupBox)
        self.GeschwebtFrequenzLabel.setMinimumSize(QtCore.QSize(91, 31))
        self.GeschwebtFrequenzLabel.setMaximumSize(QtCore.QSize(91, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.GeschwebtFrequenzLabel.setFont(font)
        self.GeschwebtFrequenzLabel.setObjectName("GeschwebtFrequenzLabel")
        self.gridLayout_3.addWidget(self.GeschwebtFrequenzLabel, 1, 0, 1, 1)
        self.GeklicktToolButton = QtWidgets.QToolButton(self.InformationenKoordinatenGroupBox)
        self.GeklicktToolButton.setMinimumSize(QtCore.QSize(31, 31))
        self.GeklicktToolButton.setMaximumSize(QtCore.QSize(31, 31))
        self.GeklicktToolButton.setText("")
        self.GeklicktToolButton.setIcon(icon7)
        self.GeklicktToolButton.setIconSize(QtCore.QSize(30, 30))
        self.GeklicktToolButton.setObjectName("GeklicktToolButton")
        self.gridLayout_3.addWidget(self.GeklicktToolButton, 3, 1, 1, 1)
        self.GeklicktMagnitudeLineEdit = QtWidgets.QLineEdit(self.InformationenKoordinatenGroupBox)
        self.GeklicktMagnitudeLineEdit.setMinimumSize(QtCore.QSize(101, 31))
        self.GeklicktMagnitudeLineEdit.setMaximumSize(QtCore.QSize(131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.GeklicktMagnitudeLineEdit.setFont(font)
        self.GeklicktMagnitudeLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.GeklicktMagnitudeLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.GeklicktMagnitudeLineEdit.setReadOnly(True)
        self.GeklicktMagnitudeLineEdit.setObjectName("GeklicktMagnitudeLineEdit")
        self.gridLayout_3.addWidget(self.GeklicktMagnitudeLineEdit, 5, 1, 1, 1)
        self.gridLayout_2.addWidget(self.InformationenKoordinatenGroupBox, 2, 0, 1, 1)
        self.horizontalLayout.addWidget(self.StatusleisteGroupBox)
        self.gridLayout.addWidget(self.GraphicFrame, 3, 0, 1, 3)
        self.StatusFrames = QtWidgets.QFrame(TestWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StatusFrames.sizePolicy().hasHeightForWidth())
        self.StatusFrames.setSizePolicy(sizePolicy)
        self.StatusFrames.setMinimumSize(QtCore.QSize(0, 50))
        self.StatusFrames.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.StatusFrames.setFrameShadow(QtWidgets.QFrame.Raised)
        self.StatusFrames.setObjectName("StatusFrames")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.StatusFrames)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.StatusProgressBar = QtWidgets.QProgressBar(self.StatusFrames)
        self.StatusProgressBar.setProperty("value", 0)
        self.StatusProgressBar.setObjectName("StatusProgressBar")
        self.gridLayout_5.addWidget(self.StatusProgressBar, 1, 0, 1, 2)
        self.TestParaInfo = QtWidgets.QTableWidget(self.StatusFrames)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.TestParaInfo.setFont(font)
        self.TestParaInfo.setObjectName("TestParaInfo")
        self.TestParaInfo.setColumnCount(8)
        self.TestParaInfo.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        item.setFont(font)
        self.TestParaInfo.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        item.setFont(font)
        self.TestParaInfo.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        item.setFont(font)
        self.TestParaInfo.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        item.setFont(font)
        self.TestParaInfo.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        item.setFont(font)
        self.TestParaInfo.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        item.setFont(font)
        self.TestParaInfo.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        item.setFont(font)
        self.TestParaInfo.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        item.setFont(font)
        self.TestParaInfo.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.TestParaInfo.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TestParaInfo.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.TestParaInfo.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.TestParaInfo.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.TestParaInfo.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.TestParaInfo.setItem(0, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.TestParaInfo.setItem(0, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.TestParaInfo.setItem(0, 7, item)
        self.TestParaInfo.horizontalHeader().setDefaultSectionSize(120)
        self.TestParaInfo.verticalHeader().setVisible(False)
        self.TestParaInfo.verticalHeader().setDefaultSectionSize(30)
        self.gridLayout_5.addWidget(self.TestParaInfo, 3, 1, 1, 1)
        self.TestStatusLabel = QtWidgets.QLabel(self.StatusFrames)
        self.TestStatusLabel.setObjectName("TestStatusLabel")
        self.gridLayout_5.addWidget(self.TestStatusLabel, 0, 0, 1, 2)
        self.label_testSetup = QtWidgets.QLabel(self.StatusFrames)
        self.label_testSetup.setObjectName("label_testSetup")
        self.gridLayout_5.addWidget(self.label_testSetup, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.StatusFrames, 5, 0, 1, 2)
        self.line4 = QtWidgets.QFrame(TestWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line4.sizePolicy().hasHeightForWidth())
        self.line4.setSizePolicy(sizePolicy)
        self.line4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line4.setObjectName("line4")
        self.gridLayout.addWidget(self.line4, 4, 0, 1, 3)
        self.TestKontrollenGroupBox = QtWidgets.QGroupBox(TestWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TestKontrollenGroupBox.sizePolicy().hasHeightForWidth())
        self.TestKontrollenGroupBox.setSizePolicy(sizePolicy)
        self.TestKontrollenGroupBox.setMaximumSize(QtCore.QSize(220, 500))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.TestKontrollenGroupBox.setFont(font)
        self.TestKontrollenGroupBox.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.TestKontrollenGroupBox.setObjectName("TestKontrollenGroupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.TestKontrollenGroupBox)
        self.gridLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_4.setVerticalSpacing(20)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.TestStartButtonLabel = QtWidgets.QLabel(self.TestKontrollenGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TestStartButtonLabel.sizePolicy().hasHeightForWidth())
        self.TestStartButtonLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.TestStartButtonLabel.setFont(font)
        self.TestStartButtonLabel.setObjectName("TestStartButtonLabel")
        self.gridLayout_4.addWidget(self.TestStartButtonLabel, 1, 0, 1, 1)
        self.TestPausePushButton = QtWidgets.QPushButton(self.TestKontrollenGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TestPausePushButton.sizePolicy().hasHeightForWidth())
        self.TestPausePushButton.setSizePolicy(sizePolicy)
        self.TestPausePushButton.setMaximumSize(QtCore.QSize(60, 60))
        self.TestPausePushButton.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icon_materials/18.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.TestPausePushButton.setIcon(icon8)
        self.TestPausePushButton.setIconSize(QtCore.QSize(60, 60))
        self.TestPausePushButton.setObjectName("TestPausePushButton")
        self.gridLayout_4.addWidget(self.TestPausePushButton, 0, 1, 1, 1)
        self.DatenExportierenToolButton = QtWidgets.QToolButton(self.TestKontrollenGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DatenExportierenToolButton.sizePolicy().hasHeightForWidth())
        self.DatenExportierenToolButton.setSizePolicy(sizePolicy)
        self.DatenExportierenToolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.DatenExportierenToolButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.DatenExportierenToolButton.setFont(font)
        self.DatenExportierenToolButton.setObjectName("DatenExportierenToolButton")
        self.gridLayout_4.addWidget(self.DatenExportierenToolButton, 2, 0, 1, 4)
        self.ReportGenerierenToolButton = QtWidgets.QToolButton(self.TestKontrollenGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ReportGenerierenToolButton.sizePolicy().hasHeightForWidth())
        self.ReportGenerierenToolButton.setSizePolicy(sizePolicy)
        self.ReportGenerierenToolButton.setMinimumSize(QtCore.QSize(0, 30))
        self.ReportGenerierenToolButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.ReportGenerierenToolButton.setObjectName("ReportGenerierenToolButton")
        self.gridLayout_4.addWidget(self.ReportGenerierenToolButton, 3, 0, 1, 4)
        self.TestStratButton = QtWidgets.QPushButton(self.TestKontrollenGroupBox)
        self.TestStratButton.setMinimumSize(QtCore.QSize(60, 60))
        self.TestStratButton.setMaximumSize(QtCore.QSize(60, 60))
        self.TestStratButton.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icon_materials/7.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.TestStratButton.setIcon(icon9)
        self.TestStratButton.setIconSize(QtCore.QSize(60, 60))
        self.TestStratButton.setObjectName("TestStratButton")
        self.gridLayout_4.addWidget(self.TestStratButton, 0, 0, 1, 1)
        self.TestPauseButtonLabel = QtWidgets.QLabel(self.TestKontrollenGroupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.TestPauseButtonLabel.setFont(font)
        self.TestPauseButtonLabel.setObjectName("TestPauseButtonLabel")
        self.gridLayout_4.addWidget(self.TestPauseButtonLabel, 1, 1, 1, 1)
        self.TestStopPushButton = QtWidgets.QPushButton(self.TestKontrollenGroupBox)
        self.TestStopPushButton.setMaximumSize(QtCore.QSize(60, 60))
        self.TestStopPushButton.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("icon_materials/21.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.TestStopPushButton.setIcon(icon10)
        self.TestStopPushButton.setIconSize(QtCore.QSize(60, 60))
        self.TestStopPushButton.setObjectName("TestStopPushButton")
        self.gridLayout_4.addWidget(self.TestStopPushButton, 0, 2, 1, 1)
        self.TestStopButtonLabel = QtWidgets.QLabel(self.TestKontrollenGroupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.TestStopButtonLabel.setFont(font)
        self.TestStopButtonLabel.setObjectName("TestStopButtonLabel")
        self.gridLayout_4.addWidget(self.TestStopButtonLabel, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.TestKontrollenGroupBox, 5, 2, 1, 1)

        self.retranslateUi(TestWindow)
        QtCore.QMetaObject.connectSlotsByName(TestWindow)

        # open and read measurement data
        # measurement data in positon 1
        self.measuredFreq = []  # init parameters
        self.forwardPower = []  # init parameters
        self.probData = []  # init parameters
        with open("./output.csv", "r") as FSCaliData:
            reader = csv.reader(FSCaliData)
            rows = []
            for row in reader:
                rows.append(row)
            print(rows)
        for i in range(len(rows)):
            self.measuredFreq.append(float(rows[i][0]))  # column 0 is frequency
            self.forwardPower.append(float(rows[i][1]))  # column 1 is forward power
            self.probData.append(float(rows[i][2]))  # column 2 is measurement data field strength from prob

        # adding data forward power to chart1
        for a, b in zip(self.measuredFreq, self.forwardPower):
            self.curveFPower.append(a, b)
        # adding data field strength to chart1
        for a, b in zip(self.measuredFreq, self.probData):
            self.curveFieldStr.append(a, b)

        # # adding graphic frame
        # self.GraphicFrame = QtWidgets.QFrame(TestWindow)
        # self.GraphicFrame.setGeometry(QtCore.QRect(20, 70, 1561, 541))
        # self.GraphicFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.GraphicFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.GraphicFrame.setObjectName("GraphicFrame")

        # creation of the interactive diagram in the "Test" window
        # self.chart_1 = QtChart.QChart()
        # self.chart_2 = QtChart.QChart()
        # # QtChart.QCategoryAxis *axisX= new QCategoryAxis
        # # creation of axis
        # self.__axisFreq = QtChart.QLogValueAxis()
        # self.__axisFreq.setLabelFormat("%d")  # format of the label
        # self.__axisFreq.setTitleText("Frequenz / kHz \r\n ")
        # self.__axisFreq.setRange(100, 100000)
        # self.__axisFreq.setMinorTickCount(8)
        # # self.__axisFreq.tickAn([ticks])
        # self.chart_1.addAxis(self.__axisFreq, QtCore.Qt.AlignBottom)
        # self.__axisMag = QtChart.QValueAxis()
        # self.__axisMag.setTitleText("Generator - Leistung / dBm  ")
        # self.__axisMag.setRange(-35, -0)
        # self.__axisMag.setTickCount(8)
        # self.__axisMag.setLabelFormat("%d")
        # self.chart_1.addAxis(self.__axisMag, QtCore.Qt.AlignLeft)

        # self.graphicsView = QmyChartView(self.GraphicFrame)
        # self.horizontalLayout.addWidget(self.graphicsView)
        # #self.graphicsView.setGeometry(QtCore.QRect(0, 0, 601, 541))
        # self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        # self.graphicsView.setCursor(QtCore.Qt.ArrowCursor)
        # self.graphicsView.mouseMove.connect(self.do_chartView_mouseMove)
        # self.graphicsView.setChart(self.chart_1)
        # self.graphicsView.setObjectName("graphicsView")
        # self.graphicsView_2 = QmyChartView(self.GraphicFrame)
        # self.horizontalLayout.addWidget(self.graphicsView_2)
        # #self.graphicsView_2.setGeometry(QtCore.QRect(620, 0, 591, 541))
        # self.graphicsView_2.setRenderHint(QtGui.QPainter.Antialiasing)
        # self.graphicsView_2.setCursor(QtCore.Qt.ArrowCursor)
        # self.graphicsView_2.mouseMove.connect(self.do_chartView_mouseMove)
        # self.graphicsView_2.setChart(self.chart_2)
        # self.graphicsView_2.setObjectName("graphicsView_2")

        # self.__axisFreq_2 = QtChart.QLogValueAxis()
        # self.__axisFreq_2.setLabelFormat("%d")  # format of the label
        # self.__axisFreq_2.setTitleText("Frequenz / kHz \r\n ")
        # self.__axisFreq_2.setRange(100, 100000)
        # self.__axisFreq_2.setMinorTickCount(8)
        # # self.__axisFreq.tickAn([ticks])
        # self.chart_2.addAxis(self.__axisFreq_2, QtCore.Qt.AlignBottom)
        # self.__axisMag_2 = QtChart.QValueAxis()
        # self.__axisMag_2.setTitleText("Spannung / V ")
        # self.__axisMag_2.setRange(-5, 65)
        # self.__axisMag_2.setTickCount(15)
        # self.__axisMag_2.setLabelFormat("%d")
        # self.chart_2.addAxis(self.__axisMag_2, QtCore.Qt.AlignLeft)

        # # create curve for forward power
        # self.curveFPower = QtChart.QLineSeries()
        # self.curveFPower.setName("P1")
        # self.chart_2.addSeries(self.curveFPower)
        # self.curveFPower.attachAxis(self.__axisFreq_2)
        # self.curveFPower.attachAxis(self.__axisMag_2)
        # self.chart_2.legend().markers(self.curveFPower)[0].setVisible(True)
        # self.chart_2.legend().setAlignment(Qt.AlignTop)
        # pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        # pen.setWidth(1)
        # self.curveFPower.setPen(pen)
        # self.curveFPower.setPointsVisible(True)
        # # self.curveProb.hovered.connect(self.do_series_hovered)
        # # self.curveProb.clicked.connect(self.do_series_clicked)
        #
        # # create curve for field strength
        # self.curveFieldStr = QtChart.QLineSeries()
        # self.curveFieldStr.setName("P1")
        # self.chart_1.addSeries(self.curveFieldStr)
        # self.curveFieldStr.attachAxis(self.__axisFreq)
        # self.curveFieldStr.attachAxis(self.__axisMag)
        # self.chart_1.legend().markers(self.curveFieldStr)[0].setVisible(True)
        # self.chart_1.legend().setAlignment(Qt.AlignTop)
        # pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        # pen.setWidth(1)
        # self.curveFieldStr.setPen(pen)
        # self.curveFieldStr.setPointsVisible(True)
        # # self.curveProb.hovered.connect(self.do_series_hovered)
        # # self.curveProb.clicked.connect(self.do_series_clicked)

        # define signals
        self.OpenFilePushButton.clicked.connect(self.on_actOpen_triggered)
        self.PrintPushButton.clicked.connect(self.handle_print)
        self.HandMovePushButton.clicked.connect(self.on_actZoomIn_triggered)
        # self.HandMovePushButton.clicked.connect(self.hide_line_labels)
        self.pushButton_4.clicked.connect(self.on_actZoomOut_triggered)
        # self.pushButton_4.clicked.connect(self.hide_line_labels)
        self.pushButton_5.clicked.connect(self.on_actZoomReset_triggered)
        #self.pushButton_5.clicked.connect(self.show_line_labels)
        self.TestStratButton.clicked.connect(self.start_thread)
        self.TestPausePushButton.clicked.connect(self.pause_thread)
        self.TestStopPushButton.clicked.connect(self.stop_thread)
        self.pushButton_7.clicked.connect(self._clearall)
        self.ReportGenerierenToolButton.clicked.connect(self.create_word_report)
        #self.graphicsView.rubberBandChanged.connect(self.hide_line_labels)
        self.DatenExportierenToolButton.clicked.connect(self.daten_exportieren)
        #self.toolButton.clicked.connect(self.drawSollSpannung)

        # define the background color of the window
        pale = QtGui.QPalette()
        pale.setColor(QtGui.QPalette.Background, QtGui.QColor(248, 248, 248))
        TestWindow.setPalette(pale)

    def retranslateUi(self, TestWindow):
        _translate = QtCore.QCoreApplication.translate
        TestWindow.setWindowTitle(_translate("TestWindow", "TestWinsow"))
        self.StatusleisteGroupBox.setTitle(_translate("TestWindow", "Statusleiste"))
        self.AktuellerZustandLabel.setText(_translate("TestWindow", "Aktueller Zustand:"))
        self.InformationenKoordinatenGroupBox.setTitle(_translate("TestWindow", "Informationen der Koordinaten"))
        self.GeschwebtLabel.setText(_translate("TestWindow", "Geschwebt"))
        self.GeklicktMagnitudeLabel.setText(_translate("TestWindow", "Magnitude:"))
        self.GeklicktLabel.setText(_translate("TestWindow", "Geklickt"))
        self.GeschwebtMagnitudeLabel.setText(_translate("TestWindow", "Magnitude:"))
        self.GeklicktFrequenzLabel.setText(_translate("TestWindow", "Frequenz:"))
        self.GeschwebtFrequenzLabel.setText(_translate("TestWindow", "Frequenz:"))
        item = self.TestParaInfo.horizontalHeaderItem(0)
        item.setText(_translate("TestWindow", "Antenne"))
        item = self.TestParaInfo.horizontalHeaderItem(1)
        item.setText(_translate("TestWindow", "Strat Frequenz(MHz)"))
        item = self.TestParaInfo.horizontalHeaderItem(2)
        item.setText(_translate("TestWindow", "Frequenz Step(%)"))
        item = self.TestParaInfo.horizontalHeaderItem(3)
        item.setText(_translate("TestWindow", "Max. Frequenz(Mhz)"))
        item = self.TestParaInfo.horizontalHeaderItem(4)
        item.setText(_translate("TestWindow", "Level(dBm)"))
        item = self.TestParaInfo.horizontalHeaderItem(5)
        item.setText(_translate("TestWindow", "Dwell(s)"))
        item = self.TestParaInfo.horizontalHeaderItem(6)
        item.setText(_translate("TestWindow", "Modulation 1"))
        item = self.TestParaInfo.horizontalHeaderItem(7)
        item.setText(_translate("TestWindow", "Modulation 2"))
        __sortingEnabled = self.TestParaInfo.isSortingEnabled()
        self.TestParaInfo.setSortingEnabled(False)
        item = self.TestParaInfo.item(0, 0)
        item.setText(_translate("TestWindow", "Horizental"))
        item = self.TestParaInfo.item(0, 1)
        item.setText(_translate("TestWindow", "90"))
        item = self.TestParaInfo.item(0, 2)
        item.setText(_translate("TestWindow", "1"))
        item = self.TestParaInfo.item(0, 3)
        item.setText(_translate("TestWindow", "1000"))
        item = self.TestParaInfo.item(0, 4)
        item.setText(_translate("TestWindow", "30"))
        item = self.TestParaInfo.item(0, 5)
        item.setText(_translate("TestWindow", "1"))
        item = self.TestParaInfo.item(0, 6)
        item.setText(_translate("TestWindow", "Off"))
        item = self.TestParaInfo.item(0, 7)
        item.setText(_translate("TestWindow", "Off"))
        self.TestStatusLabel.setText(_translate("TestWindow", "Status: "))
        self.label_testSetup.setText(_translate("TestWindow", "Test Einstellungen:"))
        self.TestKontrollenGroupBox.setTitle(_translate("TestWindow", "Testkontrollen"))
        self.TestStartButtonLabel.setText(_translate("TestWindow", "Start"))
        self.DatenExportierenToolButton.setText(_translate("TestWindow", "Daten exportieren"))
        self.ReportGenerierenToolButton.setText(_translate("TestWindow", "Report generieren"))
        self.TestPauseButtonLabel.setText(_translate("TestWindow", "Pause"))
        self.TestStopButtonLabel.setText(_translate("TestWindow", "Stop"))

    def _clearall(self):
        #self.chart_1.removeAllSeries()
        self.curveFPower.clear()
        self.curveFieldStr.clear()
        self.curveFPower_realTime.clear()
        self.curveFieldStr_realTime.clear()
        self.chart_1.legend().markers(self.curveFieldStr)[0].setVisible(False)
        self.chart_2.legend().markers(self.curveFPower)[0].setVisible(False)

    def loadData(self, rows):
        self._clearall()
        # open and read measurement data
        # measurement data in positon 1
        self.measuredFreq = []  # init parameters
        self.forwardPower = []  # init parameters
        self.probData = []  # init parameters
        for i in range(len(rows)):
            self.measuredFreq.append(float(rows[i][0]))  # column 0 is frequency
            self.forwardPower.append(float(rows[i][1]))  # column 1 is forward power
            self.probData.append(float(rows[i][2]))  # column 2 is measurement data field strength from prob

        # adding data forward power to chart1
        for a, b in zip(self.measuredFreq, self.forwardPower):
            self.curveFPower.append(a, b)
        # adding data field strength to chart1
        for a, b in zip(self.measuredFreq, self.probData):
            self.curveFieldStr.append(a, b)

    def start_thread(self):
        self._clearall()
        self.StartFreq = int(self.TestParaInfo.item(0, 1).text())
        self.FreStep = float(self.TestParaInfo.item(0, 2).text()) * 0.01
        self.MaxFreq = int(self.TestParaInfo.item(0, 3).text())
        self.External_FS_test = External_FS_test(StartFreq=self.StartFreq, FreqStep=self.FreStep, MaxFreq=self.MaxFreq)
        self.External_FS_test.start()
        self.AktuellerZustandLineEdit.setText("Test läuft")
        self.TestStatusLabel.setText("Status: %s (%s)" % (
            self.AktuellerZustandLineEdit.text(), time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())))
        self.External_FS_test.countChanged.connect(self.onCountChanged)
        self.External_FS_test.completedflag.connect(self.testCompletedflag)

    def pause_thread(self):
        if not self.External_FS_test.ispaused:
            self.External_FS_test.pause()
            self.AktuellerZustandLineEdit.setText("Test pausiert!")
            self.TestStatusLabel.setText("Status: %s (%s)" % (
                self.AktuellerZustandLineEdit.text(), time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())))
        else:
            self.External_FS_test.resum()
            self.AktuellerZustandLineEdit.setText("Test läuft!")
            self.TestStatusLabel.setText("Status: %s (%s)" % (
                self.AktuellerZustandLineEdit.text(), time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())))

    def stop_thread(self):
        if self.External_FS_test.isRunning():
            self.External_FS_test.stop()
            time.sleep(1)
            self.AktuellerZustandLineEdit.setText("Test wird gestoppt!")
        self.TestStatusLabel.setText("Status: %s (%s)" % (
            self.AktuellerZustandLineEdit.text(), time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())))

    def onCountChanged(self, measuredFreq, vorPower, FieldStrength):  # the parameters rewrite later
        frequenz = measuredFreq
        magnitude1 = vorPower
        magnitude2 = FieldStrength
        self.curveFPower_realTime.append(frequenz, magnitude1)
        self.curveFieldStr_realTime.append(frequenz, magnitude2)
        value = ((frequenz - self.StartFreq) / (self.MaxFreq - self.StartFreq)) * 100
        print("start Fre %s" % self.StartFreq)
        print("value ist %s" % value)
        print("max freq %s" % self.MaxFreq)
        self.StatusProgressBar.setValue(value)
        
    def onDataCache(self, measuredFreq, vorPower, FieldStrength):
        colum1 = [measuredFreq]
        colum2 = [vorPower]
        colum3 = [FieldStrength]

        return colum1, colum2, colum3

    def dateSave(self):
        savedData = self.onDataCache()
        self.colum_Freq = savedData[0]
        self.colum_vorPow = savedData[1]
        self.colum_fieldStr = savedData[2]
        rows = [[]]
        pass

    def testCompletedflag(self, completed):
        if completed == True:
            self.AktuellerZustandLineEdit.setText("Test ist fertig!")
            self.TestStatusLabel.setText("Status: %s (%s)" % (
                self.AktuellerZustandLineEdit.text(), time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())))

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
        self.MousPositionLabel.setText("Chart X=%.2f,Y=%.2f" % (pt.x(), pt.y()))

        # when the button "Pause" is clicked, the measuring process will take a break

    def daten_exportieren(self):
        pass
    #     if self.curve1.isChecked() == False and \
    #             self.curve2.isChecked() == False and \
    #             self.curve3.isChecked() == False and \
    #             self.curve4.isChecked() == False:
    #         messageBox = QtWidgets.QMessageBox()
    #         messageBox.setWindowTitle('Kurvenauswahl')
    #         messageBox.setIcon(QtWidgets.QMessageBox.Warning)
    #         messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
    #         messageBox.setText(
    #             'Bitte wählen Sie zuerst eine Kurve aus!')
    #         messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    #         buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
    #         buttonY.setText('Ok')
    #         messageBox.exec_()
    #     else:
    #         if self.curve1.isChecked() == True and self.series_1 is not None:
    #             fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, 'Messergebnisse speichern', 'd:\\',
    #                                                                 'Ergebnisse (*.txt)')
    #             f = open(fileName, "a")
    #             detektor = self.detektor1.currentText()
    #             f.write('Detektor: %s' % detektor)
    #             f.write('\t')
    #             attenuation = self.antten1.text()
    #             f.write('Attenuation: %s dB' % attenuation)
    #             f.write('\t')
    #             messtime = self.messtime1.text()
    #             f.write('Messzeit: %s ms' % messtime)
    #             f.write('\t')
    #             Startfre = self.startfre1.text()
    #             f.write('Startfrequenz: %s MHz' % Startfre)
    #             f.write('\n')
    #             f.write('Frequenz: MHz')
    #             f.write('\t')
    #             f.write('Feldstärke: dBuV/m')
    #             f.write('\n')
    #             for fre, mag in self.series_1:
    #                 f.write(fre)
    #                 f.write('\t')
    #                 f.write(mag)
    #                 f.write('\n')
    #             messageBox = QtWidgets.QMessageBox()
    #             messageBox.setWindowTitle('Hinweis')
    #             messageBox.setIcon(QtWidgets.QMessageBox.Information)
    #             messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/3.png'))
    #             messageBox.setText('Die Daten werden erfolgreich exportiert!')
    #             messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    #             buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
    #             buttonY.setText('Ok')
    #             messageBox.exec_()
    #         elif self.curve2.isChecked() == True and self.series_2 is not None:
    #             fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, 'Messergebnisse speichern', 'd:\\',
    #                                                                 'Ergebnisse (*.txt)')
    #             f = open(fileName, "a")
    #             detektor = self.detektor2.currentText()
    #             f.write('Detektor: %s' % detektor)
    #             f.write('\t')
    #             attenuation = self.antten2.text()
    #             f.write('Attenuation: %s dB' % attenuation)
    #             f.write('\t')
    #             messtime = self.messtime2.text()
    #             f.write('Messzeit: %s ms' % messtime)
    #             f.write('\t')
    #             Startfre = self.startfre2.text()
    #             f.write('Startfrequenz: %s MHz' % Startfre)
    #             f.write('\n')
    #             f.write('Frequenz: MHz')
    #             f.write('\t')
    #             f.write('Feldstärke: dBuV/m')
    #             f.write('\n')
    #             for fre, mag in self.series_2:
    #                 f.write(fre)
    #                 f.write('\t')
    #                 f.write(mag)
    #                 f.write('\n')
    #             messageBox = QtWidgets.QMessageBox()
    #             messageBox.setWindowTitle('Hinweis')
    #             messageBox.setIcon(QtWidgets.QMessageBox.Information)
    #             messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/3.png'))
    #             messageBox.setText('Die Daten werden erfolgreich exportiert!')
    #             messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    #             buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
    #             buttonY.setText('Ok')
    #             messageBox.exec_()
    #
    #         elif self.curve3.isChecked() == True and self.series_3 is not None:
    #             fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, 'Messergebnisse speichern', 'd:\\',
    #                                                                 'Ergebnisse (*.txt)')
    #             f = open(fileName, "a")
    #             detektor = self.detektor3.currentText()
    #             f.write('Detektor: %s' % detektor)
    #             f.write('\t')
    #             attenuation = self.antten3.text()
    #             f.write('Attenuation: %s dB' % attenuation)
    #             f.write('\t')
    #             messtime = self.messtime3.text()
    #             f.write('Messzeit: %s ms' % messtime)
    #             f.write('\t')
    #             Startfre = self.startfre3.text()
    #             f.write('Startfrequenz: %s MHz' % Startfre)
    #             f.write('\n')
    #             f.write('Frequenz: MHz')
    #             f.write('\t')
    #             f.write('Feldstärke: dBuV/m')
    #             f.write('\n')
    #             for fre, mag in self.series_3:
    #                 f.write(fre)
    #                 f.write('\t')
    #                 f.write(mag)
    #                 f.write('\n')
    #             messageBox = QtWidgets.QMessageBox()
    #             messageBox.setWindowTitle('Hinweis')
    #             messageBox.setIcon(QtWidgets.QMessageBox.Information)
    #             messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/3.png'))
    #             messageBox.setText('Die Daten werden erfolgreich exportiert!')
    #             messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    #             buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
    #             buttonY.setText('Ok')
    #             messageBox.exec_()
    #         elif self.curve4.isChecked() == True and self.series_4 is not None:
    #             fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, 'Messergebnisse speichern', 'd:\\',
    #                                                                 'Ergebnisse (*.txt)')
    #             f = open(fileName, "a")
    #             detektor = self.detektor4.currentText()
    #             f.write('Detektor: %s' % detektor)
    #             f.write('\t')
    #             attenuation = self.antten4.text()
    #             f.write('Attenuation: %s dB' % attenuation)
    #             f.write('\t')
    #             messtime = self.messtime4.text()
    #             f.write('Messzeit: %s ms' % messtime)
    #             f.write('\t')
    #             Startfre = self.startfre4.text()
    #             f.write('Startfrequenz: %s MHz' % Startfre)
    #             f.write('\n')
    #             f.write('Frequenz: MHz')
    #             f.write('\t')
    #             f.write('Feldstärke: dBuV/m')
    #             f.write('\n')
    #             for fre, mag in self.series_4:
    #                 f.write(fre)
    #                 f.write('\t')
    #                 f.write(mag)
    #                 f.write('\n')
    #             messageBox = QtWidgets.QMessageBox()
    #             messageBox.setWindowTitle('Hinweis')
    #             messageBox.setIcon(QtWidgets.QMessageBox.Information)
    #             messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/3.png'))
    #             messageBox.setText('Die Daten werden erfolgreich exportiert!')
    #             messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    #             buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
    #             buttonY.setText('Ok')
    #             messageBox.exec_()

    # by clicking the "Report generieren" button, a test report will be generated automatically
    def create_word_report(self):
        pix = self.graphicsView.grab()
        image = pix.toImage()
        image = qimage2ndarray.rgb_view(image, byteorder='little')
        savepath = 'D:/demo.png'
        cv.imwrite(savepath, image)
        WordReportGenerator.generate_word(savepath)
        # os.remove(savepath)
        messageBox = QtWidgets.QMessageBox()
        messageBox.setWindowTitle('Report')
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setWindowIcon(QtGui.QIcon('./icon_materials/8.png'))
        messageBox.setText('Der Word-Report wird erfolgreich generiert!')
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        buttonY = messageBox.button(QtWidgets.QMessageBox.Ok)
        buttonY.setText('Ok')
        messageBox.exec_()

    def on_actOpen_triggered(self):
        curPath = QtCore.QDir.currentPath()
        filename, flt = QtWidgets.QFileDialog.getOpenFileName(None, "Eine Datei öffnen", curPath, "Testdaten (*.csv)")
        if (filename == ""):
            return
        with open("%s" % filename, "r") as FSCaliData:
            reader = csv.reader(FSCaliData)
            rows = []
            for row in reader:
                rows.append(row)
        # aFile = open(filename, 'r')
        # allLine = aFile.readlines()
        # aFile.close()
        fileInfo = QtCore.QFileInfo(filename)
        QtCore.QDir.setCurrent(fileInfo.absolutePath())

        self.loadData(rows)

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

    # zoom out the diagram
    def on_actZoomIn_triggered(self):
        self.graphicsView.chart().zoom(1.2)
        self.graphicsView_2.chart().zoom(1.2)

    # zoom in the diagram
    def on_actZoomOut_triggered(self):
        self.graphicsView.chart().zoom(0.8)
        self.graphicsView_2.chart().zoom(0.8)

    # reset the diagram into original size
    def on_actZoomReset_triggered(self):
        self.graphicsView.chart().zoomReset()
        self.graphicsView_2.chart().zoomReset()

def color(hex):
    r = int(hex[1:3], 16)
    g = int(hex[3:5], 16)
    b = int(hex[5:7], 16)
    return r, g, b

if __name__ == "__main__":
    import sys

    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling) # 用于自适应屏幕，在自己电脑上使用可能GUI太大，带上屏幕之后没有问题

    app = QtWidgets.QApplication(sys.argv)
    TestWindow = QtWidgets.QWidget()
    ui = Ui_TestWindow_FS()
    ui.setupUi(TestWindow)
    #ui.drawSollSpannung()
    TestWindow.show()
    sys.exit(app.exec_())