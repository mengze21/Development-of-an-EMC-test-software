# -*- coding: utf-8 -*-

import sys
from PyQt5 import uic, QtWidgets, QtChart, QtCore, QtGui
from PyQt5.QtCore import Qt


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

class test(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(test, self).__init__(parent)
        uic.loadUi("uifiles/testQchart.ui", self)

        self.chart_1 = QtChart.QChart()
        self.chart_2 = QtChart.QChart()

        self.__axisFreq = QtChart.QLogValueAxis()
        self.__axisFreq.setLabelFormat("%d")  # format of the label
        self.__axisFreq.setTitleText("Frequenz / kHz \r\n ")
        self.__axisFreq.setRange(100, 100000)
        self.__axisFreq.setMinorTickCount(8)
        self.chart_1.addAxis(self.__axisFreq, QtCore.Qt.AlignBottom)

        self.__axisMag = QtChart.QValueAxis()
        self.__axisMag.setTitleText("Generator - Leistung / dBm  ")
        self.__axisMag.setRange(-35, -0)
        self.__axisMag.setTickCount(8)
        self.__axisMag.setLabelFormat("%d")
        self.chart_1.addAxis(self.__axisMag, QtCore.Qt.AlignLeft)

        self.__axisFreq_2 = QtChart.QLogValueAxis()
        self.__axisFreq_2.setLabelFormat("%d")  # format of the label
        self.__axisFreq_2.setTitleText("Frequenz / kHz \r\n ")
        self.__axisFreq_2.setRange(100, 100000)
        self.__axisFreq_2.setMinorTickCount(8)
        #self.__axisFreq.tickAn([ticks])
        self.chart_2.addAxis(self.__axisFreq_2, QtCore.Qt.AlignBottom)

        self.__axisMag_2 = QtChart.QValueAxis()
        self.__axisMag_2.setTitleText("Spannung / V ")
        self.__axisMag_2.setRange(-5, 65)
        self.__axisMag_2.setTickCount(15)
        self.__axisMag_2.setLabelFormat("%d")
        self.chart_2.addAxis(self.__axisMag_2, QtCore.Qt.AlignLeft)

        self.graphicsView = QmyChartView(self.frame)
        #self.graphicsView.setGeometry(QtCore.QRect(0, 0, 300, 400))
        #self.graphicsView.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addWidget(self.graphicsView)
        #self.verticalLayout.addWidget(self.frame)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView.setCursor(QtCore.Qt.ArrowCursor)
        self.graphicsView.mouseMove.connect(self.do_chartView_mouseMove)
        self.graphicsView.setChart(self.chart_1)
        self.graphicsView.setObjectName("graphicsView")

        self.graphicsView_2 = QmyChartView(self.frame)
        #self.graphicsView_2.setGeometry(QtCore.QRect(300, 0, 300, 400))
        self.horizontalLayout.addWidget(self.graphicsView_2)
        self.graphicsView_2.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView_2.setCursor(QtCore.Qt.ArrowCursor)
        self.graphicsView_2.mouseMove.connect(self.do_chartView_mouseMove)
        self.graphicsView_2.setChart(self.chart_2)
        self.graphicsView_2.setObjectName("graphicsView_2")

        self.curveProb = QtChart.QLineSeries()
        # self.normline1.setName("Norm Line 1.")
        self.chart_2.addSeries(self.curveProb)
        self.curveProb.attachAxis(self.__axisFreq_2)
        self.curveProb.attachAxis(self.__axisMag_2)
        self.chart_2.legend().markers(self.curveProb)[0].setVisible(True)
        self.chart_2.legend().setAlignment(Qt.AlignTop)

        pen = QtGui.QPen(QtGui.QColor(255, 0, 255))
        pen.setWidth(1)
        self.curveProb.setPen(pen)

        self.curveProb.setPointsVisible(True)
        #self.curveProb.hovered.connect(self.do_series_hovered)
        #self.curveProb.clicked.connect(self.do_series_clicked)

        self.x = [150, 1000, 1001, 10000, 10001, 80000]
        self.y = [10, 10, 10, 10, 10, 13]
        # print(y)

        for a, b in zip(self.x, self.y):
            self.curveProb.append(a, b)

    def do_chartView_mouseMove(self, point):
        pt = self.graphicsView.chart().mapToValue(point)
        self.MousPositionLabel.setText("Chart X=%.2f,Y=%.2f"%(pt.x(),pt.y()))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = test()
    sys.exit(ui.exec_())
