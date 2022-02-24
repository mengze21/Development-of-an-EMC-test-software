import sys, os
from os.path import join, getsize

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import time
sys.path.append('gui')


class External_FS_test(QThread):
    completedflag = pyqtSignal(bool, int)
    countChanged = pyqtSignal(float, float, float, float, int)
    positionChanged = pyqtSignal(int)          # emit the current calibration position
    #dataCache = pyqtSignal(list, list, list)

    def __init__(self, StartFreq, FreqStep, MaxFreq, E_T, startAPM, Position):
        #QtCore.QThread.__init__(self)
        super(External_FS_test, self).__init__()
        self.StartFreq = StartFreq
        self.FreqStep = FreqStep
        self.MaxFreq = MaxFreq
        self.position = Position
        self.stopped = False
        self.completed = False
        self.restart = False
        self.isPaused = False
        self.isWaiting = False
        self.testFreq = 0
        self.vorPower = 0
        self.bwdPow = 0
        self.FieldStrength = 0

    #def initialize(self):
        #self.stopped = False
        #self.completed = False
        #self.restart = False

    def run(self):
        #self.stopped = False
        #self.testFreq = self.StartFreq
        # measuredFreq = 0
        # vorPower = 0
        # FieldStrength = 0
        while self.position in range(6):
            self.stopped = False
            self.completed = False
            self.testFreq = self.StartFreq
            position = self.position
            while self.testFreq < self.MaxFreq:
                self.vorPower = self.vorPower + 0.01
                self.bwdPow = self.vorPower - 2
                self.FieldStrength = self.FieldStrength + 0.04
                print("testFreq %s" % self.testFreq)
                print("freq step %s" % self.FreqStep)
                print("position %s" % self.position)
                measuredFreq = self.testFreq
                vorPower = self.vorPower
                bwdPow = self.bwdPow
                FieldStrength = self.FieldStrength
                self.testFreq = self.testFreq + self.FreqStep * self.testFreq
                self.countChanged.emit(measuredFreq, vorPower, bwdPow, FieldStrength, position)

                time.sleep(0.01)
                while self.isPaused:
                    time.sleep(0)

                if self.stopped:
                    break
            if not self.stopped:
                self.completed = True
                completed = self.completed
                self.completedflag.emit(completed, position)

            self.isWaiting = True       # set isWaiting True to wait change of the position

            # waite for input 'Fortfahren'
            while self.isWaiting:
                time.sleep(0)

            self.position += 1
            print(self.position)


        #self.completed = True
        #self.completedflag.emit(self.completed)
        # for i in range(10):
        #     print(i)
        #     time.sleep(1)
        #
        #     while self.ispaused:
        #         time.sleep(0)
        #
        #     if self.stopped:
        #         break
        # if i == 9 :
        #     print("thread finished")
        #self.completed = True
        #completed = self.completed
        #self.completedflag.emit(completed)

    def stop(self):
        print("thread stoped")
        self.stopped = True

    def pause(self):
        self.isPaused = True

    def resum(self):
        self.isPaused = False

    def runNextTest(self):
        self.isWaiting = False
